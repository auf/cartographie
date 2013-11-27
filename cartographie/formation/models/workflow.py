# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from cartographie.formation.constants import statuts_formation as STATUTS
from cartographie.formation.models import UserRole

ETATS = [
    (STATUTS.supprimee, STATUTS.supprimee_label),
    (STATUTS.en_redaction, STATUTS.en_redaction_label),
    (STATUTS.validee, STATUTS.validee_label),
    (STATUTS.publiee, STATUTS.publiee_label),
]


def is_statut_final(statut_id):
    return int(statut_id) == int(STATUTS.supprimee)


def statusIdToStatusLabel(value):
    labels = filter(lambda x: x[0] == int(value), ETATS)

    if len(labels) == 1:
        lbl = labels.pop()

        return lbl[1]

    return ""


def exception_msg_sequence(statut_label):
    return u"""
        Vous ne pouvez pas attribuer le statut %s à cette fiche
    """ % statut_label


class WorkflowMixin(models.Model):

    statut = models.IntegerField(
        choices=ETATS,
        default=STATUTS.en_redaction
    )

    class Meta:
        abstract = True

    def changement_necessite_commentaire(self, statut_id):
        precedent = self.is_statut_precedent(statut_id)
        terminal = self.is_statut_terminal(statut_id)

        return precedent or terminal

    def is_statut_precedent(self, statut_id):
        return statut_id == STATUTS.en_redaction

    def is_statut_terminal(self, statut_id):
        if statut_id == STATUTS.supprimee:
            return True
        return False

    def set_statut(self, user, token, statut_id):
        has_permission = UserRole.has_permission_for_transition(
            user, token, self, statut_id)

        if has_permission:
            self.statut = statut_id

        return has_permission

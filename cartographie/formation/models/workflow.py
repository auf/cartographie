#coding: utf-8

from django.db import models
from cartographie.formation.constants import statuts_formation as STATUTS
from cartographie.formation.decorators import superuser_and_editeur_only


ETATS = [
    (STATUTS.abandonnee, STATUTS.abandonnee_label),
    (STATUTS.archivee, STATUTS.archivee_label),
    (STATUTS.en_redaction, STATUTS.en_redaction_label),
    (STATUTS.validee, STATUTS.validee_label),
    (STATUTS.publiee, STATUTS.publiee_label),
]


class WorkflowException(Exception):
    pass


def exception_msg_sequence(statut_label):
    return u"""
        Vous ne pouvez pas attribuer le statut %s à cette fiche
    """ % statut_label


def exception_msg_permission(user):
    return u"""
        L'utilisateur %s n'a pas le droit de modifier un statut.
    """ % user.username


class WorkflowMixin(models.Model):

    statut = models.IntegerField(
        choices=ETATS,
        default=STATUTS.en_redaction
    )

    class Meta:
        abstract = True

    def set_abandonnee(self, request):
        if self.statut in (STATUTS.validee, STATUTS.en_redaction):
            self.statut = STATUTS.abandonnee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.abandonnee_label)
            )

    @superuser_and_editeur_only
    def set_archivee(self, request):
        if self.statut in (STATUTS.publiee):
            self.statut = STATUTS.archivee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.archivee_label)
            )

    def set_en_redaction(self, request):
        if self.statut in (STATUTS.publiee, STATUTS.validee):
            # pour ramener le statut en rédaction à partir d'une
            # rédaction publiée ou validée
            self.statut = STATUTS.en_redaction
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.en_redaction_label)
            )
        pass

    def set_validee(self, request):
        if self.statut in (STATUTS.en_redaction):
            self.statut = STATUTS.validee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.validee_label)
            )
        pass

    @superuser_and_editeur_only
    def set_publiee(self, request):
        if self.statut in (STATUTS.validee):
            self.statut = STATUTS.publiee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.publiee_label)
            )
        pass

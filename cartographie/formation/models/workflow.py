#coding: utf-8

from django.db import models
from cartographie.formation.constants import statuts_formation as STATUTS

ETATS = [
    (STATUTS.abandonnee, STATUTS.abandonnee_label),
    (STATUTS.archivee, STATUTS.archivee_label),
    (STATUTS.en_redaction, STATUTS.en_redaction_label),
    (STATUTS.validee, STATUTS.validee_label),
    (STATUTS.publiee, STATUTS.publiee_label),
]


class WorkflowException(Exception):
    pass


def exception_message(statut_label):
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

    def set_abandonnee(self):

        if self.statut in (STATUTS.validee, STATUTS.en_redaction):
            self.statut = STATUTS.abandonnee
        else:
            raise WorkflowException(
                exception_message(STATUTS.abandonnee_label)
            )

    def set_archivee(self):
        if self.statut in (STATUTS.publiee):
            self.statut = STATUTS.archivee
        else:
            raise WorkflowException(
                exception_message(STATUTS.archivee_label)
            )

    def set_en_redaction(self):
        if self.statut in (STATUTS.publiee, STATUTS.validee):
            self.statut = STATUTS.en_redaction
        else:
            raise WorkflowException(
                exception_message(STATUTS.en_redaction_label)
            )
        pass

    def set_validee(self):
        if self.statut in (STATUTS.en_redaction):
            self.statut - STATUTS.validee
        else:
            raise WorkflowException(
                exception_message(STATUTS.validee_label)
            )
        pass

    def set_publiee(self):
        if self.statut in (STATUTS.validee):
            self.statut = STATUTS.publiee
        else:
            raise WorkflowException(
                exception_message(STATUTS.publiee_label)
            )
        pass

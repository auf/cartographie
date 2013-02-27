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


def superuser_and_editeur_only(f):
    """
        descriptor/decorator pour vérifier qu'un user est un editeur
    """
    def decorator(self, request):
        user = request.user

        if user and not user.is_superuser:
            role = models.UserRole.objects.get(user=user)

            if role.type != "editeur":
                raise WorkflowException(u"""
                    L'usager courant n'est pas un éditeur
                    et ne peux pas modifier ce statut
                """)
        f(self, request)

    return decorator


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

    def set_abandonnee(self, request):
        if self.statut in [STATUTS.validee, STATUTS.en_redaction]:
            self.statut = STATUTS.abandonnee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.abandonnee_label)
            )

    @superuser_and_editeur_only
    def set_archivee(self, request):
        if self.statut in [STATUTS.publiee]:
            self.statut = STATUTS.archivee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.archivee_label)
            )

    def set_en_redaction(self, request):
        if self.statut in [STATUTS.publiee, STATUTS.validee, STATUTS.abandonnee]:
            # pour ramener le statut en rédaction à partir d'une
            # rédaction publiée ou validée
            self.statut = STATUTS.en_redaction
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.en_redaction_label)
            )
        pass

    def set_validee(self, request):
        if self.statut in [STATUTS.en_redaction]:
            self.statut = STATUTS.validee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.validee_label)
            )
        pass

    @superuser_and_editeur_only
    def set_publiee(self, request):
        if self.statut in [STATUTS.validee]:
            self.statut = STATUTS.publiee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.publiee_label)
            )
        pass

    def set_statut(self, request, statut_id):
        if statut_id == STATUTS.abandonnee:
            self.set_abandonnee(request)

        if statut_id == STATUTS.archivee:
            self.set_archivee(request)

        if statut_id == STATUTS.en_redaction:
            self.set_en_redaction(request)

        if statut_id == STATUTS.validee:
            self.set_validee(request)

        if statut_id == STATUTS.publiee:
            self.set_publiee(request)


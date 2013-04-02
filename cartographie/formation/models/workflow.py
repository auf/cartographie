#coding: utf-8

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

def statusIdToStatusLabel(value):
    labels = filter(lambda x: x[0] == int(value), ETATS)

    if len(labels) == 1:
        lbl = labels.pop()

        return lbl[1]

    return ""


class WorkflowException(Exception):
    pass


def superuser_and_editeur_only(f):
    """
        descriptor/decorator pour vérifier qu'un user est un editeur
    """
    def decorator(self, request):
        user = request.user

        if user and not user.is_superuser:
            try:
                role = UserRole.objects.get(user__id=user.id)
            except ObjectDoesNotExist:
                raise WorkflowException(u"""
                    Vous ne pouvez pas attribuer ce statut
                """)

            if role.type != "editeur":
                raise WorkflowException(u"""
                    Vous ne pouvez pas attribuer ce statut
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

    def set_supprimee(self, request):
        if self.statut in [STATUTS.validee, STATUTS.en_redaction]:
            self.statut = STATUTS.supprimee
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.supprimee_label)
            )

    def set_en_redaction(self, request):
        if self.statut in [STATUTS.publiee, STATUTS.validee, \
            STATUTS.supprimee]:
            self.statut = STATUTS.en_redaction
        else:
            raise WorkflowException(
                exception_msg_sequence(STATUTS.en_redaction_label)
            )
        pass

    # Seul un admin ou un éditeur peut rétrograder une formation
    # publiée en une formation validée.
    def set_validee(self, request):
        def user_can_downgrade_to_valid():
            user = request.user

            if user and not user.is_superuser:
                try:
                    role = UserRole.objects.get(user__id=user.id)
                except ObjectDoesNotExist:
                    raise WorkflowException(u"""
                    Vous ne pouvez pas attribuer ce statut
                """)

                if role.type != "editeur":
                    raise WorkflowException(u"""
                    Vous ne pouvez pas attribuer ce statut
                """)

            return True

        if self.statut == STATUTS.en_redaction or \
                (self.statut == STATUTS.publiee and \
                     user_can_downgrade_to_valid()):
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

    def changement_necessite_commentaire(self, statut_id):
        return self.is_statut_precedent(statut_id)\
          or self.is_statut_terminal(statut_id)

    def is_statut_precedent(self, statut_id):
        return statut_id == STATUTS.en_redaction

    def is_statut_terminal(self, statut_id):
        if statut_id == STATUTS.supprimee:
            return True
        return False

    def set_statut(self, request, statut_id):
        if statut_id == STATUTS.supprimee:
            self.set_supprimee(request)

        if statut_id == STATUTS.en_redaction:
            self.set_en_redaction(request)

        if statut_id == STATUTS.validee:
            self.set_validee(request)

        if statut_id == STATUTS.publiee:
            self.set_publiee(request)


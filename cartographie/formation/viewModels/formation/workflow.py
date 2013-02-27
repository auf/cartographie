# coding: utf-8

from django.contrib import messages

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.models import Formation
from cartographie.formation.models.workflow import ETATS, WorkflowException


class WorkflowViewModel(BaseAjouterViewModel):

    def __init__(self, request, token, formation_id, statut_id):
        super(WorkflowViewModel, self).__init__(request, token)

        statut_id = int(statut_id)

        # verifier que le statut existe
        if statut_id in map(lambda st: st[0], ETATS):
            # obtenir la formation courante
            formation_courante = Formation.objects.get(pk=formation_id)

            # modifier le statut avec les fonctions de WorkflowMixin
            try:
                formation_courante.set_statut(request, statut_id)

                statut_labels = filter(lambda st: st[0] == statut_id, ETATS)
                statut_label = statut_labels.pop()

                messages.success(
                    request, u"Le statut '%s' a été appliqué à la fiche" % statut_label[1]
                )

                formation_courante.save()
            except WorkflowException as exception:
                messages.warning(
                    request, exception
                )
        else:
            messages.warning(
                request, u"Ce statut n'existe pas"
            )

    def get_data(self):
        data = super(WorkflowViewModel, self).get_data()

        return data

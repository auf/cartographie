# coding: utf-8

from django.contrib import messages

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.models import Formation
from cartographie.formation.models.workflow import ETATS
from cartographie.formation.constants import statut2label
from cartographie.formation.workflow import TRANSITIONS


class WorkflowViewModel(BaseAjouterViewModel):

    def __init__(self, request, token, formation_id, statut_id):
        super(WorkflowViewModel, self).__init__(request, token)

        statut_id = int(statut_id)

        # verifier que le statut existe
        if statut_id in map(lambda st: st[0], ETATS):

            # obtenir la formation courante
            formation_courante = Formation.objects.get(pk=formation_id)
            
            self.necessite_commentaire = formation_courante\
                .changement_necessite_commentaire(statut_id)

            pas_de_probleme = False
            # modifier le statut avec les fonctions de WorkflowMixin
            statut_modifie = formation_courante.set_statut(request.user, token, statut_id)

            if statut_modifie:
                pas_de_probleme = True
            else:
                messages.error(request, u"Vous ne pouvez pas attribuer le statut '%s' à cette fiche." % statut2label[statut_id])
      
            if pas_de_probleme:
                statut_labels = filter(lambda st: st[0] == statut_id, ETATS)
                statut_label = statut_labels.pop()

                messages.success(
                    request, u"Le statut '%s' a été appliqué à la fiche" % statut_label[1]
                )

                formation_courante.save()
                formation_courante.save_modification(request)
        else:
            messages.warning(
                request, u"Ce statut n'existe pas"
            )

    def get_data(self):
        data = super(WorkflowViewModel, self).get_data()

        return data

#coding: utf-8

from cartographie.formation.viewModels.baseListeViewModel import BaseListeViewModel

from cartographie.formation.models import FormationComposante


class ListeViewModel(BaseListeViewModel):
    """
        Ce ViewModel hérite des propriétés de base
    """
    composantes = []

    def __init__(self, token, onglet_actif="composante"):
        super(ListeViewModel, self).__init__(token, onglet_actif)

        self.composantes = FormationComposante.objects.all().order_by(
            "etablissementComposante__nom"
        )

    def get_data(self):
        data = super(ListeViewModel, self).get_data()
        data["composantes"] = self.composantes
        return data

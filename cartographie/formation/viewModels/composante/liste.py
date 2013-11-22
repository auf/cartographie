#coding: utf-8

from cartographie.formation.viewModels.baseListeViewModel import BaseListeViewModel

from cartographie.formation.models import EtablissementComposante


class ListeViewModel(BaseListeViewModel):
    """
        Ce ViewModel hérite des propriétés de base
    """
    composantes = []

    def __init__(self, token, user, onglet_actif="composante"):
        super(ListeViewModel, self).__init__(token, user, onglet_actif)

        self.composantes = EtablissementComposante.objects.filter(
            etablissement=self.etablissement
        ).order_by("nom")

    def get_data(self):
        data = super(ListeViewModel, self).get_data()
        data["composantes"] = self.composantes
        return data

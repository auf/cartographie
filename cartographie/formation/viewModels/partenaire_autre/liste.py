#coding: utf-8

from cartographie.formation.viewModels.baseListeViewModel import BaseListeViewModel

from cartographie.formation.models import EtablissementAutre


class ListeViewModel(BaseListeViewModel):
    """
        Ce ViewModel hérite des propriétés de base
    """
    partenaires_autres = []

    def __init__(self, token, onglet_actif="partenaire-autre"):
        super(ListeViewModel, self).__init__(token, onglet_actif)

        self.partenaires_autres = EtablissementAutre.objects.all().order_by("nom")

    def get_data(self):
        data = super(ListeViewModel, self).get_data()
        data["partenaires_autres"] = self.partenaires_autres
        return data

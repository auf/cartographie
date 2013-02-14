#coding: utf-8

from cartographie.formation.viewModels.baseListeViewModel import BaseListeViewModel

from cartographie.formation.models import Personne


class ListeViewModel(BaseListeViewModel):
    personnes = []

    def __init__(self, token, onglet_actif="personne"):
        super(ListeViewModel, self).__init__(token, onglet_actif)

        self.personnes = Personne.objects.filter(
            etablissement=self.etablissement
        ).order_by("nom", "prenom")

    def get_data(self):
        data = super(ListeViewModel, self).get_data()
        data["personnes"] = self.personnes
        return data

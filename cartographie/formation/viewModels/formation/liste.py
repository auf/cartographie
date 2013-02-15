# coding: utf-8

from cartographie.formation.viewModels.baseListeViewModel \
    import BaseListeViewModel

from cartographie.formation.models import Formation


class ListeViewModel(BaseListeViewModel):
    formations = []

    def __init__(self, token, onglet_actif="formation"):
        super(ListeViewModel, self).__init__(token, onglet_actif)

        # filtrer les formations pour ceux de l'établissement courant
        self.formations = Formation.objects.filter(
            etablissement=self.etablissement
        ).order_by("nom")

    def get_data(self):
        data = super(ListeViewModel, self).get_data()

        data["formations"] = self.formations

        return data

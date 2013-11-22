# -*- coding: utf-8 -*-

from cartographie.formation.viewModels.baseListeViewModel import (
    BaseListeViewModel)

from cartographie.formation.models import Formation


class ListeViewModel(BaseListeViewModel):

    formations = []

    def __init__(self, token, user, onglet_actif="formation"):
        super(ListeViewModel, self).__init__(token, user, onglet_actif)

        # filtrer les formations pour ceux de l'établissement courant

        self.cacher_onglets = True if onglet_actif == "formation" else False

        self.formations = Formation.objects.exclude(
            statut=999).filter(
            etablissement=self.etablissement).order_by('nom')

    def get_data(self):
        data = super(ListeViewModel, self).get_data()
        data["cacher_onglets"] = self.cacher_onglets
        data["formations"] = self.formations
        data['etablissement_id'] = self.etablissement.id

        return data

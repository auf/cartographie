# -*- coding: utf-8 -*-

from cartographie.formation.models import EtablissementAutre
from cartographie.formation.viewModels.baseListeViewModel import (
    BaseListeViewModel)


class ListeViewModel(BaseListeViewModel):

    partenaires_autres = []

    def __init__(self, token, user,  onglet_actif="partenaire-autre"):
        super(ListeViewModel, self).__init__(token, user, onglet_actif)

        self.partenaires_autres = EtablissementAutre.objects.filter(
            etablissement=self.etablissement).order_by("nom")

    def get_data(self):
        data = super(ListeViewModel, self).get_data()
        data["partenaires_autres"] = self.partenaires_autres
        return data

#coding: utf-8

from cartographie.formation.viewModels.baseListeViewModel \
    import BaseListeViewModel

from cartographie.formation.models import Langue


class ListeViewModel(BaseListeViewModel):
    langues = []

    def __init__(self, token, onglet_actif="langue"):
        super(ListeViewModel, self).__init__(token, onglet_actif)

        self.langues = Langue.objects.all().order_by("nom", "actif")

    def get_data(self):
        data = super(ListeViewModel, self).get_data()
        data["langues"] = self.langues
        return data

# coding: utf-8

from ..models import Acces, Formation


class ListViewModel(object):
    token = None
    etablissement = None
    formations = []

    def __init__(self, token):
        if token:
            self.token = token
            acces = Acces.objects.filter(token=token)[0]

            self.etablissement = acces.etablissement
            self.formations = Formation.objects.filter(
                etablissement=self.etablissement
            ).order_by("nom")

    def get_data(self):
        return {
            "token": self.token,
            "etablissement": self.etablissement,
            "formations": self.formations
        }

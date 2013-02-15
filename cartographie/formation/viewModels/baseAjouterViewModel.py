# coding: utf-8

from cartographie.formation.models import Acces


class BaseAjouterViewModel(object):
    token = None
    etablissement = None

    def __init__(self, request, token):
        if token:
            self.token = token
            acces = Acces.objects.get(token=token)
            self.etablissement = acces.etablissement

    def get_data(self):
        return {
            "token": self.token,
            "etablissement": self.etablissement
        }

# coding: utf-8

from cartographie.formation.models import Acces


class BaseListeViewModel(object):
    """
        La class de Base qui contient les propriétés essentiels
        pour une ListeViewModel
    """

    onglet_actif = None
    token = None
    etablissement = None

    def __init__(self, token, onglet_actif):
        if token:
            self.token = token
            acces = Acces.objects.filter(token=token)[0]
            self.etablissement = acces.etablissement
            self.onglet_actif = onglet_actif

    def get_data(self):
        return {
            "onglet_actif": self.onglet_actif,
            "token": self.token,
            "etablissement": self.etablissement
        }

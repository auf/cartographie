#coding: utf-8


class ListeEtablissementsViewModel(object):
    menu_actif = None

    def __init__(self, request, menu_actif="liste_etablissements"):
        self.menu_actif = menu_actif

    def get_data(self):
        return {
            "menu_actif": self.menu_actif
        }

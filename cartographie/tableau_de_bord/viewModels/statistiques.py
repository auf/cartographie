#coding: utf-8


class StatistiquesViewModel(object):
    menu_actif = None

    def __init__(self, request, menu_actif="statistiques"):
        self.menu_actif = menu_actif

    def get_data(self):
        return {
            "menu_actif": self.menu_actif
        }

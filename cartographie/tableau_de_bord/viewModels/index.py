#coding: utf-8


class IndexViewModel(object):
    menu_actif = None

    def __init__(self, request, menu_actif=""):
        self.menu_actif = menu_actif

    def get_data(self):
        return {
            "menu_actif": self.menu_actif
        }

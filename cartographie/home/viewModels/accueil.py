#coding: utf-8

from cartographie.home.forms.accueil import AccueilForm


class AccueilViewModel(object):
    terme_recherche = ""
    formations = None
    form = None

    def __init__(self, request, *args, **kwargs):
        self.form = AccueilForm()

    def get_data(self):

        return {
            "form": self.form
        }

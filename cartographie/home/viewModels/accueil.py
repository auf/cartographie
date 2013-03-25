#coding: utf-8

from cartographie.home.forms.accueil import AccueilForm


class AccueilViewModel(object):
    form = AccueilForm()

    def __init__(self, request, *args, **kwargs):
        pass

    def get_data(self):
        return {
            "form": self.form,
        }

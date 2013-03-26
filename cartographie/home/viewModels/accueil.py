#coding: utf-8

from cartographie.home.forms.formation import FormationForm


class AccueilViewModel(object):
    form = FormationForm()

    def __init__(self, request, *args, **kwargs):
        pass

    def get_data(self):
        return {
            "formation_form": self.form,
        }

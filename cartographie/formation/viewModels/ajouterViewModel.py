# coding: utf-8

from ..models import Acces
from ..forms.formation import FormationForm


class AjouterViewModel(object):
    token = None
    etablissement = None
    form = None

    def __init__(self, request, token):
        if token:
            self.token = token
            acces = Acces.objects.filter(token=token)[0]
            self.etablissement = acces.etablissement

            if request.method == "POST":
                form = FormationForm(self.etablissement, request.POST)
            else:
                form = FormationForm(self.etablissement)

            self.form = form

    def get_data(self):
        return {
            "token": self.token,
            "etablissement": self.etablissement,
            "form": self.form
        }

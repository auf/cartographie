# coding: utf-8

from cartographie.formation.models import Acces, Formation
from cartographie.formation.forms.formation import FormationForm


class ModifierViewModel(object):
    token = None
    etablissement = None
    formation = None
    form = None

    def __init__(self, request, token, formation_id):
        if token:
            self.token = token
            acces = Acces.objects.get(token=token)
            self.etablissement = acces.etablissement
            self.formation = Formation.objects.get(id=formation_id)

            if request.method == "POST":
                form = FormationForm(self.etablissement, request.POST)
            else:
                form = FormationForm(
                    self.etablissement,
                    instance=self.formation
                )

            self.form = form

    def get_data(self):
        return {
            "token": self.token,
            "etablissement": self.etablissement,
            "form": self.form,
            "formation": self.formation
        }

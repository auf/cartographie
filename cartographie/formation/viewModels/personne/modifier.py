#coding: utf-8

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.forms.personne import PersonneForm
from cartographie.formation.models import Personne


class ModifierViewModel(BaseAjouterViewModel):
    form = None
    personne = None

    def __init__(self, request, token, personne_id):
        super(ModifierViewModel, self).__init__(request, token)

        self.personne = Personne.objects.get(
            pk=personne_id
        )

        if request.method == "POST":
            form = PersonneForm(
                request.POST, instance=self.personne
            )
        else:
            form = PersonneForm(instance=self.personne)

        self.form = form

    def get_data(self):
        data = super(ModifierViewModel, self).get_data()
        data["personne"] = self.personne
        data["form"] = self.form

        return data

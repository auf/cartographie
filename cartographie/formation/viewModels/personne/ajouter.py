# coding: utf-8

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.forms.personne import PersonneForm


class AjouterViewModel(BaseAjouterViewModel):
    form = None

    def __init__(self, request, token):
        super(AjouterViewModel, self).__init__(request, token)

        if request.method == "POST":
            form = PersonneForm(request.POST)
        else:
            form = PersonneForm()

        self.form = form

    def get_data(self):
        data = super(AjouterViewModel, self).get_data()
        data["form"] = self.form

        return data

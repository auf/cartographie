# coding: utf-8

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.forms.composante import ComposanteForm


class AjouterViewModel(BaseAjouterViewModel):
    form = None

    def __init__(self, request, token):
        super(AjouterViewModel, self).__init__(request, token)

        if request.method == "POST":
            form = ComposanteForm(request.POST)
        else:
            form = ComposanteForm()

        self.form = form

    def get_data(self):
        data = super(AjouterViewModel, self).get_data()
        data["form"] = self.form

        return data

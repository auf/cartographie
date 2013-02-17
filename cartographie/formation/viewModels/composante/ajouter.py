# coding: utf-8

from django.core.urlresolvers import reverse

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.forms.composante import ComposanteForm


class AjouterViewModel(BaseAjouterViewModel):
    form = None
    submit_url = None
    json_request = None

    def __init__(self, request, token, json_request=False):
        super(AjouterViewModel, self).__init__(request, token)

        if request.method == "POST":
            self.form = ComposanteForm(request.POST)
        else:
            self.form = ComposanteForm()

        self.json_request = json_request

        if json_request:
            self.submit_url = reverse(
                "formation_composante_ajouter_popup",
                args=[token]
            )
        else:
            self.submit_url = reverse(
                "formation_composante_ajouter",
                args=[token]
            )

    def get_data(self):
        data = super(AjouterViewModel, self).get_data()
        data["form"] = self.form
        data["submit_url"] = self.submit_url
        data["json_request"] = self.json_request

        return data

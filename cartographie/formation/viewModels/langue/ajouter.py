# coding: utf-8

from django.core.urlresolvers import reverse

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.forms.langue import LangueForm


class AjouterViewModel(BaseAjouterViewModel):
    form = None
    submit_url = None

    def __init__(self, request, token, json_request=False):
        super(AjouterViewModel, self).__init__(request, token)

        if request.method == "POST":
            form = LangueForm(request.POST)
        else:
            form = LangueForm()

        print "AjouterViewModel json_request"
        print json_request

        if json_request:
            self.submit_url = reverse("formation_langue_ajouter_popup", args=[token])
        else:
            self.submit_url = reverse("formation_langue_ajouter", args=[token])

        self.form = form

    def get_data(self):
        data = super(AjouterViewModel, self).get_data()
        data["form"] = self.form
        data["submit_url"] = self.submit_url

        return data

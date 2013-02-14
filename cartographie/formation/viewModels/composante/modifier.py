#coding: utf-8

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.forms.composante import ComposanteForm
from cartographie.formation.models import EtablissementComposante


class ModifierViewModel(BaseAjouterViewModel):
    form = None
    composante = None

    def __init__(self, request, token, composante_id):
        super(ModifierViewModel, self).__init__(request, token)

        self.composante = EtablissementComposante.objects.get(pk=composante_id)

        if request.method == "POST":
            form = ComposanteForm(request.POST, instance=self.composante)
        else:
            form = ComposanteForm(instance=self.composante)

        self.form = form

    def get_data(self):
        data = super(ModifierViewModel, self).get_data()
        data["composante"] = self.composante
        data["form"] = self.form

        return data

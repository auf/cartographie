#coding: utf-8

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.forms.partenaire_autre import PartenaireAutreForm
from cartographie.formation.models import EtablissementAutre


class ModifierViewModel(BaseAjouterViewModel):
    form = None
    partenaire_autre = None

    def __init__(self, request, token, partenaire_autre_id):
        super(ModifierViewModel, self).__init__(request, token)

        self.partenaire_autre = EtablissementAutre.objects.get(
            pk=partenaire_autre_id
        )

        if request.method == "POST":
            form = PartenaireAutreForm(
                request.POST, instance=self.partenaire_autre
            )
        else:
            form = PartenaireAutreForm(instance=self.partenaire_autre)

        self.form = form

    def get_data(self):
        data = super(ModifierViewModel, self).get_data()
        data["partenaire_autre"] = self.partenaire_autre
        data["form"] = self.form

        return data

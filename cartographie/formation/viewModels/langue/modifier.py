#coding: utf-8

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel

from cartographie.formation.forms.langue import LangueForm
from cartographie.formation.models import Langue


class ModifierViewModel(BaseAjouterViewModel):
    form = None
    langue = None

    def __init__(self, request, token, langue_id):
        super(ModifierViewModel, self).__init__(request, token)

        self.langue = Langue.objects.get(
            pk=langue_id
        )

        if request.method == "POST":
            form = LangueForm(request.POST, instance=self.langue)
        else:
            form = LangueForm(instance=self.langue)

        self.form = form

    def get_data(self):
        data = super(ModifierViewModel, self).get_data()
        data["langue"] = self.langue
        data["form"] = self.form

        return data

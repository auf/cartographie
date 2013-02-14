#coding: utf-8

from cartographie.home.forms.accueil import AccueilForm

from cartographie.formation.models import Formation


class AccueilViewModel(object):
    terme_recherche = ""
    formations = None
    form = None

    def __init__(self, request, *args, **kwargs):
        self.form = AccueilForm()

        if request.method == "GET":
            if "s" in request.GET.keys():
                self.terme_recherche = request.GET["s"]
                self.formations = Formation.objects.filter(
                    nom__contains=self.terme_recherche
                )

    def get_data(self):

        return {
            "form": self.form,
            "terme_recherche": self.terme_recherche,
            "formations": self.formations
        }

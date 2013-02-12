# coding: utf-8

from django.forms import ModelForm, Textarea
from cartographie.formation.models import Formation, Personne


class FormationForm(ModelForm):
    class Meta:
        model = Formation
        exclude = ("modifications", "commentaires")

        widgets = {
            "presentation": Textarea(
                attrs={"rows": 5}
            )
        }

    def __init__(self, etablissement, *args, **kwargs):
        super(FormationForm, self).__init__(*args, **kwargs)

        # choisir les personnes et les contacts pour l'établissements courant
        # ref: http://collingrady.wordpress.com/2008/07/24/useful-form-tricks-in-django/
        self.fields["responsables"].queryset = Personne.objects.filter(
            actif=True, etablissement=etablissement
        )
        self.fields["contacts"].queryset = Personne.objects.filter(
            actif=True, etablissement=etablissement
        )
        pass

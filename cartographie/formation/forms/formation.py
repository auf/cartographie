# coding: utf-8

from django.forms import ModelForm, Textarea

from cartographie.formation.models import Formation, FormationCommentaire, Personne


class FormationForm(ModelForm):
    class Meta:
        model = Formation
        exclude = (
            "statut",
            "modifications",
            "commentaires",
            "etablissement_composante",
            "partenaires_auf",
            "partenaires_autres"
        )

        widgets = {
            "presentation": Textarea(
                attrs={"rows": 5}
            )
        }

    def __init__(self, etablissement, afficher_etablissement, *args, **kwargs):
        super(FormationForm, self).__init__(*args, **kwargs)

        # choisir les personnes et les contacts pour l'établissement courant
        # ref: http://collingrady.wordpress.com/2008/07/24/useful-form-tricks-in-django/
        self.fields["responsables"].queryset = Personne.objects.filter(
            actif=True, etablissement=etablissement
        )

        self.fields["contacts"].queryset = Personne.objects.filter(
            actif=True, etablissement=etablissement
        )

        if afficher_etablissement is False:
            del self.fields["etablissement"]
            del self.fields["etablissement_emet_diplome"]


class FormationCommentaireForm(ModelForm):
    class Meta:
        model = FormationCommentaire
        exclude = (
            "formation", "user", "user_display", "date"
        )

        widgets = {
            "commentaire": Textarea(
                attrs={"row": 3}
            )
        }

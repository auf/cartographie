# -*- coding: utf-8 -*-

from django import forms

from cartographie.formation.models import (
    Formation, FormationCommentaire, Personne)


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        exclude = (
            "statut",
            "modifications",
            "commentaires",
            "etablissement_composante",
            "partenaires_auf",
            "partenaires_autres",
            'brouillon',
        )

        widgets = {
            "presentation": forms.Textarea(attrs={"rows": 5})
        }

    def __init__(self, etablissement, afficher_etablissement, *args, **kwargs):
        super(FormationForm, self).__init__(*args, **kwargs)

        self.fields["responsables"].queryset = Personne.objects.filter(
            actif=True, etablissement=etablissement
        )

        self.fields["contacts"].queryset = Personne.objects.filter(
            actif=True, etablissement=etablissement
        )

        if afficher_etablissement is False:
            del self.fields["etablissement"]
            del self.fields["etablissement_emet_diplome"]


class FormationCommentaireForm(forms.ModelForm):
    class Meta:
        model = FormationCommentaire
        exclude = (
            "formation", "user", "user_display", "date"
        )

        widgets = {
            "commentaire": forms.Textarea(attrs={"row": 3})
        }


class CommentaireOptionnelForm(forms.Form):

    commentaire = forms.CharField(max_length=10000, required=False)

    widgets = {
        'commentaire': forms.Textarea(attrs={'row': 3})
    }

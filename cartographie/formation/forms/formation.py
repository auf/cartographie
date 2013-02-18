# coding: utf-8

from django.forms import ModelForm, Textarea

from cartographie.formation.models import Formation, Personne, \
                                            FormationComposante, \
                                            EtablissementComposante


class FormationForm(ModelForm):
    class Meta:
        model = Formation
        exclude = (
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


class FormationComposanteForm(ModelForm):
    class Meta:
        model = FormationComposante

    def __init__(self, *args, **kwargs):
        super(FormationComposanteForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            # limiter le choix des EtablissementComposante à ceux
            # de l'etablissement de l'instance courante de FormationComposante
            self.fields["etablissementComposante"].queryset = \
                EtablissementComposante.objects.filter(
                    etablissement=instance.formation.etablissement, actif=True
                )

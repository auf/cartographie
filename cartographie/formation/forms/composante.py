# coding: utf-8

from django.forms import ModelForm

from cartographie.formation.models import FormationComposante


class ComposanteForm(ModelForm):
    class Meta:
        model = FormationComposante

    def __init__(self, *args, **kwargs):
        super(ComposanteForm, self).__init__(*args, **kwargs)

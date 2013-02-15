# coding: utf-8

from django.forms import ModelForm
from cartographie.formation.models import EtablissementComposante


class ComposanteForm(ModelForm):
    class Meta:
        model = EtablissementComposante

    def __init__(self, *args, **kwargs):
        super(ComposanteForm, self).__init__(*args, **kwargs)
        # si on a des trucs uniques à cette classe à faire ici.

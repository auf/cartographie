# coding: utf-8

from django.forms import ModelForm
from cartographie.formation.models import EtablissementAutre


class PartenaireAutreForm(ModelForm):
    class Meta:
        model = EtablissementAutre

    def __init__(self, *args, **kwargs):
        super(PartenaireAutreForm, self).__init__(*args, **kwargs)
        # si on a des trucs uniques à cette classe à faire ici.

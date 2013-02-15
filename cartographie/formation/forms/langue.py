# coding: utf-8

from django.forms import ModelForm
from cartographie.formation.models import Langue


class LangueForm(ModelForm):
    class Meta:
        model = Langue
        exclude = ("etablissement")

    def __init__(self, *args, **kwargs):
        super(LangueForm, self).__init__(*args, **kwargs)
        # si on a des trucs uniques à cette classe à faire ici.

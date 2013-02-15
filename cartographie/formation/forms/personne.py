# coding: utf-8

from django.forms import ModelForm
from cartographie.formation.models import Personne


class PersonneForm(ModelForm):
    class Meta:
        model = Personne
        exclude = ("etablissement")

    def __init__(self, *args, **kwargs):
        super(PersonneForm, self).__init__(*args, **kwargs)
        # si on a des trucs uniques à cette classe à faire ici.

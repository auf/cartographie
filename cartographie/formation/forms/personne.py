# -*- coding: utf-8 -*-

from django.forms import ModelForm
from cartographie.formation.models import Personne


class PersonneForm(ModelForm):

    class Meta:
        model = Personne
        exclude = ('etablissement', 'actif', 'utilisateur', 'jeton_password')

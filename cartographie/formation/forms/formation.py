# coding: utf-8

from django.forms import ModelForm
from cartographie.formation.models import Formation


class FormationForm(ModelForm):

    class Meta:
        model = Formation
        exclude = ("modifications", "commentaires")

    def __init__(self, *args, **kwargs):
        super(FormationForm, self).__init__(*args, **kwargs)

        # choisir les personnes et les contacts pour l'établissements courant
        pass

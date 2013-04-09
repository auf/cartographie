#coding: utf-8

from django import forms

from auf.django.references import models as ref

from cartographie.formation.models.configuration import NiveauDiplome
from cartographie.formation.models.configuration import Discipline


def form_choices_from_query(q, empty_value_label='', pk_field='pk'):
    initial_list = [('', empty_value_label)] if empty_value_label else []
    return tuple(initial_list + [(getattr(v, pk_field), v) for v in q])


class FormationForm(forms.Form):
    s = forms.CharField(
        max_length=150,
        label=u"Recherchez une formation",
        widget=forms.TextInput(
            attrs={"class": "search-query"}
        ),
        required=False,
    )

    niveau = forms.ChoiceField(\
        choices=form_choices_from_query(NiveauDiplome.objects.all(),
        empty_value_label=u'Tous les diplômes',
        pk_field='nom'),
        required=False,)

    discipline = forms.ChoiceField(\
        choices=form_choices_from_query(Discipline.objects.all(),
        empty_value_label=u'Toutes les disciplines',
        pk_field='code'), required=False)

    region = forms.ChoiceField(\
        choices=form_choices_from_query(ref.Region.objects.all(),
        empty_value_label=u'Toutes les régions'), required=False)

    pays = forms.ChoiceField(\
        choices=form_choices_from_query(ref.Pays.objects.all(),
        empty_value_label=u'Tous les pays'), required=False)

    etablissement = forms.ChoiceField(\
        choices=form_choices_from_query(ref.Etablissement.objects.all(),
        empty_value_label=u'Tous les établissements'), required=False)


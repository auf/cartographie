#coding: utf-8

from django import forms


class FormationForm(forms.Form):
    s = forms.CharField(
        max_length=150,
        label=u"Recherchez une formation",
        widget=forms.TextInput(
            attrs={"class": "search-query"}
        )
    )

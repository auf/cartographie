#coding: utf-8

from django import forms
from django.contrib.auth.models import User


class UserForm(forms.Form):
    users = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("username"),
        label=u"Usager dont le mot de passe sera modifié"
    )

    password = forms.CharField(
        label=u"Mot de passe",
        widget=forms.widgets.PasswordInput
    )

    password_repeat = forms.CharField(
        label=u"Répétez le mot de passe",
        widget=forms.widgets.PasswordInput
    )

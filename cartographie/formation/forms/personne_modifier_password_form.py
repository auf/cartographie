# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class PersonneModifierPasswordForm(forms.Form):

    new_password1 = forms.CharField(label=_('New password'), min_length=8, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_('New password confirmation'), min_length=8, widget=forms.PasswordInput)

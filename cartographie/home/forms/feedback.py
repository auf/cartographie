# coding: utf-8

from django.forms import ModelForm
from cartographie.home.models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback

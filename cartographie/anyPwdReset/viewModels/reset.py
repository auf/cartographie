#coding: utf-8

from django.contrib.auth.models import User
from ..forms import UserForm


class ResetViewModel(object):
    users = []
    form = []

    def __init__(self, request):
        self.users = User.objects.all().order_by("username")

        if request.method == "POST":
            self.form = UserForm(request.POST)
        else:
            self.form = UserForm()

    def get_data(self):
        return {
            "users": self.users,
            "form": self.form
        }

#coding: utf-8

from django import forms
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserForm

from auf.django.permissions.forms import make_global_permissions_form
from auf.django.references import models as ref


class UserForm(DjangoUserForm):

    regions = forms.ModelMultipleChoiceField(
        label=u'Régions',
        queryset=ref.Region.objects.all(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            profile = kwargs['instance'].get_profile()
            profile_data = {'regions': profile.regions.all()}
            initial = kwargs.get('initial')
            if initial:
                profile_data.update(initial)
                kwargs['initial'] = profile_data
        super(UserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=commit)
        old_save_m2m = getattr(self, 'save_m2m', None)

        def save_m2m():
            if old_save_m2m:
                old_save_m2m()
            profile = user.get_profile()
            profile.regions = self.cleaned_data['regions']
            profile.save()

        if commit:
            save_m2m()
        else:
            self.save_m2m = save_m2m
        return user


class UserAdmin(DjangoUserAdmin):
    form = make_global_permissions_form(UserForm)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
        ('Groupes', {'fields': ('groups', 'regions')}),
    )
    list_filter = DjangoUserAdmin.list_filter + ('groups', 'profile__regions')

#coding: utf-8

from django import forms
from django.http import HttpResponseNotAllowed
from django.contrib import messages, admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .formation.models import UserRole


class ModelAdmin(ModelAdmin):
    """
    * Ajout d'une stack pour supprimer l'affichage de l'application dans
        le breadcrumb
    """
    # add_form_template = "admin/custom_change_form.html"
    # change_form_template = "admin/custom_change_form.html"
    # change_list_template = "admin/custom_change_list.html"
    # delete_confirmation_template = (
    #     "admin/custom_delete_confirmation.html")
    # delete_selected_confirmation_template = (
    #     "admin/custom_delete_selected_confirmation.html")
    # object_history_template = "admin/custom_object_history.html"
    pass

PERMISSION_DENIED_MESSAGE = ('Vous n\'avez pas la permission de faire '
                             'cette opération')


class GuardedAdminMixin(object):
    """
    Tous les modèles doivent inclure ce mixin, directement ou
    indirectement, pour que les permissions soient vérifiés.
    """

    ACCEPTED_METHODS = ['POST', 'PUT', 'DELETE', 'GET', 'HEAD', 'OPTIONS']

    def queryset(self, request):
        return self.model.objects.with_perm(request.user, 'manage')

    def __check_read_write(self, request):
        if (request.method in ['POST', 'PUT', 'DELETE']
            and not request.user.has_perm('manage')):
            messages.error(request, PERMISSION_DENIED_MESSAGE)
            raise PermissionDenied()
        elif (request.method in ['GET', 'HEAD', 'OPTIONS']):
            return True

    def __is_methods_ok(self, request):
        if request.method in self.ACCEPTED_METHODS:
            return True
        return False

    def change_view(self,
                    request,
                    object_id,
                    form_url='',
                    extra_context={}):
        self.__check_read_write(request)

        if not self.__is_methods_ok(request):
            return HttpResponseNotAllowed(self.ACCEPTED_METHODS)

        return super(GuardedAdminMixin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context,
            )

    def changelist_view(self,
                    request,
                    extra_context={}):
        self.__check_read_write(request)
        return super(GuardedAdminMixin, self).changelist_view(
            request,
            extra_context,
            )

    def add_view(self,
                    request,
                    form_url='',
                    extra_context={}):
        if (request.method == 'POST'
            and not request.user.has_perm('manage')):
            raise PermissionDenied()
        return super(GuardedAdminMixin, self).add_view(
            request,
            form_url,
            extra_context,
            )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return (request.user.has_perm('manage', obj) or
                request.user.has_perm('lecture_allocataires', obj))

    def has_add_permission(self, request):
        return request.user.has_perm('manage')


# Je crois qu'il est preferable de garder l'ordre des deux mixin comme
# tel, pour s'assurer que super(GuardedAdmin, self)... fasse un call a
# ModelAdmin.<methode>
class GuardedModelAdmin(GuardedAdminMixin, ModelAdmin):
    pass


class GuardedStackedInline(GuardedAdminMixin, StackedInline):
    pass


class GuardedTabularInline(GuardedAdminMixin, TabularInline):
    pass


class UserForm(forms.ModelForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=commit)
        return user


class RoleInline(StackedInline):
    model = UserRole
    extra = 0


class UserAdmin(DjangoUserAdmin, GuardedModelAdmin):
    form = UserForm
    inlines = DjangoUserAdmin.inlines + [RoleInline]
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Informations personnelles', {
            'fields': (
                'first_name', 'last_name', 'email'
            )
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    list_filter = DjangoUserAdmin.list_filter + ('groups',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

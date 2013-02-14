#coding: utf-8

from django import forms
from django.http import HttpResponseNotAllowed
from django.contrib import messages, admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from cartographie.formation.models import *


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


class FormationPartenaireAutreInline(TabularInline):
    model = FormationPartenaireAutre
    extra = 2


class FormationPartenaireAUFInline(TabularInline):
    model = FormationPartenaireAUF
    extra = 2


class FormationComposanteInline(TabularInline):
    model = FormationComposante
    extra = 2


class FormationAdminFieldset(ModelAdmin):
    inlines = [
        FormationComposanteInline,
        FormationPartenaireAUFInline,
        FormationPartenaireAutreInline
    ]

    fieldsets = (
        (u"Identification", {
            "fields": (
                "nom", "nom_origine", "sigle", "url",
                "discipline_1", "discipline_2", "discipline_3"
            )
        }),
        (u"Établissement(s)", {
            "fields": (
                "etablissement",
                "etablissement_emet_diplome",
                # "etablissement_composante",
                # "partenaires_auf",
                # "partenaires_autres"
            )
        }),
        (u"Diplôme", {
            "fields": (
                "niveau_diplome", "type_diplome", "delivrance_diplome",
                "niveau_entree", "niveau_sortie", "vocation"
            )
        }),
        (u"Organisation de la formation", {
            "fields": (
                "presentation", "type_formation", "langue", "duree",
                "responsables", "contacts"
            )
        }),
        (u"Gestion", {
            "fields": (
                "modifications", "commentaires"
            )
        }),
    )
    pass

class AccesAdmin(ModelAdmin):
    list_display = ('_etablissement_id', '_etablissement_nom', '_token', 
                    '_url', '_pays_nom', )
    list_display_links = ('_token',)
    list_filter = (
        'etablissement__region',
        'etablissement__pays',
    )

    search_fields = (
        'etablissement__id',
        'etablissement__nom',
    )
        
    def _get_link(self, href, text):
        link = u"""<a title="Accueil établissement" href='%s'>
                  %s</a>""" % (href, text)
        return link

    def _etablissement_id(self, instance):
        return instance.etablissement.id
    _etablissement_id.short_description = u"Id"
        
    def _etablissement_nom(self, instance):
        return instance.etablissement.nom
    _etablissement_nom.short_description = u"Établissement"
        
    def _token(self, instance):
        if instance.active == True:
            output = instance.token
        elif instance.active == False:
            output =  u"Désactivé"
        else:
            output =  u"Non généré"            
        return output
    _token.short_description = u"Code d'accès"
        
    def _url(self, instance):
        # TODO : virer hardcode domain (basse priorité)
        if instance.active == True :
            href = reverse("formation_liste", args=[instance.token])
            text = "http://cartographie.auf.org%s" % href
            output = self._get_link(href, text)
        elif instance.active == False:
            output =  u"Désactivé"
        else:
            output =  u"Non généré"    
        return output
    _url.allow_tags = True
    _url.short_description = u"URL secrète"
    
    def _pays_nom(self, instance):
        return instance.etablissement.pays.nom
    _pays_nom.short_description = u"Pays"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # True nécessaire pour accès à liste...
        # ... mais URL de modification pas dans liste : voir list_display_links
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    

class DisciplineAdmin(ModelAdmin):
    list_display = ('code', 'nom', '_discipline_auf',)
    list_display_links = ('nom',)
    list_filter = (
        'discipline__nom',
    )

    search_fields = (
        'code',
        'nom',
    )

    def _discipline_auf(self, instance):
        return instance.discipline.nom
    _discipline_auf.short_description = u"Discipline AUF"


class FormationModificationAdmin(ModelAdmin):
    list_display = ('date', 'user', '_formation',)
    list_display_links = ('_formation',)

    search_fields = (
        'formation',
    )       
    
    def _formation(self, instance):
        formation_id = instance.formation.id
        token = instance.formation.etablissement.acces_set.get().token
        
        title = instance.formation
        href = reverse("formation_modifier", args=[token, formation_id])
        text = instance.formation
        link = u"""<a title="%s" href='%s'>
                  %s</a>""" % (title, href, text)
        return link
    _formation.allow_tags = True
    _formation.short_description = u"Formation"
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # True nécessaire pour accès à liste...
        # ... mais URL de modification pas dans liste : voir list_display_links
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Formation, FormationAdminFieldset)
admin.site.register(EtablissementComposante)
admin.site.register(EtablissementAutre)
admin.site.register(Personne)
admin.site.register(Acces, AccesAdmin)

admin.site.register(FormationModification, FormationModificationAdmin)

admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(NiveauDiplome)
admin.site.register(TypeDiplome)
admin.site.register(DelivranceDiplome)
admin.site.register(NiveauUniversitaire)
admin.site.register(Vocation)
admin.site.register(TypeFormation)
admin.site.register(Langue)

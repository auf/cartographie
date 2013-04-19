#coding: utf-8

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from cartographie.home.models import FeedbackProfil, Feedback


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

class FeedbackProfilAdmin(ModelAdmin):
    pass
    
class FeedbackAdmin(ModelAdmin):
    list_display = ('courriel', 'nom', 'prenom', 'date_envoi', 'sujet', )
    list_display_links = ('courriel',)
    list_filter = ('profil',)
    search_fields = ('courriel', 'nom', 'prenom', 'sujet', 'contenu',)

class AccesAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # TODO : corriger ce hack pour que is_staff soit plus suffisant
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(FeedbackProfil, FeedbackProfilAdmin)
admin.site.register(Feedback, FeedbackAdmin)

# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from cartographie.home.models import FeedbackProfil, Feedback


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

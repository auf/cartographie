# coding: utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns(
    "cartographie.formation.views",
    url(r"^(?P<token>\w+)$", "connexion", name="connexion"),
    url(r"^liste$", "liste", name="liste"),
    url(r"^ajouter$", "ajouter", name="ajouter"),
    url(r"^modifier/(?P<formation_id>\d+)$", "modifier", name="modifier"),
    url(r"^erreur$", "erreur", name="erreur")
)

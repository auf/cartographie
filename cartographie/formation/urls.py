# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns("cartographie.formation.views",
    url(r"^erreur$", "erreur", name="formation_erreur"),
    url(r"^(?P<token>\w+)$", "connexion", name="formation_connexion"),
    url(r"^liste$", "liste", name="formation_liste"),
    url(r"^ajouter$", "ajouter", name="formation_ajouter"),
    url(r"^modifier/(?P<formation_id>\d+)$", "modifier", \
        name="formation_modifier"),
)

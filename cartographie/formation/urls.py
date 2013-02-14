# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns(
    "cartographie.formation.views",
    url(
        r"^erreur$",
        "erreur",
        name="formation_erreur"
    ),
    url(
        r"^(?P<token>\w+)$",
        "liste",
        name="formation_liste"
    ),
    url(
        r"^(?P<token>\w+)/formation/ajouter$",
        "ajouter",
        name="formation_ajouter"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)$",
        "consulter",
        name="formation_consulter"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/consulter_etablissements$",
        "consulter_etablissements",
        name="formation_consulter_etablissements"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/modifier$",
        "modifier",
        name="formation_modifier"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/modifier_etablissements$",
        "modifier_etablissements",
        name="formation_modifier_etablissements"
    ),
)

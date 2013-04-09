# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns(
    "cartographie.tableau_de_bord.views",
    url(r"^$", "index", name="dashboard_index"),
    url(
        r"^statistiques$", "statistiques", name="dashboard_statistiques"),
    url(
        r"^etablissements$",
        "liste_etablissements", name="dashboard_liste_etablissements"
    ),
    url(
        r"^modifications$",
        "modifications", name="dashboard_modifications"
    ),
)

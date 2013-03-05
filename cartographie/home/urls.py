# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns(
    "cartographie.home.views",
    url(r"^$", "accueil", name="home_accueil"),

    # interfaces publiques : formation
    url(r"^formations/$", "formation_liste", name="home_formation_liste"),
    url(r"^formations/(?P<id>\d+)$", "formation_detail", name="home_formation_detail"),
)

# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns(
    "cartographie.home.views",
    url(r"^$", "accueil", name="home_accueil"),
    url(r"^formation/$", "formation", name="home_formation"),
)

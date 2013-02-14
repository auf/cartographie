# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns(
    "cartographie.home.views",
    url(r"^$", "accueil", name="home_accueil"),
    url(r"^test$", "test", name="home_test"),
)

# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns(
    "cartographie.tableau_de_bord.views",
    url(r"^$", "index", name="dashboard_index"),
)

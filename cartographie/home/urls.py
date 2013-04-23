# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns(
    "cartographie.home.views",
    url(r"^$", "accueil", name="home_accueil"),
    
    # interfaces publiques
    # header
    url(r"^aide/$", "aide", name="home_aide"),
    url(r"^a-propos/$", "apropos", name="home_a_propos"),
    url(r"^feedback/$", "feedback", name="home_feedback"),
    # navigation
    url(r"^rechercher/$", "rechercher", name="home_rechercher"),
    # footer
    url(r"^legal/$", "legal", name="home_legal"),
    url(r"^contact/$", "contact", name="home_contact"),
    url(r"^credits/$", "credits", name="home_credits"),    

    # interfaces publiques : formation
    url(r"^formations/(?P<id>\d+)$", "formation_detail", name="home_formation_detail"),
    url(r"^geojson/$", "geojson_formations", name="home_geojson_formations"),

    url(r"^fichiers/(?P<fichier_id>\d+)$", "fichiers", name="home_fichiers"),
)

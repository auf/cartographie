# coding: utf-8

from django.conf.urls.defaults import *


urlpatterns = patterns(
    'cartographie.tableau_de_bord.views',
    url(
        r'^$',
        'index',
        name='dashboard_index'
    ),
    url(
        r'^statistiques$',
        'statistiques',
        name='dashboard_statistiques'
    ),
    url(
        r'^etablissements$',
        'liste_etablissements',
        name='dashboard_liste_etablissements'
    ),
    url(
        r'^formations$',
        'liste_formations',
        name='dashboard_liste_formations'
    ),
    url(
        r'^modifications$',
        'modifications',
        name='dashboard_modifications'
    ),
    url(
        r'^administration$',
        'administration',
        name='dashboard_administration'
    ),
    url(
        r'^jetonizer$',
        'jetonizer',
        name='jetonizer'
    ),
)

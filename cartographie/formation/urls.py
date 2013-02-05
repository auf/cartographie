# coding: utf-8

from django.conf.urls.defaults import *

from formation.views import ConnexionView, ErreurView, ListeView, AjouterView, ModifierView

urlpatterns = patterns("",
    url(r"^erreur$", ErreurView.as_view(), name="formation_erreur")
    # url(r"^(?P<token>\w+)$", ConnexionView.as_view(), \
    #     name="formation_connexion"),
    # url(r"^liste$", "liste", name="formation_liste"),
    # url(r"^ajouter$", "ajouter", name="formation_ajouter"),
    # url(r"^modifier/(?P<formation_id>\d+)$", "modifier", \
    #   name="formation_modifier"),
)

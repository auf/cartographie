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
    # ajout/edition des fiches de formation
    url(
        r"^(?P<token>\w+)/formation/ajouter$",
        "ajouter",
        name="formation_ajouter"
    ),
    # url(
    #     r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)$",
    #     "consulter",
    #     name="formation_consulter"
    # ),
    # url(
    #     r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/consulter_etablissements$",
    #     "consulter_etablissements",
    #     name="formation_consulter_etablissements"
    # ),
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
    # ajout/edition des personnes
    url(
        r"^(?P<token>\w+)/personne/liste$",
        "liste_personne",
        name="formation_personne_liste"
    ),
    url(
        r"^(?P<token>\w+)/personne/ajouter$",
        "ajouter_personne",
        name="formation_personne_ajouter"
    ),
    url(
        r"^(?P<token>\w+)/personne/(?P<personne_id>\d+)/modifier$",
        "modifier_personne",
        name="formation_personne_modifier"
    ),
    # ajout/edition des partenaires non membres
    url(
        r"^(?P<token>\w+)/partenaire_autre/liste$",
        "liste_partenaire_autre",
        name="formation_partenaire_autre_liste"
    ),
    url(
        r"^(?P<token>\w+)/partenaire_autre/ajouter$",
        "ajouter_partenaire_autre",
        name="formation_partenaire_autre_ajouter"
    ),
    url(
        r"^(?P<token>\w+)/partenaire_autre/(?P<partenaire_autre_id>\d+)/modifier$",
        "modifier_partenaire_autre",
        name="formation_partenaire_autre_modifier"
    ),
    # ajout/edition des composantes
    url(
        r"^(?P<token>\w+)/composante/liste$",
        "liste_composante",
        name="formation_composante_liste"
    ),
    url(
        r"^(?P<token>\w+)/composante/ajouter$",
        "ajouter_composante",
        name="formation_composante_ajouter"
    ),
    url(
        r"^(?P<token>\w+)/composante/(?P<composante_id>\d+)/modifier$",
        "modifier_composante",
        name="formation_composante_modifier"
    ),
    # ajout/edition des langues
    url(
        r"^(?P<token>\w+)/langue/liste$",
        "liste_langue",
        name="formation_langue_liste"
    ),
    url(
        r"^(?P<token>\w+)/langue/ajouter$",
        "ajouter_langue",
        name="formation_langue_ajouter"
    ),
    url(
        r"^(?P<token>\w+)/langue/(?P<langue_id>\d+)/modifier$",
        "modifier_langue",
        name="formation_langue_modifier"
    ),
)

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
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/consulter$",
        "consulter",
        name="formation_consulter"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/historique$",
        "historique",
        name="formation_historique"
    ),
    url(
        r'^(?P<token>\w+)/formation/(?P<formation_id>\d+)/actualiser$',
        'actualiser',
        name='formation_actualiser'
    ),
    url(
        r'^(?P<token>\w+)/formation/tout_actualiser/(?P<etablissement_id>\d+)$',
        'tout_actualiser',
        name='formation_tout_actualiser'
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
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/commentaires$",
        "modifier_commentaires",
        name="formation_modifier_commentaires"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/modifier_fichiers$",
        "modifier_fichiers",
        name="formation_modifier_fichiers"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/(?P<nouveau_statut>\d+)/commentaires/$",
        "commentaire_avant_changement_statut",
        name="formation_commentaire_avant_changement_statut"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/commentaires/ajouter$",
        "commentaire_ajouter",
        name="commentaire_ajouter"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/commentaires/(?P<commentaire_id>\d+)/modifier$",
        "commentaire_modifier",
        name="commentaire_modifier"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/commentaires/(?P<commentaire_id>\d+)/supprimer$",
        "commentaire_supprimer",
        name="commentaire_supprimer"
    ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/fichiers/(?P<fichier_id>\d+)$",
        "fichiers",
        name="formation_fichiers"
        ),
    url(
        r"^(?P<token>\w+)/formation/(?P<formation_id>\d+)/workflow/(?P<statut_id>\d+)$",
        "modifier_workflow",
        name="formation_modifier_workflow"
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
        r"^(?P<token>\w+)/personne/ajouter_popup$",
        "personne_ajouter_popup",
        name="formation_personne_ajouter_popup"
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
        r"^(?P<token>\w+)/formation/partenaire_autre/ajouter_popup$",
        "ajouter_partenaire_autre_popup",
        name="formation_partenaire_autre_ajouter_popup"
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
        r"^(?P<token>\w+)/composante/ajouter_popup$",
        "ajouter_composante_popup",
        name="formation_composante_ajouter_popup"
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
    url(
        r"^(?P<token>\w+)/langue/ajouter_popup$",
        "ajouter_langue_popup",
        name="formation_langue_ajouter_popup"
    ),
)

# coding: utf-8

from django.template import RequestContext
from django.shortcuts import render_to_response

from .decorators import token_required


def erreur(request):
    """
    Page d'erreur lorsque le token fait défaut
    """
    return render_to_response(
        "erreur.html", {}, RequestContext(request)
    )


@token_required
def liste(request, token):
    """
        Afficher la liste de formation pour l'utilisateur courant
    """

    from .viewModels.listeViewModel import ListeViewModel

    return render_to_response(
        "liste.html",
        ListeViewModel(token).get_data(),
        RequestContext(request)
    )


@token_required
def ajouter(request, token):
    """
        Formulaire d'ajout d'une fiche formation
    """

    from .viewModels.ajouterViewModel import AjouterViewModel

    return render_to_response(
        "ajouter.html",
        AjouterViewModel(token).get_data(),
        RequestContext(request)
    )


@token_required
def consulter(request, token, formation_id=None):
    """
        Voir la fiche formation sans modification possible
    """

    return render_to_response(
        "consulter.html", {}, RequestContext(request)
    )


@token_required
def modifier(request, token, formation_id=None):
    """
        Formulaire d'édition d'une fiche formation
    """
    return render_to_response(
        "modifier.html", {}, RequestContext(request)
    )

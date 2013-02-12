# coding: utf-8

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from cartographie.formation.decorators import token_required


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

    from cartographie.formation.viewModels.listeViewModel import ListeViewModel

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

    from cartographie.formation.viewModels.ajouterViewModel import AjouterViewModel

    # AjouterViewModel fait la vérification du POST avec le formulaire
    # VM = ViewModel :)
    ajoutVM = AjouterViewModel(request, token)

    if ajoutVM.form.is_valid():
        # pour gérer les m2m, on doit utiliser commit=False
        # pour sauvegarder le modele de base AVANT de faire des save m2m.
        nouvelle_formation = ajoutVM.form.save(commit=False)
        nouvelle_formation.save()

        # sauvegarder des m2m avec through:
        #   EtablissementComposante, ref.Etablissement, EtablissementAutre

        # puis sauvegarder les m2m normaux
        ajoutVM.form.save_m2m()

        return HttpResponseRedirect(
            reverse("formation_liste", args=[token])
        )

    data = ajoutVM.get_data()

    return render_to_response(
        "ajouter.html",
        data,
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

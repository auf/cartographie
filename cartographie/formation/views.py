# coding: utf-8
# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

# from auf.django.references import models as ref
from formation import models
from formation.constants import session_const
from formation.decorators import token_required


def connexion(request, token):
    try:
        # obtention d'un etablissement à partir de la valeur du token
        etab = models.Acces.objects.select_related(
            'etablissement'
        ).get(
            token=token
        )

        if len(etab) != 0:
            # tout est beau. on crée une variable session et hop
            # dans la liste des fiches formations !
            request.session[session_const.eta_id] = etab.etablissement_id
            return redirect('formation_liste')

        return redirect("formation_erreur")

    except ObjectDoesNotExist:
        request.session[session_const.erreur] = True
        return redirect('formation_erreur')


def erreur(request):
    """
    Page d'erreur lorsque le token fait défaut
    """
    return render_to_response(
        "erreur.html", {}, RequestContext(request)
    )

    pass


@token_required
def liste(request):
    """
        Afficher la liste de formation pour l'utilisateur courant
    """
    return render_to_response(
        "liste.html", {}, RequestContext(request)
    )

    pass


@token_required
def ajouter(request):
    """
        Formulaire d'ajout d'une fiche formation
    """
    return render_to_response(
        "ajouter.html", {}, RequestContext(request)
    )

    pass


@token_required
def modifier(request, formation_id=None):
    """
        Formulaire d'édition d'une fiche formation
    """
    return render_to_response(
        "modifier.html", {}, RequestContext(request)
    )

    pass

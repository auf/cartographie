# coding: utf-8
# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.forms.models import modelformset_factory
from django.forms.models import model_to_dict

from auf.django.references import models as ref
from formation import models


def connexion(request, token):
    try:
        return verifier_token(request, token)
    except ObjectDoesNotExist:
        request.session['espace_membre_erreur'] = True
        return redirect('espace_membre_accueil')
    pass


def verifier_token(request, token):
    """
    Vérifie si le token est valide et redirige l'usager à la liste
    des fiches formations
    """

    token = models.Acces.objects.select_related('etablissement').get(token=token)

    if len(token) != 0:
        request.session['espace_membre_etablissement'] = token.etablissement_id
        return redirect('liste')

    return redirect("erreur")


def erreur(request):
    """
    Page d'erreur lorsque le token fait défaut
    """
    pass


def liste(request):
    """
        Afficher la liste de formation pour l'utilisateur courant
    """

    pass


def ajouter(request):
    """
        Formulaire d'ajout d'une fiche formation
    """
    pass


def modifier(request, formation_id=None):
    """
        Formulaire d'édition d'une fiche formation
    """

    pass

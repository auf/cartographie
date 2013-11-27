# -*- coding: utf-8 -*-

from functools import wraps

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist


from . import models


def token_required(wrapped_func):
    """
        Décorateur pour vérifier la présence du token
        pour permettre de continuer à utiliser l'app
    """

    @wraps(wrapped_func)
    def inner_decorator(request, *args, **kwargs):

        token = kwargs.get("token", False)

        etab = None


        # Passe par Acces pour obtenir l'établissement
        try:
            acces = models.Acces.objects.select_related(
                'etablissement'
            ).get(
                token=token
            )

        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('formation_erreur'))


        # On passe "manuellement" au CartoEtablissement pour contourner
        # les problèmes d'imports circulaires.
        etab = models.CartoEtablissement.objects.get(pk=acces.etablissement.pk)

        if not etab:
            return HttpResponseRedirect(reverse('formation_erreur'))

        if etab.has_referent():
            if not request.user.is_authenticated() \
                    or not etab.peut_consulter(request.user):
                return HttpResponseRedirect(reverse('formation_erreur'))


        if 'formation_id' in kwargs:
            formation_id = kwargs['formation_id']
            try:
                formation = models.Formation.objects.get(pk=formation_id)
                if formation.etablissement != etab:
                    return HttpResponseRedirect(reverse('formation_erreur'))
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('formation_erreur'))
        return wrapped_func(request, *args, **kwargs)

    return inner_decorator


def editor_of_region_required(wrapped_func):
    """
        Décorateur qui vérifie si l'utilisateur est un éditeur
        de la région
    """

    @wraps(wrapped_func)
    def inner_decorator(request, *args, **kwargs):
        token = kwargs.get("token", False)

        # obtention d'un etablissement à partir de la valeur du token
        etab = models.Acces.etablissement_for_token(token)

        if etab and request.user and\
          models.UserRole.is_editeur_etablissement(request.user, etab) or\
          request.user.is_superuser:
            return wrapped_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('formation_erreur'))

    return inner_decorator

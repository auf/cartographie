#coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from functools import wraps


def token_required(permission):
    """
    Décorateur pour vérifier l'existence d'une variable de session
    pour permettre de continuer à utiliser l'app
    """

    def decorator(func):
        def inner_decorator(request, *args, **kwargs):

            if "espace_formation_etablissement_id" in request.session.keys():
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('formation_erreur'))

        return wraps(func)(inner_decorator)

    return decorator

#coding: utf-8

from functools import wraps

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from formation.constants import session_const


def token_required(f):
    """
    Décorateur pour vérifier l'existence d'une variable de session
    pour permettre de continuer à utiliser l'app
    """

    @wraps(f)
    def inner_decorator(request, *args, **kwargs):
        if session_const.eta_id in request.session.keys():
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('formation_erreur'))

    return inner_decorator

#coding: utf-8

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

        # obtention d'un etablissement à partir de la valeur du token
        try:
            acces = models.Acces.objects.select_related(
                'etablissement'
            ).get(
                token=token
            )
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('formation_erreur'))

        etab = acces.etablissement

        if etab:
            return wrapped_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('formation_erreur'))

    return inner_decorator

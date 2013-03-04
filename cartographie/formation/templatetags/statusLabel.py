#coding: utf-8

from django import template
from cartographie.formation.models.workflow import ETATS

register = template.Library()


@register.filter
def statusLabel(value):
    """
        Obtient l'étiquette pour un statut numérique d'une fiche
        formation en utilisant le tableau que je donne en paramètre
        choice du abstract model WorkflowMixin
    """
    labels = filter(lambda x: x[0] == int(value), ETATS)

    if len(labels) == 1:
        lbl = labels.pop()

        return lbl[1]

    return ""

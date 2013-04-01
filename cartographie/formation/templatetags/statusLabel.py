#coding: utf-8

from django import template
from cartographie.formation.models.workflow import statusIdToStatusLabel

register = template.Library()


@register.filter
def statusLabel(value):
    """
        Obtient l'étiquette pour un statut numérique d'une fiche
        formation en utilisant le tableau que je donne en paramètre
        choice du abstract model WorkflowMixin
    """
    return statusIdToStatusLabel(value)

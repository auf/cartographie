#coding: utf-8

from django import template
from cartographie.formation.models.workflow import statusIdToStatusLabel
from cartographie.formation.constants import statuts_formation as STATUTS

register = template.Library()


@register.filter
def statusLabel(value):
    """
        Obtient l'étiquette pour un statut numérique d'une fiche
        formation en utilisant le tableau que je donne en paramètre
        choice du abstract model WorkflowMixin
    """
    return statusIdToStatusLabel(value)

@register.filter
def statusClass(value):
    """
        Optient la classe css qui doit être associée à un statut numérique
    """
    if value == STATUTS.publiee:
        return 'label-success'
    if value == STATUTS.supprimee:
        return 'label-important'
    if value == STATUTS.en_redaction:
        return ''
    if value == STATUTS.validee:
        return 'label-info'
    return ''


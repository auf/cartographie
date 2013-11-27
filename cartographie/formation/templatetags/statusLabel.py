# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django import template

from cartographie.formation.constants import statuts_formation as STATUTS
from cartographie.formation.models.workflow import statusIdToStatusLabel

register = template.Library()


@register.filter
def statusLabel(value):
    """Obtient l'étiquette pour un statut numérique d'une fiche formation en
    utilisant le tableau que je donne en paramètre choice du abstract model
    WorkflowMixin"""

    return statusIdToStatusLabel(value)


@register.filter
def statusClass(value):
    """Obtient la classe CSS qui doit être associée à un statut numérique"""

    if value == STATUTS.publiee:
        return 'label-success'
    if value == STATUTS.supprimee:
        return 'label-important'
    if value == STATUTS.en_redaction:
        return ''
    if value == STATUTS.validee:
        return 'label-info'
    return ''


@register.filter
def expired(formation):
    year_ago = datetime.now() - timedelta(days=365)

    return formation.date_modification <= year_ago

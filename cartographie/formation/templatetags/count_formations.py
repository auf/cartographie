#coding: utf-8

from datetime import datetime, timedelta

from django import template


from cartographie.formation.models import UserRole, Formation
from cartographie.formation.models.workflow import statusIdToStatusLabel
from cartographie.formation.constants import statuts_formation as STATUTS

register = template.Library()

@register.filter
def count_formations(etablissement):
    """
    """
    count = Formation.objects.exclude(statut=999)\
                             .exclude(brouillon__isnull=False)\
                             .filter(etablissement=etablissement).count()
    return count

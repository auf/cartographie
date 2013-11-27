#coding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from cartographie.formation.models import Acces, Formation, FormationModification, UserRole
from collections import namedtuple

class ModificationsViewModel(object):
    menu_actif = None
    user_sans_region = False
    recent_modifications = None

    def __init__(self, request, menu_actif="modifications"):
        self.menu_actif = menu_actif

        roles = UserRole.get_toutes_regions(request.user)
        if roles:
            formations = Formation.objects.filter(etablissement__region__in=roles)
            self.recent_modifications \
                = FormationModification.objects.filter(formation__in=formations) \
                .order_by("-date")[:100]
        else:
            self.user_sans_region = True

    def get_data(self):
        return {
            "menu_actif": self.menu_actif,
            "user_sans_region": self.user_sans_region,
            "recent_modifications": self.recent_modifications,
        }


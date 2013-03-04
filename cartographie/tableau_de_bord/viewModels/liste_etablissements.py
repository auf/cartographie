#coding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from cartographie.formation.models import UserRole, Acces


class ListeEtablissementsViewModel(object):
    menu_actif = None
    liste_acces = None
    user_sans_region = False

    def __init__(self, request, menu_actif="liste_etablissements"):
        self.menu_actif = menu_actif

        try:
            role = UserRole.objects.get(user=request.user)
        except ObjectDoesNotExist:
            role = None
            self.user_sans_region = True

        if role:
            self.liste_acces = Acces.objects.filter(
                etablissement__region__in=role.regions.all()
            ).order_by("etablissement__nom")

    def get_data(self):
        return {
            "menu_actif": self.menu_actif,
            "liste_acces": self.liste_acces,
            "user_sans_region": self.user_sans_region
        }

#coding: utf-8

from cartographie.formation.models import UserRole, Acces


class ListeEtablissementsViewModel(object):
    menu_actif = None
    liste_acces = None

    def __init__(self, request, menu_actif="liste_etablissements"):
        self.menu_actif = menu_actif

        role = UserRole.objects.get(user=request.user)

        self.liste_acces = Acces.objects.filter(
            etablissement__region__in=role.regions.all()
        ).order_by("etablissement__nom")

    def get_data(self):
        return {
            "menu_actif": self.menu_actif,
            "liste_acces": self.liste_acces
        }

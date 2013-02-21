#coding: utf-8
from django.db.models import Count
from cartographie.formation.models import Formation, UserRole


class StatistiquesViewModel(object):
    menu_actif = None
    # nombre total de formations dans le système
    total_nb_formations = 0
    # nombre total de formation par région dans le système
    totaux_par_regions = []
    # nombre total de formation par pays dans le système
    totaux_par_pays = []
    # nombre total de formation par établissement pour les pays sous la gestion de
    # l'utilisateur connecté courant
    totaux_par_etablissements = []

    def __init__(self, request, menu_actif="statistiques"):
        self.menu_actif = menu_actif

        self.total_nb_formations = Formation.objects.all().count()

        self.totaux_par_regions = Formation.objects.values(
            "etablissement__region__nom"
        ).annotate(total=Count("id")).order_by("-total")

        self.totaux_par_pays = Formation.objects.values(
            "etablissement__pays__nom"
        ).annotate(total=Count("id")).order_by("-total")

        role = UserRole.objects.get(user=request.user)

        self.totaux_par_etablissements = Formation.objects.filter(
            etablissement__region__in=role.regions.all()
        ).values("etablissement__nom").annotate(
            total=Count("id")
        ).order_by("-total")

        print self.totaux_par_etablissements

    def get_data(self):
        return {
            "menu_actif": self.menu_actif,
            "total_nb_formations": self.total_nb_formations,
            "totaux_par_regions": self.totaux_par_regions,
            "totaux_par_pays": self.totaux_par_pays,
            "totaux_par_etablissements": self.totaux_par_etablissements
        }

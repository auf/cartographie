#coding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from cartographie.formation.models import Formation, UserRole


class StatistiquesViewModel(object):
    menu_actif = None
    user_sans_region = False
    # nombre total de formations dans le système
    total_nb_formations = 0
    # nombre total de formation sous la gestion du user courant
    total_nb_formations_sous_gestion = 0
    # nombre total de formation par région dans le système
    totaux_par_regions = []
    # nombre total de formation par pays dans le système
    totaux_par_pays = []
    # nombre total de formation par établissement pour les pays sous la gestion de
    # l'utilisateur connecté courant
    totaux_par_etablissements = []

    # nombre de formation par statut
    totaux_par_statut = []

    def __init__(self, request, menu_actif="statistiques"):
        self.menu_actif = menu_actif

        self.total_nb_formations = Formation.objects.all().count()

        self.totaux_par_regions = Formation.objects.values(
            "etablissement__region__nom"
        ).annotate(total=Count("id")).order_by("-total")

        self.totaux_par_pays = Formation.objects.values(
            "etablissement__pays__nom"
        ).annotate(total=Count("id")).order_by("-total")

        try:
            role = UserRole.objects.get(user=request.user)
        except ObjectDoesNotExist:
            role = None
            self.user_sans_region = True

        if role:
            self.total_nb_formations_sous_gestion = Formation.objects.filter(
                etablissement__region__in=role.regions.all()
            ).count()

            self.totaux_par_etablissements = Formation.objects.filter(
                etablissement__region__in=role.regions.all()
            ).values("etablissement__nom").annotate(
                total=Count("id")
            ).order_by("-total")

            self.totaux_par_statut = Formation.objects.filter(
                etablissement__region__in=role.regions.all()
            ).values("statut").annotate(
                total=Count("id")
            ).order_by("-total")

    def get_data(self):
        return {
            "menu_actif": self.menu_actif,
            "total_nb_formations": self.total_nb_formations,
            "total_nb_formations_sous_gestion": self.total_nb_formations_sous_gestion,
            "totaux_par_regions": self.totaux_par_regions,
            "totaux_par_pays": self.totaux_par_pays,
            "totaux_par_etablissements": self.totaux_par_etablissements,
            "totaux_par_statut": self.totaux_par_statut,
            "user_sans_region": self.user_sans_region
        }

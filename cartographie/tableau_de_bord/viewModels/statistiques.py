# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from auf.django.references import models as ref
from cartographie.formation.models import (
    Formation, FormationModification, UserRole)


class StatistiquesViewModel(object):
    menu_actif = None
    user_sans_region = False

    # Nombre total de formations dans le système
    total_nb_formations = 0

    # Nombre total de formation sous la gestion du user courant
    total_nb_formations_sous_gestion = 0

    # Nombre total de formation par région dans le système
    totaux_par_regions = []

    # Nombre total de formation par pays dans le système
    totaux_par_pays = []

    # Nombre total de formation par établissement pour les pays sous la gestion
    # de l'utilisateur connecté courant
    totaux_par_etablissements = []

    # nombre de formation par statut
    totaux_par_statut = []

    recent_modifications = None

    def __init__(self, request, menu_actif="statistiques"):
        self.menu_actif = menu_actif

        self.total_nb_formations = Formation.objects.exclude(
            statut=999).count()

        self.totaux_par_regions = Formation.objects.exclude(
            statut=999).values("etablissement__region__nom").annotate(
            total=Count("id")).order_by("-total")

        self.totaux_par_pays = Formation.objects.exclude(
            statut=999).values("etablissement__pays__nom").annotate(
            total=Count("id")).order_by("-total")

        regions = UserRole.get_toutes_regions(request.user)

        if regions:
            self.formations = Formation.objects.exclude(
                statut=999).filter(etablissement__region__in=regions)

            self.recent_modifications = FormationModification.objects.filter(
                formation__in=self.formations).order_by("-date")[:25]

            self.total_nb_formations_sous_gestion = self.formations.count()

            self.totaux_par_etablissements = Formation.objects.exclude(
                statut=999).filter(etablissement__region__in=regions).values(
                "etablissement__nom").annotate(total=Count("id")).order_by(
                "-total")

            self.totaux_par_statut = Formation.objects.exclude(
                statut=999).filter(etablissement__region__in=regions).values(
                "statut").annotate(total=Count("id")).order_by("-total")
        else:
            self.user_sans_region = True

    def get_data(self):
        return {
            "menu_actif": self.menu_actif,
            "total_nb_formations": self.total_nb_formations,
            "total_nb_formations_sous_gestion": (
                self.total_nb_formations_sous_gestion),
            "totaux_par_regions": self.totaux_par_regions,
            "totaux_par_pays": self.totaux_par_pays,
            "totaux_par_etablissements": self.totaux_par_etablissements,
            "totaux_par_statut": self.totaux_par_statut,
            "user_sans_region": self.user_sans_region,
            "recent_modifications": self.recent_modifications,
        }

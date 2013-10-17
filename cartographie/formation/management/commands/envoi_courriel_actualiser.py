#coding: utf-8

import csv, os, sys

from django.core.management.base import BaseCommand
from formation.models import EtablissementComposante, Formation

from datetime import datetime, timedelta

from collections import defaultdict

class Command(BaseCommand):
    help = u"""
        Fais un import de base dans les models de configuration
    """

    def handle(self, *args, **options):

        def get_formations_exp_in_n_days(n_days):
            today = datetime.now()
            n_days_ago = today + timedelta(days=-(365 - n_days))
            print n_days_ago
            expire_in_n_days = Formation.objects.filter(date_modification__lte=n_days_ago)
            print expire_in_n_days
            return expire_in_n_days

        def index_by_etablissement(formations):
            etab = defaultdict(list)
            for f in formations:
                etab[f.etablissement] = f
            return etab

        def envoi_courriel(etab_formations):
            print etab_formations

        expire_in_days = (15, 30, 45,)
        all_expirations = {}

        for day in expire_in_days:
            formations = get_formations_exp_in_n_days(day)
            etab_formations = index_by_etablissement(formations)
            all_expirations[day] = etab_formations

        import ipdb; ipdb.set_trace()


        # Ensemble des établissements ayant une formation qui expire et ce,
        # peu importe quand
        all_etablissements = set([e for values in all_expirations.values()
                                    for e in values])

        for etab in all_etablissements:
            etab_email = {}
            for day in expire_in_days:
                etab_email[day] = all_expirations[day][etab]
            print etab_email

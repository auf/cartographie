#coding: utf-8
from datetime import datetime, timedelta
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.template import Template, Context

from formation.models import Formation, CourrielRappel

class Command(BaseCommand):
    help = u"""
        Fais un import de base dans les models de configuration
    """

    def handle(self, *args, **options):

        def get_formations_exp_in_n_days(n_days):
            today = datetime.now()
            n_days_ago = today + timedelta(days=-(365 - n_days))
            n_days_ago_p1 = today + timedelta(days=-(365 - n_days + 1))
            print n_days_ago
            print expire_in_n_days
            expire_in_n_days = Formation.objects.filter(date_modification__lte=n_days_ago,
                                                        date_modification__gte=n_days_ago_p1)
            return expire_in_n_days

        def index_by_etablissement(formations):
            etab = defaultdict(list)
            for f in formations:
                etab[f.etablissement].append(f)
            return etab

        def envoi_courriel(etab_formations):
            contexte = {}
            print etab_formations
            for day in etab_formations.keys():
                contexte['expiration_%s_jours' % day] = etab_formations[day]
            t = Template(courriel.template)

        courriel = CourrielRappel.objects.filter(actif=True)[0]

        expire_in_days = [int(d) for d in courriel.periode.split(',')]
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
            envoi_courriel(etab_email)
            print etab_email

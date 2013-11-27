#coding: utf-8
from datetime import datetime, timedelta
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.template import Template, Context

from formation.models import Formation, CourrielRappel
from django.core.mail import send_mail

from cartographie.formation.models.formation import EnveloppeParams


class Command(BaseCommand):
    help = u"""
        Fais un import de base dans les models de configuration
    """

    def handle(self, *args, **options):

        def index_by_etablissement(formations):
            etab = defaultdict(list)
            for f in formations:
                etab[f.etablissement].append(f)
            return etab

        def envoi_courriel(etab_formations):
            contexte = {}
            for day in etab_formations.keys():
                contexte['expiration_%s_jours' % day] = etab_formations[day]
            t = Template(courriel.corps)
            etab = etab_formations['etab']
            to_string = "%s %s <%s>" % (etab.responsable_prenom,
                                        etab.responsable_nom,
                                        etab.responsable_courriel)
            send_mail(courriel.sujet, t.render(Context(contexte)), 'test@cartographie.auf.org', [to_string])

        courriels = CourrielRappel.objects.filter(actif=True)

        for courriel in courriels:

            expire_in_days = [int(d) for d in courriel.periode.split(',')]
            all_expirations = {}

            for day in expire_in_days:
                formations = Formation.expire_dans_n_jours(day)
                etab_formations = index_by_etablissement(formations)
                all_expirations[day] = etab_formations

            # Ensemble des établissements ayant une formation qui expire et ce,
            # peu importe quand
            all_etablissements = set([e for values in all_expirations.values()
                                  for e in values])

            for etab in all_etablissements:
                etab_email = {}
                etab_email['etab'] = etab
                for day in expire_in_days:
                    etab_email[day] = all_expirations[day][etab]
                    envoi_courriel(etab_email)

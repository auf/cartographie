#coding: utf-8


from   auf.django.references import models as ref
from   django.core.management.base import BaseCommand
from   django.db.models import Count
from   formation.models import Formation
import json
import sys

class Command(BaseCommand):
    
    def handle(self, filename, **kwargs):
        data = json.load(open(filename))
        country2num_formations = Command.num_formations_per_country()

        for country_data in data['features']:
            code = country_data['id'].lower()

            country_data['auf_membre'] = code in country2num_formations
            country_data['auf_nb_formations'] = country2num_formations.get(code, 0)

        json.dump(data, sys.stdout)

    @staticmethod
    def num_formations_per_country():

        def result2pair(result):
            return result['etablissement__pays__code_iso3'].lower(), result['count']

        # On doit passer par Formation.objects parce que
        # 'related_name' = '+' dans EtablissementBase pour la colonne
        # 'pays'.

        query = Formation.objects.values('etablissement__pays__code_iso3')\
            .annotate(count=Count('etablissement__pays__code_iso3'))

        return dict(map(result2pair, query))

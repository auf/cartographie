#coding: utf-8

# Usage:
# ./bin/django update_dbf data/world_merc.dbf

from    __future__ import print_function
from   .. import dbf
from   auf.django.references.models import Etablissement
from   django.core.management.base import BaseCommand
from   django.db.models import Count
from   formation.models import Formation
import json
import sys


class Command(BaseCommand):
    
    def handle(self, filename, **kwargs):
        print("Using '%s'... " % filename, end='')

        country2num_formations = Command.num_formations_per_country()
        country2num_etablissements = Command.num_etablissements_per_country()

        table = dbf.Table(filename)
        table.open()

        for record in dbf.Process(table):
            code = record.iso3.lower()

            record.forma = country2num_formations.get(code, 0)
            record.etab = country2num_etablissements.get(code, 0)

        table.close()
        print("Done")

    @staticmethod
    def num_etablissements_per_country():

        def result2pair(result):
            return result['pays__code_iso3'].lower(), result['count']

        query = Etablissement.objects.values('pays__code_iso3')\
            .annotate(count=Count('pays__code_iso3'))

        return dict(map(result2pair, query))

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

 

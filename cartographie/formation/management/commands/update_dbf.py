#coding: utf-8

# Usage:
# ./bin/django update_dbf data/world_merc.dbf

from  __future__ import print_function
from .. import dbf
from django.core.management.base import BaseCommand
from formation.stats import (num_etablissements_per_country,
                             num_formations_per_country)


class Command(BaseCommand):

    def handle(self, filename, **kwargs):
        print("Using '%s'... " % filename, end='')

        country2num_formations = num_formations_per_country()
        country2num_etablissements = num_etablissements_per_country()

        table = dbf.Table(filename)
        table.open()

        for record in dbf.Process(table):
            code = record.iso3.lower()

            record.forma = country2num_formations.get(code, 0)
            record.etab = country2num_etablissements.get(code, 0)

        table.close()
        print("Done")

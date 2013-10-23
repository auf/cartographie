from __future__ import print_function
from auf.django.references.models import Etablissement
from django.db.models import Count
from formation.models import Formation


def num_etablissements_per_country():
    def result2pair(result):
        return result['pays__code_iso3'].lower(), result['count']

    query = Etablissement.objects.values('pays__code_iso3')\
        .exclude(formation__isnull=True)\
        .annotate(count=Count('pays__code_iso3'))

    return dict(map(result2pair, query))


def num_formations_per_country():
    def result2pair(result):
        return (result['etablissement__pays__code_iso3'].lower(),
                result['count'])

    # On doit passer par Formation.objects parce que
    # 'related_name' = '+' dans EtablissementBase pour la colonne
    # 'pays'.

    query = Formation.objects.values('etablissement__pays__code_iso3')\
        .exclude(statut=999)\
        .annotate(count=Count('etablissement__pays__code_iso3'))

    return dict(map(result2pair, query))

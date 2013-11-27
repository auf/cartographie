#coding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from cartographie.formation.models import UserRole, Acces
from collections import namedtuple

Column = namedtuple('Column', ['sort_name', 'sort_function', 'name'])

def make_sort_by_column(column):
    def sort_by_column(acces, asc):
        prefix = '' if asc else '-'
        return acces.order_by(prefix + column)
    return sort_by_column

def sort_by_formation_count(acces, asc):
    prefix = '' if asc else '-'
    return acces.annotate(Count('etablissement__formation')). \
        order_by(prefix + 'etablissement__formation__count')

class ListeEtablissementsViewModel(object):
    columns = map(lambda args: Column(*args),
                  [('region', make_sort_by_column('etablissement__region'), 
                    'Région'),
                   ('pays', make_sort_by_column('etablissement__pays'), 'Pays'),
                   ('nom', make_sort_by_column('etablissement__nom'), 'Nom'),
                   ('formations', sort_by_formation_count, 'Formations'),
                   (None, None, 'Consulter')])

    sort_name2sort_function = dict((col.sort_name, col.sort_function)
                                   for col in columns)

    menu_actif = None
    liste_acces = None
    user_sans_region = False
    sort = None

    def __init__(self, request, menu_actif="liste_etablissements"):
        self.menu_actif = menu_actif

        regions = UserRole.get_toutes_regions(request.user)
        if regions:
            self.liste_acces = Acces.objects.filter(
                etablissement__region__in=regions)
            self._sort(request.GET.get('tri'))
        else:
            self.user_sans_region = True

    def get_data(self):
        return {
            "menu_actif": self.menu_actif,
            "liste_acces": self.liste_acces,
            "user_sans_region": self.user_sans_region,
            "sort": self.sort,
            "columns": ListeEtablissementsViewModel.columns,
        }

    def _sort(self, sort):
        if sort and sort.strip('-') in \
                ListeEtablissementsViewModel.sort_name2sort_function:
            asc = sort[0] != '-'
            sort_name = sort.strip('-')
            prefix = '' if asc else '-'
            self.sort = { 'asc': asc,
                          'name': sort_name, 
                          'string': prefix + sort_name }
            self.liste_acces = ListeEtablissementsViewModel.\
                sort_name2sort_function[sort_name](self.liste_acces, asc)
        else:
            self.liste_acces.order_by("etablissement__region",
                                      "etablissement__pays",
                                      "etablissement__nom")

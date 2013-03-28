#coding: utf-8

from cartographie.formation.models import Formation
from cartographie.home.forms.formation import FormationForm
from collections import namedtuple
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

Column = namedtuple('Column', ['sort_name', 'sort_column', 'name'])

class FormationListeViewModel(object):
    NUM_FORMATIONS_PER_PAGE = 25
    columns = map(lambda args: Column(*args),
                  [('nom', 'nom', 'Nom'),
                   ('niveau', 'niveau_diplome', 'Niveau'),
                   ('discipline', 'discipline_1__nom', 'Discipline(s)'),
                   ('etablissement', 'etablissement__nom', 'Établissement'),
                   ('pays', 'etablissement__pays__nom', 'Pays'),
                   ('region', 'etablissement__region__nom', 'Région')])

    sort_name2sort_column = dict((col.sort_name, col.sort_column) 
                                 for col in columns)
                             
    def __init__(self, request, *args, **kwargs):
        self.form = FormationForm()
        self.formations = Formation.objects.all()
        self.terme_recherche = None
        self.sort = None

        self._filter(request.GET.get('s'))
        self._sort(request.GET.get('tri'))
        self._paginate(request)

    def get_data(self):
        return {
            "formation_form": self.form,
            "terme_recherche": self.terme_recherche,
            "formations": self.formations,
            "tri": self.sort,
            "columns": FormationListeViewModel.columns
        }

    def _filter(self, query):
        if not query:
            return

        self.terme_recherche = query
        self.form.initial['s'] = self.terme_recherche
        self.formations = Formation.objects.filter(
            Q(nom__icontains=self.terme_recherche) | 
            Q(discipline_1__nom__icontains=self.terme_recherche) |
            Q(discipline_2__nom__icontains=self.terme_recherche) |
            Q(discipline_3__nom__icontains=self.terme_recherche) |
            Q(etablissement__nom__icontains=self.terme_recherche) |
            Q(etablissement__region__nom__icontains=self.terme_recherche) |
            Q(etablissement__pays__nom__icontains=self.terme_recherche) |
            Q(niveau_diplome__nom__icontains=self.terme_recherche)
            )

    def _paginate(self, request):
        paginator = Paginator(self.formations, 
                              FormationListeViewModel.NUM_FORMATIONS_PER_PAGE)

        page = request.GET.get('page')

        try:
            self.formations = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            self.formations = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999)
            self.formations = paginator.page(paginator.num_pages)

    def _sort(self, sort):
        if sort and sort.strip('-') in \
                FormationListeViewModel.sort_name2sort_column:
            asc = sort[0] != '-'
            sort_name = sort.strip('-')
            prefix = '' if asc else '-'
            self.sort = { 'asc': asc,
                          'name': sort_name, 
                          'string': prefix + sort_name }
            self.formations = self.formations.order_by(
                prefix + FormationListeViewModel.
                sort_name2sort_column[sort_name])
        else:
            self.formations = self.formations.order_by('nom')

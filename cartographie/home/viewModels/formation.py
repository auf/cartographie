#coding: utf-8

from cartographie.formation.models import Formation
from cartographie.home.forms.formation import FormationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class FormationListeViewModel(object):

    def __init__(self, request, *args, **kwargs):
        self.form = FormationForm()
        self.formations = None
        self.terme_recherche = None

        if self._has_query(request):
            self._filter_by_query(request)
        else:
            self._filter_by_page(request)

    def get_data(self):
        return {
            "formation_form": self.form,
            "terme_recherche": self.terme_recherche,
            "formations": self.formations
        }

    def _filter_by_page(self, request):
        self.formations = Formation.objects.all()

        paginator = Paginator(self.formations, 25)

        page = request.GET.get('page')
        try:
            self.formations = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            self.formations = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999)
            self.formations = paginator.page(paginator.num_pages)

    def _has_query(self, request):
        return "s" in request.GET

    def _filter_by_query(self, request):
        self.terme_recherche = request.GET["s"]
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
            ).order_by('nom')

#coding: utf-8

from cartographie.formation.models import Formation
from cartographie.formation.models.configuration import Discipline
from collections import namedtuple
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from auf.django.references import models as ref
from  django.core.exceptions import ObjectDoesNotExist

from django import forms
from cartographie.formation.models.configuration import NiveauDiplome
from cartographie.formation.models.configuration import Discipline

NUM_FORMATIONS_PER_PAGE = 25


Column = namedtuple('Column', ['sort_name', 'sort_name_desc', 'sort_column', 'name'])

columns = map(lambda args: Column(*args),
              [('nom', '-nom', 'nom', 'Nom'),
               ('niveau', '-niveau', 'niveau_diplome', 'Niveau'),
               ('discipline', '-discipline', 'discipline_1__nom', 'Discipline(s)'),
               ('etablissement', '-etablissement', 'etablissement__nom', 'Établissement'),
               ('pays', '-pays', 'etablissement__pays__nom', 'Pays'),
               ('region', '-region', 'etablissement__region__nom', 'Région')])

sort_name2sort_column = dict((col.sort_name, col.sort_column) 
                             for col in columns)


def discipline_parent(discipline):
    if discipline is None:
        return

    code_parent = discipline.code[:-1]

    if not code_parent:
        return

    try:
        return Discipline.objects.get(code=code_parent)
    except:
        pass
    
def disciplines_enfants(discipline):
    code = discipline.code if discipline else ''

    regex_enfants = r'^%s[0-9]$' % code
    return Discipline.objects.filter(code__regex=regex_enfants)    

def num_formations(formations, discipline):
    return formations.filter(Q(discipline_1__code__startswith=discipline.code) | Q(discipline_2__code__startswith=discipline.code) | Q(discipline_1__code__startswith=discipline.code)).count()

class RechercheForm(forms.Form):
    terme = forms.CharField(
        max_length=150,
        label=u"Recherchez une formation",
        widget=forms.TextInput(attrs={"class": "search-query input-xlarge"}),
        required=False,
        )

    # niveau = forms.ModelChoiceField(queryset=NiveauDiplome.objects.all(),
    #                                 empty_label=u'Tous les diplômes',
    #                                 required=False)

    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(),
                                        empty_label=u'Toutes les disciplines', 
                                        required=False)

    region = forms.ModelChoiceField(queryset=ref.Region.objects.all(),
                                    empty_label=u"Toutes", 
                                    required=False,
                                    widget=forms.Select(attrs={"class": "input-medium"}))

    pays = forms.ModelChoiceField(queryset=ref.Pays.objects.all(),
                                  empty_label=u'Tous',
                                  required=False,
                                  widget=forms.Select(attrs={"class": "input-medium"}))

    etablissement = forms.ModelChoiceField(queryset=ref.Etablissement.objects.all(),
                                           empty_label=u'Tous', 
                                           required=False,
                                           widget=forms.Select(attrs={"class": "input-medium"}))

    # Affichés en tant que champs cachés.
    tri = forms.Field(required=False)
    parpage = forms.Field(required=False)
    page = forms.Field(required=False)

    def _post_clean(self):
        region = self.cleaned_data['region']
        if region:
            self.fields['pays'].queryset = self.fields['pays'].queryset.filter(region=region)
            self.fields['etablissement'].queryset = self.fields['etablissement'].queryset.filter(pays__region=region)

        pays = self.cleaned_data['pays']
        if pays:
            self.fields['etablissement'].queryset = self.fields['etablissement'].queryset.filter(pays=pays)

    

def recherche_formation(form):
    def _filter(formations):
        def _contains():
            terme = form.cleaned_data['terme']
            if terme:
                return Q(nom__icontains=terme) |\
                    Q(discipline_1__nom__icontains=terme) |\
                    Q(discipline_2__nom__icontains=terme) |\
                    Q(discipline_3__nom__icontains=terme) |\
                    Q(etablissement__nom__icontains=terme) |\
                    Q(etablissement__region__nom__icontains=terme) |\
                    Q(etablissement__pays__nom__icontains=terme) |\
                    Q(niveau_diplome__nom__icontains=terme)
            return Q()

        def _region():
            region = form.cleaned_data['region']
            if region:
                return Q(etablissement__region=region)
            return Q()
        
        def _pays():
            pays = form.cleaned_data['pays']
            if pays:
                return Q(etablissement__pays=pays)
            return Q()

        def _etablissement():
            etablissement = form.cleaned_data['etablissement']
            if etablissement:
                return Q(etablissement=etablissement)
            return Q()

        def _discipline():
            discipline = form.cleaned_data['discipline']
            if discipline:
                return Q(discipline_1__code__startswith=discipline.code) | \
                    Q(discipline_2__code__startswith=discipline.code) | \
                    Q(discipline_3__code__startswith=discipline.code)
            return Q()

        def _niveau_diplome():
            niveau_diplome = form.cleaned_data['niveau']
            if niveau_diplome:
                return Q(niveau_diplome=niveau_diplome)
            return Q()

        q_formation = _contains()

        for filter in [_region, _pays, _etablissement, _discipline# , _niveau_diplome
                       ]:
            q_formation &= filter()

        return formations.filter(q_formation)

    formations = _filter(Formation.objects.exclude(statut=999)) # 999 = supprimées
    return formations

class FormationRechercheViewModel(object):
    formations = None
    discipline = None
    form = None
    parent = None
    enfants = None
    sort = None

    def __init__(self, request, *args, **kwargs):
        self.form = RechercheForm(request.GET)

        # TODO: Quoi faire si c'est invalide?
        if not self.form.is_valid():
            print "FORM NON VALIDE"
            print self.form.errors
            return

        self.formations = self.raw_formations = recherche_formation(self.form)
        self._sort(request.GET.get('tri'))
        self._paginate(request)
        
        self.discipline = self.form.cleaned_data['discipline']
        if self.discipline:
            self.discipline.num_formations = num_formations(self.raw_formations, self.discipline)
        self.parent = discipline_parent(self.discipline)
        self.enfants = disciplines_enfants(self.discipline)
        for discipline in self.enfants:
            discipline.num_formations = num_formations(self.raw_formations, discipline)


    def get_data(self):
        data =  {
            "columns": columns,
            "formations": self.formations,
            "discipline": self.discipline,
            "form": self.form,
            "parent": self.parent,
            "enfants": self.enfants,
            "tri": self.sort,
            }
        return data

    def _paginate(self, request):
        page = request.GET.get('page')
        try:
            perpage = int(request.GET.get('parpage', NUM_FORMATIONS_PER_PAGE))
        except ValueError:
            perpage = NUM_FORMATIONS_PER_PAGE

        if perpage <= 0:
            perpage = NUM_FORMATIONS_PER_PAGE

        paginator = Paginator(self.formations, perpage)
        try:
            self.formations = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            self.formations = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999)
            self.formations = paginator.page(paginator.num_pages)

    def _sort(self, sort):
        if sort and sort.strip('-') in sort_name2sort_column:
            asc = sort[0] != '-'
            sort_name = sort.strip('-')
            prefix = '' if asc else '-'
            self.sort = { 'asc': asc,
                          'name': sort_name, 
                          'string': prefix + sort_name }
            self.formations = self.formations.order_by(
                prefix + sort_name2sort_column[sort_name])
        else:
            self.formations = self.formations.order_by('nom')

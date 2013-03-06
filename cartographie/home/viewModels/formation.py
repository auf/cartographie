#coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cartographie.formation.models import Formation


class FormationListeViewModel(object):
    formations = None

    def __init__(self, request, *args, **kwargs):
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

    def get_data(self):
        return {
            "formations": self.formations
        }

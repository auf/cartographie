#coding: utf-8


from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from cartographie.formation.models import Formation

def accueil(request):

    from cartographie.home.viewModels.accueil import AccueilViewModel

    vm = AccueilViewModel(request)

    return render_to_response(
        "accueil.html", vm.get_data(), RequestContext(request)
    )

#@login_required
def formation_liste(request):
    formations = Formation.objects.all()
    c = {
        'formations':formations,
    }
    return render(request, "formation_liste.html", c)

#@login_required
def formation_detail(request, id, slug=None):
    formation = Formation.objects.get(pk=id)
    c = {
        'formation':formation,
    }
    return render(request, "formation_detail.html", c)

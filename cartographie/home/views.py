#coding: utf-8

from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from cartographie.formation.models import Formation


def accueil(request):

    from cartographie.home.viewModels.accueil import AccueilViewModel

    vm = AccueilViewModel(request)

    return render_to_response(
        "accueil.html", vm.get_data(), RequestContext(request)
    )


@login_required
def formation_liste(request):

    from cartographie.home.viewModels.formation \
        import FormationListeViewModel

    # la gestion de la pagination se fait dans le viewModel
    vm = FormationListeViewModel(request)

    return render_to_response(
        "formation_liste.html", vm.get_data(), RequestContext(request)
    )


@login_required
def formation_detail(request, id, slug=None):
    formation = Formation.objects.get(pk=id)
    c = {
        'formation': formation,
    }
    return render(request, "formation_detail.html", c)

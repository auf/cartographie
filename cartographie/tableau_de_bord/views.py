#coding: utf-8
#
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    from viewModels.index import IndexViewModel as vm

    return render_to_response(
        "index.html", vm(request).get_data(), RequestContext(request)
    )


@login_required
def statistiques(request):
    from viewModels.statistiques import StatistiquesViewModel as vm

    return render_to_response(
        "statistiques.html", vm(request).get_data(), RequestContext(request)
    )


@login_required
def liste_etablissements(request):
    from viewModels.liste_etablissements import ListeEtablissementsViewModel as vm

    return render_to_response(
        "liste_etablissements.html", vm(request).get_data(), RequestContext(request)
    )

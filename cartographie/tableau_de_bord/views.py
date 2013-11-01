# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext


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

@login_required
def modifications(request):
    from viewModels.modifications import ModificationsViewModel as vm

    return render_to_response(
        "modifications.html", vm(request).get_data(), RequestContext(request)
    )


@login_required
def administration(request):
    return render(request, 'administration.html', {})


@login_required
def jetonizer(request):
    call_command('jetonizer')
    messages.success(request, 'Les jetons ont été regénéré avec succès.')

    return redirect('dashboard_administration')

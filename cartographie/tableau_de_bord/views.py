# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext

from cartographie.formation.models import Acces, Formation, Personne, UserRole


@login_required
def contact(request):

    contacts = UserRole.get_contacts(request.user)

    return render_to_response(
        "contact.html", contacts, RequestContext(request)
    )


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
    from viewModels.liste_etablissements import (
        ListeEtablissementsViewModel as vm)

    return render_to_response(
        'liste_etablissements.html', vm(request).get_data(),
        RequestContext(request))


@login_required
def liste_formations(request):
    formations_dict = defaultdict(lambda: [])

    regions = UserRole.get_toutes_regions(request.user)

    formations = Formation.objects.filter(
        etablissement__region__in=regions).exclude(statut=999)

    for formation in formations:
        pays = formation.etablissement.pays.nom
        token = Acces.token_for_etablissement(formation.etablissement)
        formations_dict[pays].append((formation, token))

    for pays, formations_list in formations_dict.items():
        # Trie les formations dans un pays par ordre alphabétique
        formations_dict[pays] = sorted(
            formations_list, cmp=lambda a, b: cmp(a[0].nom, b[0].nom))

    return render(request, 'liste_formations.html', {
        'formations_dict': sorted((k, v) for k, v in formations_dict.items()),
        'menu_actif': 'liste_formations',
    })


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

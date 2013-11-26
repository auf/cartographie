# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import chain
import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.management import call_command
from django.http import Http404
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from cartographie.formation.models import Acces, Formation, Personne, UserRole


@login_required
def contact(request):

    contacts = UserRole.get_contacts(request.user)

    return render_to_response(
        "contact.html", contacts, RequestContext(request)
    )

@login_required
def export_tous_contacts(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    contacts = UserRole.get_contacts(request.user)
    personnes_csv = map(lambda u: ("%s %s" % (u.prenom, u.nom), u.courriel), contacts['referents'])
    users_csv = map(lambda u: (u.get_full_name(), u.email), contacts['referents_regions'])

    data_csv = chain(personnes_csv, users_csv)
    writer =csv.writer(response)
    for personne in data_csv:
        writer.writerow(personne)
    return response


@login_required
def export_contacts(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    keys = request.POST.keys()

    personne_keys = map(lambda k: k.replace('personne-', ''),
                        filter(lambda k: k.startswith('personne-'), keys))

    user_keys = map(lambda k: k.replace('user-', ''),
                    filter(lambda k: k.startswith('user'), keys))

    personnes = Personne.objects.filter(pk__in=personne_keys)
    users = User.objects.filter(pk__in=user_keys)

    personnes_csv = map(lambda u: ("%s %s" % (u.nom, u.prenom), u.courriel), personnes)
    users_csv = map(lambda p: (p.get_full_name(), p.email), users)

    data_csv = chain(personnes_csv, users_csv)

    writer = csv.writer(response)
    for personne in data_csv:
        writer.writerow(personne)

    return response

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
    if not request.user.is_superuser:
        raise Http404

    return render(request, 'administration.html', {})


@login_required
def jetonizer(request):
    call_command('jetonizer')
    messages.success(request, 'Les jetons ont été regénéré avec succès.')

    return redirect('dashboard_administration')

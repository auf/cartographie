#coding: utf-8

from collections import defaultdict
from datetime import datetime, timedelta
import json

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext, Template, Context
from django.conf import settings

from auf.django.references import models as ref
from auf.django.references.models import Etablissement

from cartographie.formation.models import Fichier, Formation, Personne, Acces
from cartographie.formation.sendfile import send_file
from cartographie.formation.stats import num_etablissements_per_country
from cartographie.formation.models.userRole import UserRole
import cartographie.home

@login_required
def accueil_login(request):
    regions = UserRole.get_toutes_regions(request.user)
    if regions:
        return HttpResponseRedirect(reverse('dashboard_statistiques'))
    else:
        try:
            personne = Personne.objects.get(utilisateur=request.user)
            if personne.role in ('referent', 'redacteur',):
                token = Acces.objects.get(etablissement=personne.etablissement)

            return redirect('formation_liste', token.token)
        except Personne.DoesNotExist:
            pass




def get_film_url():
    if getattr(settings, 'FILM_URL', ''):
        return {'afficher_film': True,
                'film_url': settings.FILM_URL}
    return {'afficher_film': False}


def accueil(request):
    lasts = Formation.objects.exclude(
        statut=999).order_by('-date_modification')[:10]

    view_data = {
        'dernieres': lasts,
    }

    view_data.update(get_film_url())

    return render(request, "accueil.html", view_data)


def rechercher(request):
    from cartographie.home.viewModels.formation \
        import FormationRechercheViewModel

    form_params = request.GET.copy()

    if request.GET.get('pays'):
        try:
            pays = int(request.GET.get('pays'))
        except ValueError:
            pays_iso3 = request.GET.get('pays')
            form_params['pays'] = ref.Pays.objects.get(code_iso3=pays_iso3).pk

    vm = FormationRechercheViewModel(form_params)
    vm_data = vm.get_data()
    c = {}
    c.update(vm_data)
    view_data = get_film_url()
    c.update(view_data)

    return render(request, "rechercher.html", c)


def liste_etablissements(request):
    regions = defaultdict(lambda: [])

    for etablissement in Etablissement.objects.all():
        # Seulement lister les établissements possédant au moins une formation
        # active (statut différent de 999)
        if etablissement.formation_set.exclude(statut=999):
            regions[etablissement.region].append(etablissement)

    # Trie les régions en ordre décroissant de nombre de formations par région
    ordered = sorted(
        ((k, v) for k, v in regions.iteritems()),
        cmp=lambda a, b: cmp(len(b[1]), len(a[1])))

    context = {
        'regions': ordered,
    }

    return render(request, 'etablissements.html', context)


def aide(request):
    view_data = get_film_url()
    return render(request, "statiques/aide.html", view_data)


def apropos(request):
    view_data = get_film_url()
    return render(request, "statiques/a-propos.html", view_data)


def feedback(request):
    from cartographie.home.viewModels.feedback import FeedbackViewModel
    vm = FeedbackViewModel(request)
    vm_data = vm.get_data()
    c = {}
    c.update(vm_data)
    view_data = get_film_url()
    c.update(view_data)
    return render(request, "feedback.html", c)


def legal(request):
    view_data = get_film_url()
    return render(request, "statiques/legal.html", view_data)


def contact(request):
    view_data = get_film_url()
    return render(request, "statiques/contact.html", view_data)


def credits(request):
    view_data = get_film_url()
    return render(request, "statiques/credits.html", view_data)


def formation_detail(request, id, slug=None):
    formation = Formation.objects.get(pk=id)

    c = {}

    year_ago = datetime.now() - timedelta(days=365)

    if formation.date_modification <= year_ago:
        # TODO Valider le message d'erreur
        messages.error(
            request,
            u"""Cette formation n'a pas été mise à jour dans la dernière année.
            Les informations contenues peuvent ne plus être valides.""")
        c['old'] = True
    elif formation.statut == 2:
        messages.error(
            request, u"""Formation en cours de publication. Les informations
            présentées dans cette fiche pourraient être révisées prochainement.
            Cette fiche est mise temporairement à votre disposition pour votre
            convenance."""
            )
    elif formation.statut == 1:
        messages.error(
            request, u"""Formation en rédaction. Les informations présentées
            dans cette fiche n'ont pas été validées par l'établissement
            dispensant la formation. Cette fiche est mis temporairement à votre
            disposition pour votre convenance. Merci de vous référer
            directement au site Internet de la formation ou de l'établissement
            dispensant la formation pour obtenir des informations officielles
            validées."""
            )
    elif formation.statut == 999:
        messages.error(
            request, u"""Formation supprimée. Aucune information sur cette
            fiche n'est fiable."""
            )

    c.update({
        'formation': formation,
        'files': Fichier.objects.filter(
            formation=formation).filter(is_public=True).order_by('nom'),
        'composantes_actives': formation.etablissement_composante.filter(actif=True),
        'auf_actifs': formation.formationpartenaireauf_set.filter(
            etablissement__actif=True),
    })

    view_data = get_film_url()
    c.update(view_data)

    return render(request, "formation/formation_detail.html", c)


def fichiers(request, fichier_id):
    requested_file = get_object_or_404(Fichier, pk=fichier_id)

    if requested_file.is_public:
        return send_file(requested_file.file)

    raise Http404


def geojson_formations(request):
    geojson = []

    raw_template = """<div>
        {% load pluralize %}
        <b>{{ nom }}</b><br/>
        <div>{{ formations }} formation{{ formations|pluralize_fr }}</div>
        <div>
            {{ etablissements }} établissement{{ etablissements|pluralize_fr }}
        </div>
        </div>"""

    t = Template(raw_template)

    def get_geojson_feature(country):
        return {
            "type": "Feature",
            "properties": {
                "isoAlpha3": country['code'],
                "formations": country['formations'],
                "etablissements": country['etablissements'],
                "nom": country['nom'],
                "tooltip": t.render(Context(country)),
                "url": "%s?pays=%s" % (
                    reverse('home_rechercher'), country['code'])
            },
            "geometry": {
                "type": "Point",
                "coordinates": [country['lon'], country['lat']]
            }
        }

    coordonnees_path = (
        "%s/data/coordonnees.json" % cartographie.home.__path__[0]
    )

    with open(coordonnees_path) as coords:
        lines = coords.readlines()
        coords = json.loads("".join(lines))
        etab_per_country = num_etablissements_per_country()
        form_per_country = Formation.num_formations_per_country()
        for country in form_per_country.keys():
            isoAlpha3 = country.upper()
            feature_dict = {
                "code": isoAlpha3,
                "formations": form_per_country[country],
                "etablissements": etab_per_country[country],
                "lat": coords[isoAlpha3]["lat"],
                "lon": coords[isoAlpha3]["lon"],
                "nom": coords[isoAlpha3]["nom"],
            }
            geojson.append(get_geojson_feature(feature_dict))

    return HttpResponse(json.dumps(geojson), content_type="application/json")

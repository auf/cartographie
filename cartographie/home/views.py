#coding: utf-8


import json
import cartographie.home

from cartographie.formation.models import Fichier, Formation
from cartographie.formation.sendfile import send_file
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext, Template, Context

from cartographie.formation.models import Fichier, Formation
from cartographie.formation.sendfile import send_file
from cartographie.home.forms.feedback import FeedbackForm

def accueil(request):
    from cartographie.home.viewModels.accueil \
        import AccueilViewModel

    vm = AccueilViewModel(request)

    return render_to_response(
        "accueil.html", vm.get_data(), RequestContext(request)
    )

def aide(request):
    return render(request, "statiques/aide.html")

def apropos(request):
    return render(request, "statiques/a-propos.html")

def feedback(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            messages.success(
                request, u"Votre message nous a bien été envoyé. Merci!"
            )
            form.save()
            # envoie courriel
    c = {
        'form': form,
    }
    return render(request, "feedback.html", c)

def legal(request):
    return render(request, "statiques/legal.html")

def contact(request):
    return render(request, "statiques/contact.html")

def credits(request):
    return render(request, "statiques/credits.html")

def formation_rechercher(request):
    from cartographie.home.viewModels.formation \
        import FormationRechercheViewModel
   
    vm = FormationRechercheViewModel(request)

    return render_to_response(
        "formation_rechercher.html", vm.get_data(), RequestContext(request)
    )

def formation_detail(request, id, slug=None):
    formation = Formation.objects.get(pk=id)
    c = {
        'formation': formation,
        'files': Fichier.objects.filter(formation=formation).filter(is_public=True).order_by('nom')
    }
    return render(request, "formation/formation_detail.html", c)


def fichiers(request, fichier_id):
    requested_file = get_object_or_404(Fichier, pk=fichier_id)

    if requested_file.is_public:
        return send_file(requested_file.file)

    raise Http404

def geojson_formations(request):
    import json
    geojson = []

    raw_template = """<div>
      <b>{{ nom }}</b><br/>
      <div>{{ formations }} formations</div>
      u
    </div>"""
    t = Template(raw_template)
    def get_feature(country):
        return {
              "type": "Feature",
              "properties": {
                  "isoAlpha3": country['code'],
                  "formations": country['formations'],
                  "nom": country['nom'],
                  "tooltip": t.render(Context(country))
              },
              "geometry": {
                "type": "Point",
                "coordinates": [country['lon'], country['lat']]
            }
        }

    coordonnees_path = "%s/data/coordonnees.json" % cartographie.home.__path__[0]
    with open(coordonnees_path) as coords:
        lines = coords.readlines()
        coords = json.loads("".join(lines))
        form_per_country = Formation.num_formations_per_country()
        for country in form_per_country.keys():
            isoAlpha3 = country.upper()
            feature_dict = {
              "code": isoAlpha3,
              "formations": form_per_country[country],
              "lat": coords[isoAlpha3]["lat"],
              "lon": coords[isoAlpha3]["lon"],
              "nom": coords[isoAlpha3]["nom"],
            }
            geojson.append(get_feature(feature_dict))
    print geojson
    return HttpResponse(json.dumps(geojson), content_type="application/json")

#coding: utf-8

from cartographie.formation.models import Fichier, Formation
from cartographie.formation.sendfile import send_file
from cartographie.home.forms.formation import FormationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext

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
    return render(request, "feedback.html")

def legal(request):
    return render(request, "statiques/legal.html")

def contact(request):
    return render(request, "statiques/contact.html")

def credits(request):
    return render(request, "statiques/credits.html")

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
        'form': FormationForm(),
        'files': Fichier.objects.filter(formation=formation).filter(is_public=True).order_by('nom')
    }
    return render(request, "formation/formation_detail.html", c)


def fichiers(request, fichier_id):
    requested_file = get_object_or_404(Fichier, pk=fichier_id)

    if requested_file.is_public:
        return send_file(requested_file.file)

    raise Http404

#coding: utf-8

from cartographie.formation.models import Fichier, Formation
from cartographie.formation.sendfile import send_file
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext

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

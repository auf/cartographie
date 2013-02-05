# coding: utf-8
# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
# from django.forms.models import modelformset_factory
# from django.forms.models import model_to_dict
# from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import TemplateView

# from auf.django.references import models as ref
from formation import models
from formation.decorators import token_required


class ConnexionView(View):
    def get(self, request, token):
        """
        Vérifie si le token est valide et redirige l'usager à la liste
        des fiches formations
        """
        try:
            token = models.Acces.objects.select_related(
                'etablissement'
            ).get(
                token=token
            )

            if len(token) != 0:
                request.session['espace_formation_etablissement_id'] = token.etablissement_id
                return redirect('formation_liste')
            return redirect("formation_erreur")

        except ObjectDoesNotExist:

            request.session['espace_formation_erreur'] = True
            return redirect('formation_erreur')


class ErreurView(TemplateView):
    template_name = "erreur.html"


class ListeView(View):
    @token_required
    def get(request):
        return render_to_response("liste.html", {}, RequestContext(request))


class AjouterView(View):
    @token_required
    def get(request):
        return render_to_response("ajouter.html", {}, RequestContext(request))

    @token_required
    def post(request, **kwargs):
        return render_to_response("liste.html", {}, RequestContext(request))


class ModifierView(View):
    @token_required
    def get(request, formation_id):
        return render_to_response("modifier.html", {}, RequestContext(request))

    @token_required
    def post(request, **kwargs):
        return render_to_response("modifier.html", {}, RequestContext(request))

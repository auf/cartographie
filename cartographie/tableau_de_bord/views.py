#coding: utf-8
#
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render_to_response(
        "index.html", {}, RequestContext(request)
    )


@login_required
def statistiques(request):
    return render_to_response(
        "statistiques.html", {}, RequestContext(request)
    )


@login_required
def liste_etablissements(request):
    return render_to_response(
        "liste_etablissements.html", {}, RequestContext(request)
    )

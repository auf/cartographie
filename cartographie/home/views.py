#coding: utf-8

from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response


def accueil(request):

    return render_to_response(
        "accueil.html", {}, RequestContext(request)
    )


def test(request):
    return render_to_response(
        "accueil.html", {}, RequestContext(request)
    )

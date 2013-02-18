#coding: utf-8

from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response


def any_password_reset(request):

    from cartographie.anyPwdReset.viewModels.reset import ResetViewModel

    vm = ResetViewModel(request)

    return render_to_response(
        "any_password_reset.html", vm.get_data(), RequestContext(request)
    )

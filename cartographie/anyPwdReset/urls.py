# coding: utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns(
    "cartographie.anyPwdReset.views",
    url(
        r"^admin/any_password_reset/$", "any_password_reset",
        namespace="anyPwdReset", name="any_password_reset"
    ),
)

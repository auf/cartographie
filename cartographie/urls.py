# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, \
        handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

handler404
handler500  # Pyflakes

urlpatterns = patterns('',
    # app Home
    (r'^$', include("cartographie.home.urls")),
    # app Formation
    (r'^etablissement/', include("cartographie.formation.urls")),
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset',
        name='formation_password_reset'
    ),
    url(
        r"^admin/any_password_reset/$",
        "cartographie.anyPwdReset.views.any_password_reset",
        name="any_password_reset"
    ),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',
        'django.contrib.auth.views.password_reset_confirm'
    ),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT, }),
        )

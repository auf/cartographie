# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, \
    handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse_lazy


admin.autodiscover()

handler404
handler500  # Pyflakes

urlpatterns = patterns(
    '',
    # app Home
    (r'^', include("cartographie.home.urls")),
    # app Formation
    (r'^etablissement/', include("cartographie.formation.urls")),
    # app tableau_de_bord
    (r'^dashboard/', include("cartographie.tableau_de_bord.urls")),
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    # login/logout
    url(r'^connexion/', "django.contrib.auth.views.login", name="login"),
    url(r'^deconnexion/', "django.contrib.auth.views.logout", 
        {"next_page": reverse_lazy("home_accueil") }, name="logout"),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^404/$', handler404),
        url(r'^500/$', handler500),
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        )
    )

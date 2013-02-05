# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, \
        handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

handler404
handler500  # Pyflakes

urlpatterns = patterns(
    '',
    # admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^formation/', include("cartographie.formation.urls"))
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT, }),
        )

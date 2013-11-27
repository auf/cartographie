# -*- encoding: utf-8 -*-

import os
import socket

from django.conf.global_settings import (
    TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TEMPLATE_CONTEXT_PROCESSORS)
from django.conf.global_settings import (
    MIDDLEWARE_CLASSES as DEFAULT_MIDDLEWARE_CLASSES)
from django.conf.global_settings import (
    AUTHENTICATION_BACKENDS as DEFAULT_AUTHENTICATION_BACKENDS)
from django.core.urlresolvers import reverse_lazy

# Rapports d'erreurs
SERVER_EMAIL = 'ne-pas-repondre@auf.org'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = '1025'
EMAIL_SUBJECT_PREFIX = '[auf_cartographie - %s] ' % socket.gethostname()
ADMINS = ()

MANAGERS = ADMINS

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr-ca'

PROJECT_ROOT = os.path.dirname(__file__)
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'sitestatic')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

ROOT_URLCONF = 'cartographie.urls'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'south',
    'raven.contrib.django',
    # AUF
    'home',
    'formation',
    'tableau_de_bord',
    'auf.django.references',
    'auf.django.permissions',
    'auf.django.pong',
    'auf.django.mailing',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'home.context_processor.stats',
)

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES + (
    'auf.django.piwik.middleware.TrackMiddleware',
)

INTERNAL_IPS = ('127.0.0.1', '::ffff:127.0.0.1', )

AUTHENTICATION_BACKENDS = DEFAULT_AUTHENTICATION_BACKENDS

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

SOUTH_TESTS_MIGRATE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s %(process)d ' +
                '%(thread)d %(message)s')
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

ADMIN_TOOLS_INDEX_DASHBOARD = 'cartographie.dashboard.CustomIndexDashboard'

from conf import *

LOGIN_REDIRECT_URL = reverse_lazy("home_accueil_login")
LOGIN_URL = reverse_lazy("login")

UPLOAD_DIRECTORY = MEDIA_ROOT

DEBUG = True

# -*- encoding: utf-8 -*-

from cartographie.settings import *

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'david.cormier@savoirfairelinux.com'


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Décommentez ces lignes pour activer la debugtoolbar
INTERNAL_IPS = ('127.0.0.1',)
#INSTALLED_APPS += ('debug_toolbar',)
#MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

AUTH_PASSWORD_REQUIRED = False

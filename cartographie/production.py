# -*- encoding: utf-8 -*-

# En production, rediriger la sortie terminal on disponible en WSGI
# vers la sortie fichier errorlog.
import sys
sys.stdout = sys.stderr

from cartographie.settings import *

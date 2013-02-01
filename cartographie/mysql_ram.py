#encoding UTF-8
# -*- encoding: utf-8 -*-

"""
Configuration du site pour faire fonctionner les tests unitaires avec
MySQL en RAM.
"""

from production import *

DATABASES['default']['HOST'] = '/var/run/mysqld/mysqld-ram.sock'

host = "mysql --socket=%s -uroot -e" % DATABASES['default']['HOST']
db = "unittests_%s" % DATABASES['default']['NAME']
DATABASES['default']['NAME'] = db
DATABASES['default']['TEST_NAME'] = db
user = DATABASES['default']['USER']
pwd = DATABASES['default']['PASSWORD']

cmd_creer_bd = "%(host)s \
        'CREATE DATABASE %(db)s;'" % {
                'host': host,
                'db': db,
                }

cmd_creer_user = """%(host)s \
        "GRANT USAGE ON *.* TO %(user)s@localhost \
        IDENTIFIED BY '%(pwd)s';" """ % {
                'host': host,
                'user': user,
                'pwd': pwd,
                }

cmd_creer_privileges = "%(host)s \
        'GRANT ALL PRIVILEGES ON *.* TO %(user)s@localhost ;'" % {
                'host': host,
                'user': user,
                }


# La bd non préfixée par "test_" a besoin d'exister pour lancer les tests.
# Cette commande ne modifie rien, si la table existe déjà.
os.system(cmd_creer_bd)

# Création de l'accès à la base "test_xxx" en fonction de conf.py
os.system(cmd_creer_user)
os.system(cmd_creer_privileges)

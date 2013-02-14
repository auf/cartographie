#coding: utf-8

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.management import call_command


class JetonizerTestCase(TestCase):

    def test_command(self):
        """
        tester la commande Jetonizer et s'assurer que chaque etablissement
        membre possede son propre jeton
        """

        args = []
        opts = {}

        call_command("jetonizer", *args, **opts)


class ImportUsersTestCase(TestCase):

    def test_command(self):
        """
            Tester l'import des employés de l'AUF dans la tables des users de
            l'application "formation"
        """

        args = []
        opts = {}

        call_command("import_auf_employees", *args, **opts)


class ImportConfigData(TestCase):
    def test_command(self):
        args = []
        opts = {}

        call_command("import_config_models", *args, **opts)

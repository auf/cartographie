#coding: utf-8

from django.core.management.base import BaseCommand

from auf.django.references import models as ref
from formation.models import Acces


class Command(BaseCommand):
    help = u"""
        Crée les jetons d'accès pour tout établissement membre
        qui n'en possède pas.
    """

    def handle(self, *args, **options):
        etabs = ref.Etablissement.objects.filter(membre=True).all()

        for etab in etabs:
            self.stdout.write("Verification de l'établissement: %s\n" % etab)

            acces_avec_token = Acces.objects.filter(etablissement=etab).all()

            if len(acces_avec_token) == 0:
                self.stdout.write("** Pas de jeton d'acces\n")

                nouvel_acces = Acces()
                nouvel_acces.etablissement = etab
                nouvel_acces.active = True
                nouvel_acces.generer_token()
                nouvel_acces.save()
                self.stdout.write("** token: %s\n" % nouvel_acces.token)
            else:
                self.stdout.write("** Possede un jeton d'acces\n")

            self.stdout.write("---\n")

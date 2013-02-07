#coding: utf-8

import random
import string

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as DjangoUser

from auf.django.references import models as ref


class Command(BaseCommand):
    args = ''
    help = """
        Importation des usagers de l'AUF
    """

    def handle(self, *args, **options):
        # obtention des employés de l'AUF
        # on exclut ceux qui ne possède pas de courriel
        employes = ref.Employe.objects.filter(
            courriel__isnull=False
        ).exclude(
            courriel=''
        )

        for e in employes:
            self.stdout.write(
                "Verification de l'existence de l'employe: %s\n" % e
            )

            # Il existe un User avec le courriel de cet employé !
            if DjangoUser.objects.filter(email=e.courriel).count() > 0:
                self.stdout.write("** %s existe ! next !\n" % e)
                continue  # go on, nothing to see

            self.stdout.write("** Creation du user\n")

            # la création elle-même du user à partir des infos de
            # l'employé
            nouveau_user = DjangoUser.objects.create(
                first_name=e.prenom,
                last_name=e.nom,
                is_staff=True,
                is_active=True,
                username=(e.courriel.split('@')[0]),
                email=e.courriel
            )

            nouveau_user.set_password(
                ''.join([string.letters[random.randint(0, 25)]])
            )

            self.stdout.write("---\n")

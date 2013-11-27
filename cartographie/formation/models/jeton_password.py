# -*- coding: utf-8 -*-

import os

from django.db import models


class JetonPasswordManager(models.Manager):

    def create_jeton_password(self):
        # Utilise os.urandom pour avoir une chaîne cryptographiquement
        # sécuritaire
        secret = os.urandom(32).encode('hex').upper()
        jeton_password = self.create(jeton=secret)

        return jeton_password


class JetonPassword(models.Model):

    class Meta(object):

        app_label = 'formation'
        verbose_name = 'Jeton de mot de passe'
        verbose_name_plural = 'Jetons de mot de passe'

    EXPIRE_APRES = 3  # jours

    objects = JetonPasswordManager()

    jeton = models.CharField(max_length=64, blank=False)

    creation = models.DateField(auto_now=True)

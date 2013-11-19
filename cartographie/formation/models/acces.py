#coding: utf-8

import string
import random

from django.db import models

from auf.django.references import models as ref


class Acces(models.Model):
    """
        Classe d'association d'un établissement à un jeton d'identification
    """

    etablissement = models.ForeignKey(ref.Etablissement)
    token = models.CharField(max_length=128, unique=True, null=False,
              verbose_name="Code d'accès")
    active = models.NullBooleanField()

    token_charset = "abcdefghiklmnopqrstuvwxyz01234567890"

    @staticmethod
    def token_for_etablissement(etablissement):
        try:
            acces = Acces.objects.select_related('etablissement')\
                .get(etablissement=etablissement)
            return acces.token
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def etablissement_for_token(token):
        try:
            acces = Acces.objects.select_related('etablissement')\
                .get(token=token)
            return acces.etablissement
        except ObjectDoesNotExist:
            return None

    class Meta:
        verbose_name = u"Accès aux formulaires"
        verbose_name_plural = u"Accès aux formulaires"
        app_label = "formation"
        db_table = "formation_acces"

    def __unicode__(self):
        return u"%s" % self.etablissement

    def generer_token(self, size=32):
        self.token = ''.join(
            random.choice(string.letters + string.digits) for i in xrange(size)
        )

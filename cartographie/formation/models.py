#coding: utf-8

import random
import string

from django.db import models

from auf.django.references import models as ref


class Formation(models.Model):

    pass


class FormationHistoriqueModification(models.Model):
    formation = models.ForeignKey(Formation)
    derniere_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"Historique d'une formation"
        verbose_name_plural = u"Historiques d'une formation"

    def __unicode__(self):
        return u"%s" % self.etablissement


class Acces(models.Model):
    """
        Classe d'association d'un établissement à un jeton d'identification
    """

    etablissement = models.ForeignKey(ref.Etablissement)
    token = models.CharField(max_length=128, unique=True, null=False)
    active = models.NullBooleanField()

    token_charset = "abcdefghiklmnopqrstuvwxyz01234567890"

    class Meta:
        verbose_name = u"Code d'accès"
        verbose_name_plural = u"Codes d'accès"

    def __unicode__(self):
        return u"%s" % self.etablissement

    def generer_token(self, size=32):
        self.token = ''.join(
            random.choice(string.letters + string.digits) for i in xrange(size)
        )

    pass

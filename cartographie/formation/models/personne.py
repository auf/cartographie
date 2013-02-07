#coding: utf-8

from django.db import models
from auf.django.references import models as ref


class Personne(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    fonction = models.CharField(
        max_length=100,
        help_text=u"Titre ou fonction occupée"
    )
    etablissement = models.ForeignKey(ref.Etablissement)
    courriel = models.EmailField()

    class Meta:
        verbose_name = u"Personne"
        verbose_name_plural = u"Personnes"

    def __unicode__(self):
        return u"%s %s" % (self.prenom, self.nom)

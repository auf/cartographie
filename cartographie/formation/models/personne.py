#coding: utf-8

from django.db import models
from auf.django.references import models as ref


class Personne(models.Model):
    nom = models.CharField(max_length=100, blank=False)

    prenom = models.CharField(max_length=100, blank=False)

    etablissement = models.ForeignKey(
        ref.Etablissement,
        verbose_name=u"Établissement",
        blank=False
    )

    fonction = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name=u"Fonction",
        help_text=u"Titre ou fonction occupée"
    )

    courriel = models.EmailField(
        verbose_name=u"Courriel",
        null=True,
        blank=True,
    )

    telephone = models.CharField(
        max_length=100,
        verbose_name=u"Téléphone",
        null=True,
        blank=True,
    )

    actif = models.BooleanField(
        default=True,
        verbose_name=u"Actif?"
    )

    class Meta:
        verbose_name = u"Personne"
        verbose_name_plural = u"Personnes"
        app_label = "formation"
        db_table = "formation_personne"

    def __unicode__(self):
        return u"%s %s" % (self.prenom, self.nom.upper())

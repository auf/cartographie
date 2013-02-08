# coding: utf-8

from django.db import models

from auf.django.references import models as ref


class EtablissementComposante(models.Model):
    nom = models.CharField(
        max_length=150,
        verbose_name=u"Nom",
        help_text=u"Intitulé en français de la composante",
        blank=False
    )

    nom_origine = models.CharField(
        max_length=150,
        verbose_name=u"Nom d'origine",
        help_text=u" ".join([
            u"Intitulé de la composante dans la langue d'origine",
            u"si ce n'est pas le français"
        ])
    )

    sigle = models.CharField(
        max_length=150,
        verbose_name=u"Sigle de la composante"
    )

    ville = models.CharField(
        max_length=150,
        help_text=u"Ville de la composante (libellé en français)"
    )

    pays = models.ForeignKey(ref.Pays, help_text=u"Pays de la composante")

    url = models.URLField(help_text=u"Site Internet de la composante")

    diplomante = models.BooleanField(
        default=False,
        verbose_name=u"Diplômante?",
        help_text=u" ".join([
            u"Cocher si cette composante d'établissement est habilitée",
            u"à émettre des diplômes."
        ])
    )

    class Meta:
        verbose_name = u""
        verbose_name_plural = u""
        app_label = "formation"
        db_table = "formation_etablissementcomposante"

    def __unicode__(self):
        return u""


class EtablissementAutre(models.Model):
    nom = models.CharField(
        max_length=150, verbose_name=u"Nom",
        help_text=u" ".join([
            u"Intitulé en français de l'établissement non membre de l'AUF"
        ]),
        blank=False
    )

    nom_origine = models.CharField(
        max_length=150,
        verbose_name=u"Nom d'origine",
        help_text=u" ".join([
            u"Intitulé de l'établissment non membre dans la langue d'origine",
            u"si ce n'est pas le français"
        ])
    )

    sigle = models.CharField(
        max_length=150,
        verbose_name=u"Sigle de l'établissement non membre de l'AUF"
    )

    ville = models.CharField(
        max_length=150,
        verbose_name=u"Ville",
        help_text=u"Ville (libellé en français)"
    )

    pays = models.ForeignKey(
        ref.Pays,
        verbose_name=u"Pays", help_text=u"Pays"
    )

    url = models.URLField(
        help_text=u"Site Internet de l'établissement non membre de l'AUF"
    )

    class Meta:
        verbose_name = u""
        verbose_name_plural = u""
        app_label = "formation"
        db_table = "formation_etablissementautre"

    def __unicode__(self):
        return u""

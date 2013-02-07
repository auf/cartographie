# coding: utf-8

from django.db import models

from auf.django.references import models as ref


class EtablissementComposante(models.Model):
    nom = models.CharField(
        max_length=100,
        help_text=u"Intitulé en français de la composante"
    )
    nom_origine = models.CharField(
        max_length=100,
        help_text=u" ".join([
            u"Intitulé de la composante dans la langue d'origine ",
            u"si ce n'est pas le français"
        ])
    )
    sigle = models.CharField(
        max_length=100,
        verbose_name=u"Sigle de la composante"
    )
    ville = models.CharField(
        max_length=100,
        help_text=u"Ville de la composante (libellé en français)"
    )
    pays = models.ForeignKey(ref.Pays, help_text=u"Pays de la composante")
    url = models.URLField(help_text=u"Site Internet de la composante")
    diplomant = models.BooleanField(
        verbose_name=u"La composante est diplômante?"
    )

    class Meta:
        verbose_name = u""
        verbose_name_plural = u""

    def __unicode__(self):
        return u""

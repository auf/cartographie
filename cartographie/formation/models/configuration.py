#coding: utf-8

from django.db import models

from auf.django.references import models as ref


class AbstractNomStatut(models.Model):
    """
        Abstract Model de base pour tous les Models qui doivent
        avoir les propriétés "nom" obligatoire et "actif" en boolean
    """
    nom = models.CharField(max_length=150, verbose_name=u"Nom", blank=False)
    actif = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Discipline(models.Model):
    code = models.CharField(max_length=100, verbose_name=u"Code Erasmus")
    nom = models.CharField(max_length=150, verbose_name=u"Nom")
    discipline = models.ForeignKey(ref.Discipline, null=True)

    class Meta:
        verbose_name = u"Discipline"
        verbose_name_plural = u"Disciplines"

    def __unicode__(self):
        return u"%s %s" % (self.code, self.nom)


class NiveauDiplome(AbstractNomStatut):
    class Meta:
        verbose_name = u"Niveau de diplôme"
        verbose_name_plural = u"Niveaux de diplôme"

    def __unicode__(self):
        return u"%s" % (self.nom)


class TypeDiplome(AbstractNomStatut):
    class Meta:
        verbose_name = u"Type de diplôme"
        verbose_name_plural = u"Types de diplôme"

    def __unicode__(self):
        return u"%s" % (self.nom)


class DelivranceDiplome(AbstractNomStatut):
    class Meta:
        verbose_name = u"Délivrance de diplôme"
        verbose_name_plural = u"Délivrances de diplôme"

    def __unicode__(self):
        return u"%s" % (self.nom)


class NiveauUniversitaire(AbstractNomStatut):
    """
    Niveau universitaire en nombre d'années d'enseignement supérieur
    """
    class Meta:
        verbose_name = u"Niveau universitaire"
        verbose_name_plural = u"Niveaux universitaire"

    def __unicode__(self):
        return u"%s" % (self.nom)


class Vocation(AbstractNomStatut):

    class Meta:
        verbose_name = u"Vocation"
        verbose_name_plural = u"Vocations"

    def __unicode__(self):
        return u"%s" % (self.nom)


class TypeFormation(AbstractNomStatut):
    class Meta:
        verbose_name = u"Type de formation"
        verbose_name_plural = u"Types de formation"

    def __unicode__(self):
        return u"%s" % (self.nom)


class Langue(AbstractNomStatut):
    class Meta:
        verbose_name = u"Langue"
        verbose_name_plural = u"Langues"

    def __unicode__(self):
        return u"%s" % (self.nom)

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
        
    def __unicode__(self):
        return u"%s" % (self.nom)


class Discipline(models.Model):
    code = models.CharField(max_length=100, verbose_name=u"Code Erasmus")
    nom = models.CharField(max_length=150, verbose_name=u"Nom")
    discipline = models.ForeignKey(ref.Discipline, null=True)

    class Meta:
        verbose_name = u"Discipline"
        verbose_name_plural = u"Disciplines"
        app_label = "formation"
        db_table = "formation_config_discipline"

    def __unicode__(self):
        return u"%s %s" % (self.code, self.nom)


class NiveauDiplome(AbstractNomStatut):
    class Meta:
        verbose_name = u"Niveau de diplôme"
        verbose_name_plural = u"Niveaux de diplôme"
        app_label = "formation"
        db_table = "formation_config_niveaudiplome"


class TypeDiplome(AbstractNomStatut):
    class Meta:
        verbose_name = u"Type de diplôme"
        verbose_name_plural = u"Types de diplôme"
        app_label = "formation"
        db_table = "formation_config_typediplome"


class DelivranceDiplome(AbstractNomStatut):
    class Meta:
        verbose_name = u"Délivrance de diplôme"
        verbose_name_plural = u"Délivrances de diplôme"
        app_label = "formation"
        db_table = "formation_config_delivrancediplome"


class NiveauUniversitaire(AbstractNomStatut):
    """
    Niveau universitaire en nombre d'années d'enseignement supérieur
    """
    class Meta:
        verbose_name = u"Niveau universitaire"
        verbose_name_plural = u"Niveaux universitaires"
        app_label = "formation"
        db_table = "formation_config_niveauuniversitaire"


class Vocation(AbstractNomStatut):

    class Meta:
        verbose_name = u"Vocation"
        verbose_name_plural = u"Vocations"
        app_label = "formation"
        db_table = "formation_config_vocation"


class TypeFormation(AbstractNomStatut):
    class Meta:
        verbose_name = u"Type de formation"
        verbose_name_plural = u"Types de formation"
        app_label = "formation"
        db_table = "formation_config_typeformation"


class Langue(AbstractNomStatut):
    class Meta:
        verbose_name = u"Langue"
        verbose_name_plural = u"Langues"
        app_label = "formation"
        db_table = "formation_config_langue"

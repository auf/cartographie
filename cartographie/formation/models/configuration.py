#coding: utf-8

from django.db import models

from auf.django.references import models as ref


class AbstractNomStatut(models.Model):
    nom = models.CharField(max_length=150, verbose_name=u"Nom", blank=False)
    actif = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Discipline(models.Model):
    code = models.CharField(max_length=100, verbose_name=u"Code Erasmus")
    nom = models.CharField(max_length=150, verbose_name=u"Nom")
    discipline = models.ForeignKey(ref.Discipline, null=True)


class NiveauDiplome(AbstractNomStatut):
    pass


class TypeDiplome(AbstractNomStatut):
    pass


class DelivranceDiplome(AbstractNomStatut):
    pass


class NiveauUniversitaire(AbstractNomStatut):
    """
    Niveau universitaire en nombre d'années d'enseignement supérieur
    """
    pass


class Vocation(AbstractNomStatut):
    pass


class TypeFormation(AbstractNomStatut):
    pass


class Langue(AbstractNomStatut):
    pass

#coding: utf-8

from django.db import models

from auf.django.references import models as ref


class Discipline(models.Model):
    """
        Disciplines Eramus (organisées en niveaux)
        source francisée : select "Domaine de formation"
        http://www.formationsup-nordpasdecalais.fr/formations-recherche/advanced-search.html?menuKey=cdm&submenuKey=advanced
    """
    code = models.CharField(max_length=50, verbose_name="Code Erasmus")
    nom = models.CharField(max_length=150, verbose_name="Code Nom")
    discipline = models.ForeignKey(ref.Discipline, null=True)

    # config initiale ??

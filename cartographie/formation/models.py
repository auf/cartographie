#coding: utf-8

import random
import string

from django import forms
from django.db import models
from django.contrib.auth.models import User

from auf.django.references import models as ref


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', primary_key=True)
    regions = models.ManyToManyField(
        ref.Region, verbose_name=u"Régions", blank=True, null=True
    )

    class Meta:
        verbose_name = u"Profile d'utilisateur"
        verbose_name_plural = u"Profiles d'utilisateurs"

    def __unicode__(self):
        return u"%s" % self.user


class Formation(models.Model):

    class Meta:
        verbose_name = u"Formation"
        verbose_name_plural = u"Formations"

    def __unicode__(self):
        return u""

    pass


class FormationModification(models.Model):
    formation = models.ForeignKey(Formation)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"Modification d'une formation"
        verbose_name_plural = u"Modifications d'une formation"

    def __unicode__(self):
        return u"%s" % self.etablissement


class FormationCommentaire(models.Model):
    formation = models.ForeignKey(Formation)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    commentaire = models.CharField(max_length=10000, widget=forms.Textarea)

    class Meta:
        verbose_name = u"Commentaire"
        verbose_name_plural = u"Commentaires"

    def __unicode__(self):
        return u"%s" % self.commentaire


class EtablissementComposante(models.Model):
    nom = models.CharField(help_text=u"Intitulé en français de la composante")
    nom_origine = models.CharField(
        help_text=u" ".join(
            "Intitulé de la composante dans la langue d'origine ",
            "si ce n'est pas le français"
        )
    )
    sigle = models.CharField(verbose_name="Sigle de la composante")
    ville = models.CharField(
        help_text="Ville de la composante (libellé en français)"
    )
    pays = models.ForeignKey(ref.Pays, help_text="Pays de la composante")
    url = models.URLField(help_text="Site Internet de la composante")
    diplomant = models.BooleanField(
        verbose_name="La composante est diplômante?"
    )

    class Meta:
        verbose_name = u""
        verbose_name_plural = u""

    def __unicode__(self):
        return u""


class RoleComposante(models.Model):
    nom = models.CharField()

    class Meta:
        verbose_name = u""
        verbose_name_plural = u""

    def __unicode__(self):
        return u""


class FormationEtablissementComposante(models.Model):
    formation = models.ForeignKey(Formation)
    etablissementComposante = models.ForeignKey(EtablissementComposante)
    roles = models.ManyToManyField(
        RoleComposante, verbose_name=u"Rôles", blank=True, null=True
    )

    class Meta:
        verbose_name = u""
        verbose_name_plural = u""

    def __unicode__(self):
        return u""


class Personne(models.Model):
    nom = models.CharField()
    prenom = models.CharField()
    fonction = models.CharField(help_text=u"Titre ou fonction occupée")
    courriel = models.EmailField()

    class Meta:
        verbose_name = u"Personne"
        verbose_name_plural = u"Personnes"

    def __unicode__(self):
        return u"%s %s" % (self.prenom, self.nom)


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

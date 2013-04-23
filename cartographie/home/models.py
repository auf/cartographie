#coding: utf-8

from django.db import models

class FeedbackProfil(models.Model):
    nom = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nom

    class Meta:
        verbose_name = u"Profil pour feedback"
        verbose_name_plural = u"Profils pour feedback"

class Feedback(models.Model):
    courriel = models.EmailField(max_length=254)
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True,
        verbose_name=u"Prénom",
    )
    profil = models.ForeignKey("FeedbackProfil", null=True, blank=True)
    profil_autre = models.CharField(max_length=100, null=True, blank=True,
        verbose_name=u"Autre profil (le cas échéant)",
        #help_text=u"Saisir autre profil, le cas échéant",
    )
    date_envoi = models.DateField(auto_now_add=True, editable=False,
        verbose_name=u"Date d'envoi",
    )
    sujet = models.CharField(max_length=254)
    contenu = models.TextField()

    def __unicode__(self):
        return "%s %s %s" % (self.courriel, self.prenom, self.nom.upper())

    class Meta:
        pass

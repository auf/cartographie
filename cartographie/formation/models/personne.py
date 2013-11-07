# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from auf.django.references import models as ref
from cartographie.formation.models.jeton_password import JetonPassword
from cartographie.formation.models.userRole import UserRole


class Personne(models.Model):

    class Meta:
        verbose_name = u"Personne"
        verbose_name_plural = u"Personnes"
        app_label = "formation"
        db_table = "formation_personne"

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

    role = models.ForeignKey(UserRole, verbose_name=u'Rôle')

    actif = models.BooleanField(
        default=True,
        verbose_name=u"Actif?"
    )

    utilisateur = models.ForeignKey(
        User, verbose_name=u'Utilisateur', blank=False)

    jeton_password = models.ForeignKey(
        JetonPassword, verbose_name=u'Jeton de mot de passe')

    def save(self, *args, **kwargs):
        if not self.id:
            # Prendre le courriel comme username
            user = User.objects.create_user(courriel, email=courriel)
            user.password = UNUSABLE_PASSWORD
            user.save()
            self.utilisateur = user

            jeton = JetonPassword.objects.create_jeton_password()
            jeton.save()
            self.jeton_password = jeton

            _courriel_validation()
        else:
            if not self.role:
                _courriel_validation()

        return super(Personne, self).save(*args, **kwargs)

    def _courriel_validation(self):
        # FIXME
        pass

    def __unicode__(self):
        return u"%s %s" % (self.prenom, self.nom.upper())

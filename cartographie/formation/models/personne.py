# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from auf.django.references import models as ref
from cartographie.formation.models.jeton_password import JetonPassword
from cartographie.formation.models.userRole import UserRole

class CartoEtablissement(ref.Etablissement):
    def has_referent(self):
        count = Personne.objects.filter(etablissement=self, role="referent").count()
        return bool(count)

    def peut_consulter(self, user):
        """ Détermine si un utilisateur peut consulter la liste des formations
        de cet établissement"""

        # Soit qu'il est admin
        if user.is_superuser:
            return True

        # Soit qu'il a un rôle sur la région
        roles = UserRole.objects.filter(user=user,
                                        regions=self.region,
                                        type__in=(u'editeur', u"referent")).count()
        if roles:
            return True

        # Soit qu'il a un rôle sur l'établissement
        return self.a_un_role(user, u"redacteur", u"referent")


    def a_un_role(self, user, *roles):
        """ Retourne True si l'utilisateur possède l'un des rôles sur
        cet établissement"""
        try:
            personne = Personne.objects.get(utilisateur_id=user.pk,
                                            role__in=roles,
                                            etablissement__pk=self.pk)
        except Personne.DoesNotExist:
            return False
        return True

    def __eq__(self, other):
        if isinstance(other, (ref.Etablissement, CartoEtablissement)):
            return other.pk == self.pk
        return False

    def __req__(self, other):
        return self.__eq__(other)

    class Meta:
        proxy = True


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

    role = models.CharField(
        choices=UserRole.ROLE_CHOICES, max_length=25, verbose_name=u'Rôle',
        blank=True)

    actif = models.BooleanField(
        default=True,
        verbose_name=u"Actif?"
    )

    utilisateur = models.ForeignKey(
        User, verbose_name=u'Utilisateur', blank=True, null=True)

    jeton_password = models.ForeignKey(
        JetonPassword, verbose_name=u'Jeton de mot de passe', blank=True, null=True)

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

            self._courriel_validation(jeton)

        return super(Personne, self).save(*args, **kwargs)

    def _courriel_validation(self, jeton=None):
        # FIXME
        if jeton:
            print(jeton.jeton)

    def __unicode__(self):
        return u"%s %s" % (self.prenom, self.nom.upper())

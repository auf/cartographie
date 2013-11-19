# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

from auf.django.references import models as ref

from cartographie.formation.models.jeton_password import JetonPassword
from cartographie.formation.models.userRole import UserRole
from cartographie.formation.models.acces import Acces

class CartoEtablissement(ref.Etablissement):
    def has_referent(self):
        count = Personne.objects.filter(etablissement=self, role="referent").count()
        return bool(count)

    def peut_consulter(self, user):
        """ Détermine si un utilisateur peut consulter la liste des formations
        de cet établissement"""

        # L'utilisateur doit être actif
        if not user.is_active:
            return False

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
        return UserRole.a_un_role_sur_etablissement(user,
                                                    self,
                                                    u"redacteur",
                                                    u"referent")

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
            user = User.objects.create_user(self.courriel, email=self.courriel)
            user.set_unusable_password()
            user.is_active = False
            user.save()
            self.utilisateur = user

            self.envoyer_courriel_editeur()
            self.creer_jeton()

        return super(Personne, self).save(*args, **kwargs)

    def creer_jeton(self):
        jeton = JetonPassword.objects.create_jeton_password()
        jeton.save()
        self.jeton_password = jeton

    def envoyer_courriel_motdepasse(self):
        from cartographie.formation.models.formation import EnveloppeParams
        from auf.django.mailing.models import envoyer

        if not self.jeton_password:
            self.creer_jeton()
            self.save()

        params = EnveloppeParams.creer_depuis_modele("motpasse")
        params.nom = self.utilisateur.username
        params.url = reverse("formation_personne_modifier_password",
                             args=[self.jeton_password.jeton])
        params.courriel_destinataire = self.utilisateur.email
        params.save()

        #FIXME: utiliser courriel AUF
        envoyer("motpasse", "david.cormier@gmail.com")

    def envoyer_courriel_editeur(self):
        from cartographie.formation.models.formation import EnveloppeParams
        from auf.django.mailing.models import envoyer

        user_roles = UserRole.objects.filter(regions=self.etablissement.region,
                                             type=u'editeur')

        token = Acces.token_for_etablissement(self.etablissement)

        for user_role in user_roles:
            params = EnveloppeParams.creer_depuis_modele("refvalid")
            params.nom = self.utilisateur.username
            params.url = reverse('formation_personne_liste', args=[token])
            params.courriel_destinataire = user_role.user.email
            params.save()

        #FIXME: utiliser courriel AUF
        envoyer('refvalid', 'david.cormier@gmail.com')


    def _courriel_validation(self, jeton=None):
        # FIXME
        if jeton:
            print(jeton.jeton)

    def __unicode__(self):
        return u"%s %s" % (self.prenom, self.nom.upper())

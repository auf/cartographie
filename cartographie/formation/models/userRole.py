# -*- coding: utf-8 -*-
from itertools import chain, groupby

from auf.django.references import models as ref
from auf.django.permissions import Role
from cartographie.formation.constants import statuts_formation as STATUTS
from cartographie.formation.workflow import TRANSITIONS

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from .acces import Acces


class UserRole(models.Model, Role):
    """
        Rôle de User qui permet de leur associer des régions
    """

    perms = {
        'editeur': [
            'manage'
        ],

        'referent': [
            # FIXME trouver les bonnes perms pour les référents
            'manage',
        ],
    }

    ROLE_CHOICES = (
        (u'editeur', u"AUF: Éditeur"),
        (u'referent', u"Référent"),
        (u'redacteur', u"Rédacteur"),
    )

    type = models.CharField(max_length=25, choices=ROLE_CHOICES)
    user = models.ForeignKey(User, related_name='roles')
    regions = models.ManyToManyField(
        ref.Region,
        verbose_name=u"Régions",
        related_name='roles'
    )

    class Meta:
        verbose_name = u"Rôle d'usager"
        verbose_name_plural = u"Rôles d'usager"
        app_label = "formation"
        db_table = "formation_userrole"

    def __unicode__(self):
        return u""

    def has_perm(self, perm):
        return perm in self.perms[self.type]


    @staticmethod
    def a_un_role_sur_etablissement(user, etablissement, *roles):
        """ Retourne True si l'utilisateur possède l'un des rôles sur
        cet établissement"""
        from cartographie.formation.models import Personne

        try:
            personne = Personne.objects.get(utilisateur_id=user.pk,
                                            role__in=roles,
                                            etablissement__pk=etablissement.pk)
        except Personne.DoesNotExist:
            return False
        return True


    # FIXME
    # Pour éviter le  monkey patching. mettre dans User si on upgrade à Django 1.5
    @staticmethod
    def is_editeur_etablissement(user, etablissement):

        return not user.is_anonymous() and user.roles.filter(
              regions__pk=etablissement.region.pk
          ).filter(type=u'editeur').exists()


    @staticmethod
    def get_toutes_regions(user, roletype=None):
        """Retourne l'ensemble des régions couvertes
        par l'ensemble des rôles de l'utilisateur"""
        if not user:
            return []
        roles = UserRole.objects.filter(user=user)
        if roletype:
            roles = roles.filter(type=roletype)
        regions = set(chain(*(role.regions.all() for role in roles)))
        return list(regions)

    @staticmethod
    def has_permission_for_transition(user, token, formation, final_status):

        def token2etablissement(token):
            try:
                acces = Acces.objects.select_related('etablissement').get(token=token)
            except ObjectDoesNotExist:
                return None

            etablissement = acces.etablissement
            if not etablissement:
                return None
            return etablissement


        try:
            permissions = TRANSITIONS[formation.statut][final_status]['roles']
        except KeyError:
            return False

        if user.is_active and user.is_superuser:
            return True
        
        if user.is_anonymous() and 'token' in permissions:
            etablissement = token2etablissement(token)
            if etablissement and etablissement == formation.etablissement:
                return True
        
        if not user.is_active:
            return False

        if permissions:
            if UserRole.is_editeur_etablissement(user, formation.etablissement):
                return True

            if UserRole.a_un_role_sur_etablissement(user,
                                                    formation.etablissement,
                                                    *permissions):
                return True

        return False

    @staticmethod
    def get_contacts(user):
        """Retourne les contacts d'un utilisateur"""
        from .personne import Personne

        regions = UserRole.get_toutes_regions(user, roletype="editeur")

        personnes = Personne.objects.filter(role="referent",
                                            etablissement__region__in=regions).distinct()

        users = User.objects.filter(roles__regions__in=regions,
                                    roles__type="referent").distinct()

        return {
            'referents': personnes,
            'referents_regions': users,
        }





    @staticmethod
    def valid_status(user, token, formation):
        status = set()
        for statut in [STATUTS.supprimee,
                       STATUTS.en_redaction,
                       STATUTS.validee,
                       STATUTS.publiee]:
            if formation.statut != statut and \
                    UserRole.has_permission_for_transition(user, token, formation, statut):
                status.add(statut)

        return status

    def get_filter_for_perm(self, perm, model):
        if perm == "manage" and self.has_perm("manage"):
            if model in [ref.Region]:
                return models.Q(id__in=self.regions.all())

        return False

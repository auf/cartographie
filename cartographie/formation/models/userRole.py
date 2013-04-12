#coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from auf.django.references import models as ref
from auf.django.permissions import Role


class UserRole(models.Model, Role):
    """
        Rôle de User qui permet de leur associer des régions
    """

    perms = {
        'editeur': [
            'manage'
        ],
    }

    ROLE_CHOICES = (
        (u'editeur', u"AUF: Éditeur"),
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


    # FIXME
    # Pour éviter le  monkey patching. mettre dans User si on upgrade à Django 1.5
    @staticmethod
    def is_editeur_etablissement(user, etablissement):
        return not user.is_anonymous() and len(user.roles.filter(
              regions__pk=etablissement.region.pk
          ).filter(type=u'editeur')) > 0

    @staticmethod
    def peut_modifier_workflow(user, etablissement):
        """
            Retourne True si l'utilisateur peut modifier
            le workflow d'une formation de cet etablissement
        """
        return user and UserRole.is_editeur_etablissement(user, etablissement)\
            or user.is_superuser

    def get_filter_for_perm(self, perm, model):
        if perm == "manage" and self.has_perm("manage"):
            if model in [ref.Region]:
                return models.Q(id__in=self.regions.all())

        return False

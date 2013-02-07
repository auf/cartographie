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

    def has_perm(self, perm):
        return perm in self.perms[self.type]

    def get_filter_for_perm(self, perm, model):
        if perm == "manage" and self.has_perm("manage"):
            if model in [ref.Region]:
                return models.Q(id__in=self.regions.all())

        return False

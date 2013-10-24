from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from .formation import Formation
import os.path

def filename(instance, filename):
    return os.path.join('etablissements', str(instance.formation.etablissement.id), 'formations', str(instance.formation.id), filename)

class Fichier(models.Model):

    formation = models.ForeignKey(Formation, verbose_name=u"Formation")

    file = models.FileField(upload_to=filename,
                            storage=FileSystemStorage(location=settings.UPLOAD_DIRECTORY),
                            verbose_name=u"Fichier",
                            help_text=u"Fichier joint a la formation")

    is_public = models.BooleanField(
        default=True,
        verbose_name=u"Public?",
        help_text=u"Cocher si le fichier est public",
        )

    nom = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=u"Nom du fichier",
        help_text=u"Indiquer le titre du fichier"
        )

    def __unicode__(self):
        return u"%s" % self.nom

    class Meta:
        verbose_name = u"Fichiers"
        verbose_name_plural = u"Fichier"
        app_label = "formation"
        db_table = "formation_fichier"

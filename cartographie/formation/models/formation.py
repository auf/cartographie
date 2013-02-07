#coding: utf-8

import datetime

from django.db import models
from django.contrib.auth.models import User

from auf.django.references import models as ref

from . import Discipline, EtablissementComposante, Personne


class Formation(models.Model):
    """
        Formation entièrement ou partiellement en français dispensée par un
        établissement membre de l'AUF
    """

    # identification
    nom = models.CharField(
        max_length=250,
        help_text=u"Intitulé en français de la formation"
    )
    nom_origine = models.CharField(
        verbose_name=u"Nom d'origine",
        max_length=250,
        help_text=u" ".join([
            u"Intitulé de la formation dans la langue d'origine",
            u"si ce n'est pas le français"
        ])
    )
    sigle = models.CharField(
        max_length=50,
        verbose_name=u"Sigle de la formation",
        help_text=u"Abbréviation du nom de la formation"
    )
    url = models.URLField(
        help_text=u"Lien Internet vers une page présentant la formation"
    )
    discipline_1 = models.ForeignKey(Discipline, null=True)
    discipline_2 = models.ForeignKey(Discipline, null=True)
    discipline_3 = models.ForeignKey(Discipline, null=True)

    # etablissement(s)
    etablissement = models.ForeignKey(
        ref.Etablissement,
        verbose_name=u"Structure d'accueil",
        help_text=u"Établissement dispensant cette formation"
    )

    etablissement_emet_diplome = models.BooleanField(
        default=True,
        verbose_name=u"Émet diplôme ?",
        help_text=u"".join([
            u"Cocher si cet établissement émet un diplôme pour cette formation"
        ])
    )

    etablissement_composante = models.ManyToManyField(
        "FormationComposante", through="Etablissement"
    )

    # TODO: quel through ?
    partenaires_auf = models.ManyToManyField(
        "FormationPartenaireAUF", through=""
    )

    # TODO: quel through ?
    partenaires_autres = models.ManyToManyField(
        "FormationPartenaireAutre", through=""
    )

    # Diplôme
    niveau_diplome = models.ForeignKey(
        "NiveauDiplome",
        limit_choices_to={"actif": True}
    )
    type_diplome = models.ForeignKey(
        "TypeDiplome", verbose_name=u"Type de diplôme",
        limit_choices_to={"actif": True}
    )
    delivrance_diplome = models.ForeignKey(
        "DelivranceDiplome", verbose_name=u"Délivrance du diplôme",
        limit_choices_to={"actif": True}
    )
    niveau_entree = models.ManyToManyField(
        "NiveauUniversitaire", verbose_name=u"Niveau d'entrée",
        help_text=u"Nombre d'années d'enseignement supérieur",
        limit_choices_to={"actif": True}
    )
    niveau_sortie = models.ManyToManyField(
        "NiveauUniversitaire", verbose_name=u"Niveau de sortie",
        help_text=u"Nombre d'années d'enseignement supérieur",
        limit_choices_to={"actif": True}
    )
    vocation = models.ManyToManyField(
        "Vocation",
        limit_choices_to={"actif": True}
    )

    # Organisation de la formation
    presentation = models.CharField(
        max_length=500,
        verbose_name=u"Présentation de la formation",
        help_text=u" ".join([
            u"Informations clés pour valoriser la formation",
            u"(500 caractères maximum)"
        ])
    )
    type_formation = models.ForeignKey(
        "TypeFormation",
        verbose_name=u"Type de formation",
        limit_choices_to={"actif": True}
    )
    langue = models.ManyToManyField(
        "langue", verbose_name=u"Langue(s) d'enseignement",
        limit_choices_to={"actif": True}
    )
    duree = models.IntegerField(verbose_name=u"Durée de la formation en heure")

    # limiter les responsables et les contacts au personne du meme
    # etablissement que la formation courante
    responsables = models.ManyToManyField(
        Personne,
        limit_choices_to={
            "actif": True,
            "personne__etablissement": BaseModel.etablissement
        }
    )
    contacts = models.ManyToManyField(
        Personne,
        limit_choices_to={
            "actif": True,
            "personne__etablissement": BaseModel.etablissement
        }
    )

    # gestion
    date_creation = models.DateTimeField(editable=False)
    date_modification = models.DateTimeField(editable=False)
    modifications = models.ManyToManyField("FormationModification")
    commentaires = models.ManyToManyField("FormationCommentaire")

    class Meta:
        verbose_name = u"Formation"
        verbose_name_plural = u"Formations"

    def __unicode__(self):
        return u""

    def save(self, *args, **kwargs):
        # sauvegarder le champ de création seulement lors de la création
        if not self.id:
            self.date_creation = datetime.datetime.now()
        # sauvegarder la date de modification à chaque sauvegarde
        self.date_modification = datetime.datetime.now()

        super(Formation, self).save(*args, **kwargs)


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
    user = models.ForeignKey(User, null=True)
    user_display = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    commentaire = models.CharField(max_length=10000)  # , widget=forms.Textarea

    class Meta:
        verbose_name = u"Commentaire"
        verbose_name_plural = u"Commentaires"

    def __unicode__(self):
        return u"%s" % self.commentaire

    def save(self, *args, **kwargs):
        if self.user:
            # sauvegarder un affichage personnalisé de l'usager qui a fait
            # le commentaire
            self.user_display = u"%s %s" % (
                self.user.firstname, self.user.lastname.upper()
            )
        super(FormationCommentaire, self).save(*args, **kwargs)


class EtablissementComposante(models.Model):
    nom = models.CharField(max_length=150, help_text=u"Intitulé en français de la composante")
    pass


class FormationComposante(models.Model):
    formation = models.ForeignKey(Formation)
    etablissementComposante = models.ForeignKey(EtablissementComposante)

    # roles = models.ManyToManyField(
    #     RoleComposante, verbose_name=u"Rôles", blank=True, null=True
    # )

    class Meta:
        verbose_name = u""
        verbose_name_plural = u""

    def __unicode__(self):
        return u""


class RoleComposante(models.Model):
    nom = models.CharField(max_length=100)

    class Meta:
        verbose_name = u""
        verbose_name_plural = u""

    def __unicode__(self):
        return u""

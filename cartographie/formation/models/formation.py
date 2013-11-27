#coding: utf-8

from collections import defaultdict
import datetime

from django.db import models
from django.db.models import signals, Q, Count
from django.contrib.auth.models import User

from .configuration import (
    Discipline, NiveauDiplome, TypeDiplome, DelivranceDiplome,
    NiveauUniversitaire, Vocation, TypeFormation, Langue)
from .etablissement import EtablissementComposante, EtablissementAutre
from .personne import Personne
from .workflow import WorkflowMixin
from auf.django.mailing.models import ModeleCourriel, Enveloppe
from auf.django.references import models as ref
from cartographie.formation.signals.formation import formation_is_valider
from cartographie.utils.copymixin import CopyMixin


class EnveloppeParams(models.Model):

    enveloppe = models.ForeignKey(Enveloppe, related_name="auf_enveloppe")

    nom = models.CharField(max_length=50)

    url = models.TextField()

    courriel_destinataire = models.EmailField()

    def get_corps_context(self):

        return {'nom': self.nom,
                'adresse_validation': self.url}

    def get_adresse(self):
        return self.courriel_destinataire

    @classmethod
    def creer_depuis_modele(cls, code_modele):
        """ Créée l'enveloppe en même temps que les paramètres"""

        instance = cls()
        modele = ModeleCourriel.objects.get(code=code_modele)
        enveloppe = Enveloppe(modele=modele)
        enveloppe.save()
        instance.enveloppe = enveloppe
        return instance

    class Meta(object):
        app_label = 'formation'


class Formation(CopyMixin, WorkflowMixin, models.Model):
    """Formation entièrement ou partiellement en français dispensée par un
    établissement membre de l'AUF"""

    nom = models.CharField(
        max_length=250,
        verbose_name=u"Intitulé de la formation en français",
        help_text=u"Intitulé de la formation en français",
        blank=False
    )

    nom_origine = models.CharField(
        verbose_name=u"Intitulé de la formation dans la langue d'origine",
        max_length=250,
        null=True,
        blank=True,
        help_text=u" ".join([
            u"Intitulé de la formation dans la langue d'origine",
            u"si ce n'est pas le français"
        ])
    )

    sigle = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=u"Sigle de la formation",
        help_text=u"Indiquer ici le sigle de la formation s'il existe"
    )

    url = models.URLField(
        null=True,
        blank=True,
        verbose_name=u"Lien Internet",
        help_text=u"Lien Internet vers une page présentant la formation"
    )

    discipline_1 = models.ForeignKey(
        Discipline, blank=False, related_name="+",
        help_text=u"""Indiquer une discipline minimum, trois disciplines
                  au maximum (choisir une des valeurs proposées)""",
        limit_choices_to={"actif": True}
    )

    discipline_2 = models.ForeignKey(
        Discipline, null=True, blank=True, related_name="+",
        help_text=u"""Indiquer une discipline minimum, trois disciplines
                  au maximum (choisir une des valeurs proposées)""",
        limit_choices_to={"actif": True}
    )

    discipline_3 = models.ForeignKey(
        Discipline, null=True, blank=True, related_name="+",
        help_text=u"""Indiquer une discipline minimum, trois disciplines
                  au maximum (choisir une des valeurs proposées)""",
        limit_choices_to={"actif": True}
    )

    etablissement = models.ForeignKey(
        ref.Etablissement,
        verbose_name=u"Structure d'accueil",
        help_text=u"Établissement dispensant cette formation",
        blank=False
    )

    etablissement_emet_diplome = models.BooleanField(
        default=True,
        verbose_name=u"Émet diplôme ?",
        help_text=u"".join([
            u"Cocher si cet établissement émet un diplôme pour cette formation"
        ])
    )

    etablissement_composante = models.ManyToManyField(
        EtablissementComposante,
        related_name="+",
        null=True,
        blank=True,
        through="FormationComposante",
        verbose_name=u"Composante d'établissement",
        help_text=u"Texte d'aide",
    )

    partenaires_auf = models.ManyToManyField(
        ref.Etablissement,
        related_name="+",
        null=True,
        blank=True,
        through="FormationPartenaireAUF",
        verbose_name=u"Partenaires membre de l'AUF",
        help_text=u"Texte d'aide"
    )

    partenaires_autres = models.ManyToManyField(
        EtablissementAutre,
        related_name="+",
        null=True,
        blank=True,
        through="FormationPartenaireAutre",
        verbose_name=u"""Partenaires <strong class='text-info'>non
            membre</strong> de l'AUF""",
        help_text=u"Texte d'aide"
    )

    niveau_diplome = models.ForeignKey(
        NiveauDiplome,
        null=True,
        blank=True,
        limit_choices_to={"actif": True},
        related_name="+",
        verbose_name=u"Niveau de diplôme",
        help_text=u"Choisir une des valeurs proposées"
    )

    type_diplome = models.ForeignKey(
        TypeDiplome,
        null=True,
        blank=True,
        limit_choices_to={"actif": True},
        related_name="+",
        verbose_name=u"Type de diplôme",
        help_text=u"Choisir une des valeurs proposées"
    )

    delivrance_diplome = models.ForeignKey(
        DelivranceDiplome,
        null=True,
        blank=True,
        limit_choices_to={"actif": True},
        related_name="+",
        verbose_name=u"Délivrance du diplôme",
        help_text=u"Choisir une des valeurs proposées"
    )

    niveau_entree = models.ManyToManyField(
        NiveauUniversitaire,
        null=True,
        blank=True,
        limit_choices_to={"actif": True},
        related_name="niveau_entree+",
        verbose_name=u"Niveau d'entrée",
        help_text=u"""Niveau requis pour pouvoir s'inscrire
                  dans la formation souhaitée, en nombre d'années d'études
                  dans l'enseignement supérieur""",
    )

    niveau_sortie = models.ForeignKey(
        NiveauUniversitaire,
        null=True,
        blank=True,
        verbose_name=u"Niveau de sortie",
        help_text=u"""Niveau obtenu à l'issue de la formation souhaitée,
                  en nombre d'années d'études
                  dans l'enseignement supérieur""",
        limit_choices_to={"actif": True},
    )

    vocation = models.ManyToManyField(
        Vocation,
        null=True,
        blank=True,
        limit_choices_to={"actif": True},
        related_name="vocation+"
    )

    # Organisation de la formation
    presentation = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=u"Présentation de la formation",
        help_text=u" ".join([
            u"Informations clés pour valoriser la formation",
            u"(500 caractères maximum)"
        ])
    )

    type_formation = models.ForeignKey(
        TypeFormation,
        null=True,
        blank=True,
        verbose_name=u"Déroulement de la formation",
        help_text=u"Choisir une des valeurs proposées",
        limit_choices_to={"actif": True},
        related_name="type_formation+"
    )

    langue = models.ManyToManyField(
        Langue,
        null=True,
        blank=True,
        verbose_name=u"Langue(s) d'enseignement",
        help_text=u"""Indiquer la ou les langues dans lesquelles se déroulent
                  les enseignements de la formation. Vous pouvez ajouter
                  une nouvelle langue à la liste en cliquant sur le bouton
                  ci-dessous.""",
        limit_choices_to={"actif": True},
        related_name="langue+"
    )

    duree = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=u"Durée de la formation",
        help_text=u"""Précisez la durée minimale nécessaire pour l'obtention
                  du diplôme en nombre d'années d'études"""
    )

    # limiter les responsables et les contacts au personne du meme
    # etablissement que la formation courante
    responsables = models.ManyToManyField(
        Personne,
        null=True,
        blank=True,
        limit_choices_to={
            "actif": True,
            # "personne__etablissement": self.etablissement
        },
        related_name="responsables+",
        help_text=u"""Sélectionnez une personne dans la liste déroulante. Vous
            pouvez ajouter une nouvelle personne à la liste en cliquant sur le
            bouton ci-dessous."""

    )

    contacts = models.ManyToManyField(
        Personne,
        null=True,
        blank=True,
        limit_choices_to={
            "actif": True,
            # "personne__etablissement": self.etablissement
        },
        related_name="contacts+",
        help_text=u"""Sélectionnez une personne dans la liste déroulante. Vous
            pouvez ajouter une nouvelle personne à la liste en cliquant sur le
            bouton ci-dessous."""
    )

    # gestion
    date_creation = models.DateTimeField(auto_now_add=True, editable=False)
    date_modification = models.DateTimeField(editable=False)

    modifications = models.ManyToManyField(
        "FormationModification",
        null=True,
        blank=True,
        related_name="modifications+"
    )

    commentaires = models.ManyToManyField(
        "FormationCommentaire",
        null=True,
        blank=True,
        related_name="commentaires+"
    )

    brouillon = models.OneToOneField('self', related_name='publication_originale', null=True)

    class Meta:
        verbose_name = u"Formation"
        verbose_name_plural = u"Formations"
        app_label = "formation"
        db_table = "formation_formation"
        ordering = ["etablissement"]

    def __unicode__(self):
        return u"%s" % (self.nom,)

    def save_modification(self, request):
        modif = FormationModification()

        if request.user.is_authenticated():
            modif.save_modification(self.id, request.user)
        else:
            modif.save_modification(self.id)

    content_fields = [
        'nom_origine', 'sigle', 'url', 'discipline_1', 'discipline_2',
        'discipline_3', 'niveau_diplome', 'type_diplome', 'delivrance_diplome',
        'niveau_entree', 'niveau_sortie', 'vocation', 'presentation',
        'type_formation', 'langue', 'duree', 'responsables', 'contacts',
    ]

    def save(self, *args, **kwargs):
        # Mettre à jour la date de modification lorsque le contenu est modifié

        if self.pk is not None:
            orig = Formation.objects.get(pk=self.pk)
            orig_fields = [
                getattr(orig, field) for field in self.content_fields]
            self_fields = [
                getattr(self, field) for field in self.content_fields]
            changed = [x != y for x, y in zip(orig_fields, self_fields)]

            if any(changed):
                self.date_modification = datetime.datetime.now()
        else:
            self.date_modification = datetime.datetime.now()

        super(Formation, self).save(*args, **kwargs)

    @staticmethod
    def num_formations_per_country():

        def result2pair(result):
            return (
                result['etablissement__pays__code_iso3'].lower(),
                result['count']
            )

        # On doit passer par Formation.objects parce que
        # 'related_name' = '+' dans EtablissementBase pour la colonne
        # 'pays'.

        query = Formation.objects.values('etablissement__pays__code_iso3')\
            .exclude(statut=999)\
            .annotate(count=Count('etablissement__pays__code_iso3'))

        return dict(map(result2pair, query))


class FormationModification(models.Model):
    formation = models.ForeignKey(Formation)
    user = models.ForeignKey(User, null=True, blank=True, related_name="+")
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"Modification d'une formation"
        verbose_name_plural = u"Modifications d'une formation"
        app_label = "formation"
        db_table = "formation_formationmodification"
        ordering = ['-date']

    def __unicode__(self):
        return u"%s" % (self.date)

    def save_modification(self, formation_id, user=None):
        """
            Permet d'enregistrer une modification dans une fiche
        """
        self.formation = Formation.objects.get(id=formation_id)

        if user:
            self.user = user

        self.save()


class FormationCommentaire(models.Model):
    formation = models.ForeignKey(Formation, related_name="+")
    user = models.ForeignKey(User, null=True, related_name="+")
    user_display = models.CharField(max_length=150, blank=False)
    date = models.DateTimeField(auto_now=True)
    commentaire = models.CharField(
        verbose_name=u"Commentaire",
        max_length=10000
    )

    class Meta:
        verbose_name = u"Commentaire"
        verbose_name_plural = u"Commentaires"
        app_label = "formation"
        db_table = "formation_formationcommentaire"

    def __unicode__(self):
        return u"%s" % self.commentaire

    def get_form_with_data(self):

        from cartographie.formation.forms.formation \
            import FormationCommentaireForm

        return FormationCommentaireForm(instance=self)

    def save(self, *args, **kwargs):
        if self.user:
            # sauvegarder un affichage personnalisé de l'usager qui a fait
            # le commentaire
            self.user_display = u"%s %s" % (
                self.user.first_name, self.user.last_name.upper()
            )
        super(FormationCommentaire, self).save(*args, **kwargs)

    def peut_modifier(self, user):
        return user.is_active and (user.is_superuser or self.user == user)


class FormationComposante(models.Model):
    formation = models.ForeignKey(Formation)
    etablissementComposante = models.ForeignKey(
        EtablissementComposante,
        related_name="+",
        verbose_name=u"Composante d'établissement",
        limit_choices_to={"actif": True}
    )

    etablissement_composante_emet_diplome = models.BooleanField(
        default=False,
        verbose_name=u"Émet diplôme?",
        help_text=u" ".join([
            u"Cocher si cette composante émet un diplôme pour cette formation"
        ])
    )

    class Meta:
        verbose_name = u"Composante de formation"
        verbose_name_plural = u"Composantes de formation"
        app_label = "formation"
        db_table = "formation_formationcomposante"

    def __unicode__(self):
        return u""


class FormationPartenaireAUF(models.Model):
    formation = models.ForeignKey(Formation)
    etablissement = models.ForeignKey(
        ref.Etablissement,
        limit_choices_to={
            "membre": True, "actif": True
        },
        related_name="+"
    )
    partenaire_auf_emet_diplome = models.BooleanField(
        default=False,
        verbose_name=u"Émet diplôme?",
        help_text=u" ".join([
            u"Cocher si ce partenaire membre de l'AUF émet un diplôme",
            u"pour cette formation"
        ])
    )

    class Meta:
        verbose_name = u"Formation d'un partenaire membre de l'AUF"
        verbose_name_plural = u"Formations d'un partenaire membre de l'AUF"
        app_label = "formation"
        db_table = "formation_formationpartenaireauf"

    def __unicode__(self):
        return u""


class CourrielRappel(ModeleCourriel):
    periode = models.CharField(max_length=50)
    actif = models.BooleanField()

    class Meta:
        verbose_name = u"Rappel actualisation de formations"
        verbose_name_plural = u"Rappel actualisation de formations"
        app_label = "formation"
        db_table = "formation_courrielrappel"


class FormationPartenaireAutre(models.Model):
    formation = models.ForeignKey(Formation)
    etablissement = models.ForeignKey(
        EtablissementAutre,
        related_name="+"
    )
    partenaire_autre_emet_diplome = models.BooleanField(
        default=False,
        verbose_name=u"Émet diplôme?",
        help_text=u" ".join([
            u"Cocher si ce partenaire non membre de l'AUF émet un diplôme",
            u"pour cette formation"
        ])
    )

    class Meta:
        verbose_name = u"Formation de partenaire autres"
        verbose_name_plural = u"Formations de partenaire autres"
        app_label = "formation"
        db_table = "formation_formationpartenaireautre"

    def __unicode__(self):
        return u""

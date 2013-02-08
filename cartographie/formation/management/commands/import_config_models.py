#coding: utf-8

from django.core.management.base import BaseCommand
from .models import Discipline, NiveauDiplome, TypeDiplome, \
                    DelivranceDiplome, NiveauUniversitaire, \
                    Vocation, TypeFormation

# Données de base pour les models qui feront parti de l'admin Django
# de cet app.
niveaux_diplome = [
    u"Master", u"DEA", u"Doctorat"
]
types_diplome = [
    u"Diplôme national", u"Diplôme de la structure d'accueil", u"Certificat"
]
delivrances_diplome = [
    u"Structure d'accueil", u"Organisme partenaire",
    u"Codiplôme", u"Double diplôme"
]
niveaux_universitaire = [
    "1", "2", "3", "4", "5", "6", "Plus de 6"
]
vocations = [
    u"Professionnel", u"Recherche"
]
types_formation = [
    u"Présentiel", "À distance", "Mixte"
]
langues = [
    "Français", "Anglais", "Arabe", u"Espagnol", u"Portugais"
]


def ajouter_data_au_modele(model, data):
    """
        Fonction d'import.

        @model: le modele auquelle on veut ajouter des données
        @data: les données sous forme de list
    """

    for d in data:
        filtered_model = model.objects.filter(nom=d).all()
        if len(filtered_model) == 0:
            nouveau_model = model()
            nouveau_model.nom = d
            nouveau_model.save()


class Command(BaseCommand):
    help = u"""
        Fais un import de base dans les models de configuration
    """

    def handle(self, *args, **options):
        self.stdout.write(
            "Début de l'importation des Models de configuration\n"
        )

        self.stdout.write("Importation: NiveauDiplome\n")
        ajouter_data_au_modele(NiveauDiplome, niveaux_diplome)
        self.stdout.write("Importation: TypeDiplome\n")
        ajouter_data_au_modele(TypeDiplome, types_diplome)
        self.stdout.write("Importation: DelivranceDiplome\n")
        ajouter_data_au_modele(DelivranceDiplome, delivrances_diplome)
        self.stdout.write("Importation: NiveauUniversitaire\n")
        ajouter_data_au_modele(NiveauUniversitaire, niveaux_universitaire)
        self.stdout.write("Importation: Vocation\n")
        ajouter_data_au_modele(Vocation, vocations)
        self.stdout.write("Importation: TypeFormation\n")
        ajouter_data_au_modele(TypeFormation, types_formation)

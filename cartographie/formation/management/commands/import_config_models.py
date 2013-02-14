#coding: utf-8

import csv, os, sys

from django.core.management.base import BaseCommand
from formation.models import Discipline, NiveauDiplome, TypeDiplome, \
                    DelivranceDiplome, NiveauUniversitaire, \
                    Vocation, TypeFormation, Langue


class Command(BaseCommand):
    help = u"""
        Fais un import de base dans les models de configuration
    """

    def handle(self, *args, **options):
        self.stdout.write(
            "Début de l'importation des Models de configuration\n"
        )
        # import des discipline
        self.stdout.write("Importation: Discipline\n")
        self._ajouter_data_discipline("formation_disciplines.csv")

        # import des autres
        self.stdout.write("Importation: NiveauDiplome\n")
        self._ajouter_data_au_modele("formation_niveaudiplome.csv", NiveauDiplome)
        self.stdout.write("Importation: TypeDiplome\n")
        self._ajouter_data_au_modele("formation_typediplome.csv", TypeDiplome)
        self.stdout.write("Importation: DelivranceDiplome\n")
        self._ajouter_data_au_modele("formation_delivrancediplome.csv", DelivranceDiplome)
        self.stdout.write("Importation: NiveauUniversitaire\n")
        self._ajouter_data_au_modele("formation_niveauuniversitaire.csv", NiveauUniversitaire)
        self.stdout.write("Importation: Vocation\n")
        self._ajouter_data_au_modele("formation_vocation.csv", Vocation)
        self.stdout.write("Importation: TypeFormation\n")
        self._ajouter_data_au_modele("formation_typeformation.csv", TypeFormation)
        self.stdout.write("Importation: Langue\n")
        self._ajouter_data_au_modele("formation_langue.csv", Langue)

    def _ajouter_data_au_modele(self, filename, model):
        """
            Fonction d'import.

            @model: le modele auquelle on veut ajouter des données
            @data: les données sous forme de list
        """

        path = os.getcwd()
        path = os.path.join(path, "cartographie", "formation", "data", filename)

        self.stdout.write("%s\n" % path)

        with open(path, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')

            for d in reader:
                self.stdout.write("%s\n" % str(d))

                nom = d[0].strip()
                actif = True if d[1].strip() == "True" else False

                filtered_model = model.objects.filter(nom=nom).all()

                if len(filtered_model) == 0:
                    nouveau_model = model()
                    nouveau_model.nom = nom
                    nouveau_model.actif = actif
                    nouveau_model.save()

    def _ajouter_data_discipline(self, filename):
        path = os.getcwd()
        path = os.path.join(path, "cartographie", "formation", "data", filename)

        self.stdout.write("%s\n" % path)

        with open(path, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')

            for d in reader:
                self.stdout.write("%s\n" % str(d))

                code = d[0].strip()
                nom = d[1].strip()
                actif = None if d[2].strip() == "NULL" else None

                filtered_disci = Discipline.objects.filter(nom=nom).all()

                if len(filtered_disci) == 0:
                    nouveau_disci = Discipline()
                    nouveau_disci.code = code
                    nouveau_disci.nom = nom
                    nouveau_disci.discipline = actif
                    nouveau_disci.save()
        pass

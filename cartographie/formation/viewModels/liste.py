# coding: utf-8

from cartographie.formation.models import Acces, Formation, Personne, \
                                          FormationPartenaireAutre, \
                                          FormationComposante


class ListeViewModel(object):
    onglet_actif = None
    token = None
    etablissement = None
    formations = []
    personnes = []
    partenaires_autres = []
    composantes = []

    def __init__(self, token, onglet_actif="formation"):
        if token:
            self.token = token
            acces = Acces.objects.filter(token=token)[0]

            self.etablissement = acces.etablissement
            self.onglet_actif = onglet_actif

            # filtrer les formations pour ceux de l'établissement courant
            self.formations = Formation.objects.filter(
                etablissement=self.etablissement
            ).order_by("nom")

            self.personnes = Personne.objects.filter(
                etablissement=self.etablissement
            ).order_by("nom")

            self.partenaires_autres = FormationPartenaireAutre.objects.filter(
                etablissement=self.etablissement
            ).order_by("etablissement__nom")

            self.composantes = FormationComposante.objects.all().order_by(
                "etablissementComposante__nom"
            )

    def get_data(self):
        return {
            "onglet_actif": self.onglet_actif,
            "token": self.token,
            "etablissement": self.etablissement,
            "formations": self.formations,
            "personnes": self.personnes,
            "partenaires_autres": self.partenaires_autres,
            "composantes": self.composantes
        }

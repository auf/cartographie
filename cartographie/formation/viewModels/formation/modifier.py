# coding: utf-8

from django.forms.models import inlineformset_factory

from cartographie.formation.models import Acces, Formation
from cartographie.formation.models import FormationComposante
from cartographie.formation.models import FormationPartenaireAUF
from cartographie.formation.models import FormationPartenaireAutre

from cartographie.formation.forms.formation import FormationForm
from cartographie.formation.forms.formation import FormationComposanteForm


class ModifierViewModel(object):
    """
        Les données nécessaires à la view "modifier" et "modifier_etablissements"
        sont obtenus et gérés ici.
    """

    token = None
    acces = None
    etablissement = None
    formation = None
    form = None

    composanteFormset = None
    partenaireAufFormset = None
    partenaireAutreFormset = None

    def __init__(self, request, token, formation_id, presence_formsets=False):
        if token:
            self.token = token
            self.acces = Acces.objects.get(token=token)
            self.etablissement = self.acces.etablissement
            self.formation = Formation.objects.get(pk=formation_id)

            # setup des formsets

            # ici, je spécifie un form particulier car je veux limiter la liste
            # de choix des EtablissementComposante. On ne peut le faire que dans
            # un ModelForm lors du __init__
            composanteFormset = inlineformset_factory(
                Formation, FormationComposante,
                form=FormationComposanteForm, extra=1
            )

            partenaireAufFormset = inlineformset_factory(
                Formation, FormationPartenaireAUF, extra=1
            )
            partenaireAutreFormset = inlineformset_factory(
                Formation, FormationPartenaireAutre, extra=1
            )

            presence_etablissement = presence_formsets

            if request.method == "POST":
                # gestion du formulaire de base d'une fiche
                self.form = FormationForm(
                    self.etablissement,
                    presence_etablissement,
                    request.POST,
                    instance=self.formation
                )

                # l'utilisation du parametre "prefix" sur les objets
                # {whatever}Formset est obligatoire pour des formsets multiples
                # dans un même formulaire
                if presence_formsets:
                    # si ce if n'est pas présent dans le contexte ou on fait un
                    # post sans les formsets, il nous avertit que les données
                    # des formsets ne sont pas présents...

                    # gestion des formsets dans l'onglet "Établissement(s)"
                    self.composanteFormset = composanteFormset(
                        request.POST,
                        instance=self.formation,
                        prefix="composante"
                    )
                    self.partenaireAufFormset = partenaireAufFormset(
                        request.POST,
                        instance=self.formation,
                        prefix="partenaires-auf"
                    )
                    self.partenaireAutreFormset = partenaireAutreFormset(
                        request.POST,
                        instance=self.formation,
                        prefix="partenaires-autre"
                    )
            else:
                # init de base des formulaires et des formsets
                self.form = FormationForm(
                    self.etablissement,
                    presence_etablissement,
                    instance=self.formation
                )
                self.composanteFormset = composanteFormset(
                    instance=self.formation,
                    prefix="composante"
                )
                self.partenaireAufFormset = partenaireAufFormset(
                    instance=self.formation,
                    prefix="partenaires-auf"
                )
                self.partenaireAutreFormset = partenaireAutreFormset(
                    instance=self.formation,
                    prefix="partenaires-autre"
                )

    def get_data(self):
        return {
            "token": self.token,
            "etablissement": self.etablissement,
            "form": self.form,
            "formation": self.formation,
            "composanteFormset": self.composanteFormset,
            "partenaireAufFormset": self.partenaireAufFormset,
            "partenaireAutreFormset": self.partenaireAutreFormset
        }

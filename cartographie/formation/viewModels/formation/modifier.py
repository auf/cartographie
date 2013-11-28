# -*- coding: utf-8 -*-

from django.forms.models import inlineformset_factory


from cartographie.formation.models import Acces, Formation, UserRole
from cartographie.formation.models import (
    FormationComposante, EtablissementComposante, EtablissementAutre)
from cartographie.formation.models import FormationPartenaireAUF
from cartographie.formation.models import FormationPartenaireAutre

from cartographie.formation.constants import statuts_formation
from cartographie.formation.forms.formation \
    import FormationForm

from .base import BaseModifierViewModel


class ModifierViewModel(BaseModifierViewModel):
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
        super(ModifierViewModel, self).__init__(request, token, formation_id)
        if token:
            self.token = token
            self.acces = Acces.objects.get(token=token)
            self.etablissement = self.acces.etablissement

            etablissement_courant = self.etablissement

            def limiter_choix_etablissement(field, **kwargs):
                """
                    Cette fonction est utilisé en callback par inlineformset_factory

                    Je m'en sers pour limiter les choix d'EtablissementComposante
                    à l'établissement courant.
                """
                if field.name == 'etablissementComposante':
                    formfield = field.formfield()
                    # refaire le queryset
                    formfield.queryset = EtablissementComposante.objects.filter(
                        etablissement=etablissement_courant, actif=True
                    )
                    return formfield

                return field.formfield()

            def limiter_choix_partenaire_autre(field, **kwargs):
                """
                    Limite les choix des partenaires non nembres de l'AUF

                    aux partenaires qui sont associés à l'établissement qui donne
                    la formation
                """
                if field.name == 'etablissement':
                    formfield = field.formfield()
                    formfield.queryset = EtablissementAutre.objects.all()
                    return formfield

                elif field.name == 'partenaire_autre_emet_diplome':
                    return field.formfield()

            # setup des formsets
            composanteFormset = inlineformset_factory(
                Formation, FormationComposante,
                extra=1,
                formfield_callback=limiter_choix_etablissement
            )

            partenaireAufFormset = inlineformset_factory(
                Formation, FormationPartenaireAUF, extra=1
            )
            partenaireAutreFormset = inlineformset_factory(
                Formation, FormationPartenaireAutre, extra=1,
                formfield_callback=limiter_choix_partenaire_autre
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
        data = super(ModifierViewModel, self).get_data()
        data.update({
                "token": self.token,
                "etablissement": self.etablissement,
                "form": self.form,
                "formation": self.formation,
                "composanteFormset": self.composanteFormset,
                "partenaireAufFormset": self.partenaireAufFormset,
                "partenaireAutreFormset": self.partenaireAutreFormset,
                "statuts_formation": statuts_formation,
                })
        return data

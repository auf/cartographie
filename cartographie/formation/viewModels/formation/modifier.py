# coding: utf-8

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import inlineformset_factory


from cartographie.formation.models import Acces, Formation, FormationCommentaire
from cartographie.formation.models import FormationComposante, EtablissementComposante
from cartographie.formation.models import FormationPartenaireAUF
from cartographie.formation.models import FormationPartenaireAutre

from cartographie.formation.constants import statuts_formation
from cartographie.formation.forms.formation \
    import FormationForm, FormationCommentaireForm

from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel


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
            "partenaireAutreFormset": self.partenaireAutreFormset,
            "statuts_formation": statuts_formation
        }


class CommentaireViewModel(BaseAjouterViewModel):
    formation = None
    form = None
    commentaires = []

    def __init__(self, request, token, formation_id):
        super(CommentaireViewModel, self).__init__(request, token)
        self.formation = Formation.objects.get(pk=formation_id)
        self.commentaires = FormationCommentaire.objects.filter(
            formation=self.formation
        ).order_by("date")

        if request.method == "POST":
            self.form = FormationCommentaireForm(request.POST)
        else:
            self.form = FormationCommentaireForm()

    def get_data(self):
        data = super(CommentaireViewModel, self).get_data()
        data.update({
            "formation": self.formation,
            "statuts_formation": statuts_formation,
            "commentaires": self.commentaires,
            "form": self.form
        })
        return data


class CommentaireSupprimerViewModel(BaseAjouterViewModel):
    redirect_url = None
    success = False

    def __init__(self, request, token, formation_id, commentaire_id):
        super(CommentaireSupprimerViewModel, self).__init__(request, token)

        self.redirect_url = reverse(
            "formation_modifier_commentaires",
            args=[token, formation_id]
        )

        try:
            commentaire_courant = FormationCommentaire.objects.get(
                pk=commentaire_id
            )
        except ObjectDoesNotExist:
            self.success = False
        else:
            # si l'id du user courant concorde avec l'id de l'auteur du commentaire
            if commentaire_courant.user.id == request.user.id:
                commentaire_courant.delete()
                self.success = True

    def get_data(self):
        super(CommentaireSupprimerViewModel, self).get_data()

        data_json = {
            "redirect_url": self.redirect_url,
            "success": self.success
        }

        return data_json

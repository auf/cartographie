#coding: utf-8

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from cartographie.formation.models import Formation, FormationCommentaire, UserRole
from cartographie.formation.constants import statuts_formation
from cartographie.formation.viewModels.baseAjouterViewModel \
    import BaseAjouterViewModel
from cartographie.formation.forms.formation \
    import FormationCommentaireForm


class CommentairesViewModel(BaseAjouterViewModel):
    # Affiche la liste des commentaires

    formation = None
    form = None
    commentaires = []

    def __init__(self, request, token, formation_id):
        super(CommentairesViewModel, self).__init__(request, token)
        self.formation = Formation.objects.get(pk=formation_id)
        self.form = FormationCommentaireForm()
        self.commentaires = FormationCommentaire.objects.filter(
            formation=self.formation
        ).order_by("date")
        self.peut_modifier_workflow = UserRole.peut_modifier_workflow(request.user, self.etablissement)

    def get_data(self):
        data = super(CommentairesViewModel, self).get_data()
        data.update({
            "formation": self.formation,
            "statuts_formation": statuts_formation,
            "commentaires": self.commentaires,
            "form": self.form,
            'form_url': reverse('commentaire_ajouter', args=[self.token, self.formation.id]),
            "peut_modifier_workflow": self.peut_modifier_workflow,
        })
        return data


class CommentaireAjouterViewModel(BaseAjouterViewModel):
    form = None
    formation = None

    def __init__(self, request, token, formation_id):
        super(CommentaireAjouterViewModel, self).__init__(request, token)
        self.formation = Formation.objects.get(pk=formation_id)

        if request.method == "POST":
            self.form = FormationCommentaireForm(request.POST)
        else:
            self.form = FormationCommentaireForm()

    def get_data(self):
        data = super(CommentaireAjouterViewModel, self).get_data()
        data.update({
            "form": self.form,
            "formation": self.formation
        })

        return data


class CommentaireModifierViewModel(BaseAjouterViewModel):
    success = False
    commentaire = None

    def __init__(self, request, token, formation_id, commentaire_id):
        super(CommentaireModifierViewModel, self).__init__(request, token)

        try:
            self.commentaire = FormationCommentaire.objects.get(
                pk=commentaire_id, user=request.user
            )
        except ObjectDoesNotExist:
            self.success = False
        else:
            self.success = True

    def get_data(self):
        super(CommentaireModifierViewModel, self).get_data()

        data = {
            "success": self.success,
            "commentaire": self.commentaire,
        }
        return data


class CommentaireSupprimerViewModel(BaseAjouterViewModel):
    redirect_url = None
    success = False

    def __init__(self, request, token, formation_id, commentaire_id):
        super(CommentaireSupprimerViewModel, self).__init__(request, token)

        try:
            commentaire_courant = FormationCommentaire.objects.get(
                pk=commentaire_id
            )
        except ObjectDoesNotExist:
            self.success = False
        else:
            # si l'id du user courant concorde avec l'id de l'auteur
            # du commentaire
            if commentaire_courant.user.id == request.user.id:
                commentaire_courant.delete()
                self.success = True
                self.redirect_url = reverse(
                    "formation_modifier_commentaires",
                    args=[token, formation_id]
                )

    def get_data(self):
        super(CommentaireSupprimerViewModel, self).get_data()

        data_json = {
            "redirect_url": self.redirect_url,
            "success": self.success
        }

        return data_json

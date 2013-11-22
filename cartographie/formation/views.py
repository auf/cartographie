# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import (
    get_object_or_404, redirect, render, render_to_response)
from django.template import RequestContext
from django.utils import simplejson

from cartographie.formation.decorators import (
    token_required, editor_of_region_required)
from cartographie.formation.forms.personne_modifier_password_form import (
    PersonneModifierPasswordForm)
from cartographie.formation.models import (
    Acces, Fichier, Formation, FormationModification, Personne)
from cartographie.formation.models.workflow import (
    statusIdToStatusLabel, is_statut_final)
from sendfile import send_file


def erreur(request):
    """
    Page d'erreur lorsque le token fait défaut
    """
    return render_to_response(
        "erreur.html", {}, RequestContext(request)
    )


@token_required
def liste(request, token):
    """Afficher la liste de formation pour l'utilisateur courant"""

    from cartographie.formation.viewModels.formation.liste import (
        ListeViewModel)

    admin = request.user.is_superuser
    referent = False

    try:
        personne = Personne.objects.get(utilisateur=request.user)
        referent = personne.role == 'referent'
    except Personne.DoesNotExist:
        pass

    context = RequestContext(request, {
        'peut_actualiser': admin or referent,
    })

    return render_to_response(
        "liste.html",
        ListeViewModel(token, request.user, onglet_actif="formation").get_data(),
        context
    )


@token_required
def ajouter(request, token):
    """
        Formulaire d'ajout d'une fiche formation
    """

    from cartographie.formation.viewModels.formation.ajouter \
        import AjouterViewModel

    # AjouterViewModel fait la vérification du POST avec le formulaire
    # VM = ViewModel :)
    ajoutVM = AjouterViewModel(request, token)

    if ajoutVM.form.is_valid():
        # pour gérer les m2m, on doit utiliser commit=False
        # pour sauvegarder le modele de base AVANT de faire des save m2m.
        nouvelle_formation = ajoutVM.form.save(commit=False)
        # sauvegarder l'établissement à la main car la VM le connait
        nouvelle_formation.etablissement = ajoutVM.etablissement
        nouvelle_formation.save()
        nouvelle_formation.save_modification(request)
        # puis sauvegarder les m2m normaux
        ajoutVM.form.save_m2m()

        return HttpResponseRedirect(
            reverse(
                "formation_modifier_etablissements",
                args=[token, nouvelle_formation.id]
            )
        )

    return render_to_response(
        "formation/ajouter.html",
        ajoutVM.get_data(),
        RequestContext(request)
    )


@token_required
def consulter(request, token, formation_id):
    """
        Fiche d'une formation
    """

    formation = Formation.objects.get(pk=formation_id)

    c = {
        'formation': formation,
        'files': Fichier.objects.filter(formation=formation).order_by('nom'),
        'composantes_actives': formation.etablissement_composante.filter(
            actif=True),
        'auf_actifs': formation.formationpartenaireauf_set.filter(
            etablissement__actif=True),
        'prive': True,
    }

    return render(request, "formation/formation_detail.html", c)


@token_required
def historique(request, token, formation_id):
    """
        Historique d'une formation
    """

    historique = FormationModification.objects.filter(formation=formation_id) \
        .order_by("-date")

    formation = Formation.objects.get(pk=formation_id)

    c = {
        'formation': formation,
        'historique': historique,
    }

    return render(request, "formation/historique.html", c)


@token_required
def actualiser(request, token, formation_id):
    '''Mettre à jour une formation'''

    formation = Formation.objects.get(pk=formation_id)
    formation.date_modification = datetime.datetime.now()
    formation.save()

    messages.success(
        request, u'La formation "%s" a été mise à jour' % (formation.nom, ))

    return redirect('formation_liste', token)


@token_required
def tout_actualiser(request, token, etablissement_id):
    '''Mettre à jour toutes les formations'''

    formations = Formation.objects.filter(
        etablissement_id=etablissement_id).exclude(statut=999)
    formations.update(date_modification=datetime.datetime.now())

    messages.success(
        request, u'Les formations ont été mises à jour')

    return redirect('formation_liste', token)


@token_required
def select_actualiser(request, token, etablissement_id):
    '''Mettre à jour les formations sélectionnées'''

    if request.method == 'POST':
        ids = []
        for key in request.POST.keys():
            if key.startswith('formation-'):
                num = key.split('-')[1]
                ids.append(num)
        if ids:
            formations = Formation.objects.filter(
                etablissement_id=etablissement_id, pk__in=ids)
            formations.update(date_modification=datetime.datetime.now())

            messages.success(request, u'Les formations ont été mises à jour')

    return redirect('formation_liste', token)


@token_required
def modifier(request, token, formation_id=None):
    """
        Formulaire d'édition d'une fiche formation
    """

    from cartographie.formation.viewModels.formation.modifier \
        import ModifierViewModel

    modifVM = ModifierViewModel(request, token, formation_id)

    if modifVM.form.is_valid():
        # pas nécessaire de gérer les m2m ici, contrairement à l'ajout
        # d'une nouvelle fiche
        formation_courante = modifVM.form.save()
        # TODO: overrider la fonction save du formulaire pour donner la request
        # à la fonction save du Model. Pour l'instant, on fait le
        # save_modification() de la ligne suivante:
        formation_courante.save_modification(request)
        # obtenir les infos de nouveau pour rafraîchir la page
        modifVM = ModifierViewModel(request, token, formation_courante.id)

    return render_to_response(
        "formation/modifier.html",
        modifVM.get_data(),
        RequestContext(request)
    )


def modifier_workflow(request, token, formation_id, statut_id):
    """
        Modifier le statut de workflow de la fiche courante
    """

    from cartographie.formation.viewModels.formation.workflow \
        import WorkflowViewModel

    # le gros du traitement se fait dans le ViewModel suivant
    WorkflowViewModel(request, token, formation_id, statut_id)
    # peu importe ce qui arrive, un message a été setté dans le ViewModel
    # on redirige donc sans faire de validation
    return HttpResponseRedirect(
        reverse("formation_modifier", args=[token, formation_id])
    )


@token_required
def modifier_etablissements(request, token, formation_id=None):

    from cartographie.formation.viewModels.formation.modifier \
        import ModifierViewModel

    # absorber les infos de la requete
    modifVM = ModifierViewModel(
        request, token, formation_id, presence_formsets=True
    )

    if request.method == "POST":
        # vérifier la présence du champ "etablissement_emet_diplome"
        # et la conserver si elle est présente
        emet = request.POST.get("etablissement_emet_diplome", False)

        if emet == "on":
            modifVM.formation.etablissement_emet_diplome = True
        else:
            modifVM.formation.etablissement_emet_diplome = False

        modifVM.formation.save()
        modifVM.formation.save_modification(request)

    formsets_sauvegarder = []
    # Verifier la validité des formsets
    if modifVM.composanteFormset.is_valid():
        modifVM.composanteFormset.save()
        formsets_sauvegarder.append(True)

    if modifVM.partenaireAufFormset.is_valid():
        modifVM.partenaireAufFormset.save()
        formsets_sauvegarder.append(True)

    if modifVM.partenaireAutreFormset.is_valid():
        modifVM.partenaireAutreFormset.save()
        formsets_sauvegarder.append(True)

    # si au moins un formset a été sauvegardé, on redirige
    if True in formsets_sauvegarder:
        return HttpResponseRedirect(
            reverse(
                "formation_modifier_etablissements",
                args=[token, formation_id]
            )
        )

    return render_to_response(
        "formation/modifier_etablissements.html",
        modifVM.get_data(),
        RequestContext(request)
    )


@token_required
def modifier_commentaires(request, token, formation_id=None):

    from cartographie.formation.viewModels.formation.commentaire \
        import CommentairesViewModel

    vm = CommentairesViewModel(request, token, formation_id)

    return render_to_response(
        "formation/commentaire/liste.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def modifier_fichiers(request, token, formation_id=None):

    from cartographie.formation.viewModels.formation.fichier \
        import FichierViewModel

    vm = FichierViewModel(request, token, formation_id)

    return render_to_response(
        "formation/modifier_fichier.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def commentaire_ajouter(request, token, formation_id):
    """
        Cette fonction ne sert qu'à recevoir du data via un POST
        ou à afficher un formulaire si c'est un call ajax
    """
    from cartographie.formation.viewModels.formation.commentaire \
        import CommentaireAjouterViewModel

    vm = CommentaireAjouterViewModel(request, token, formation_id)

    form_url = reverse('commentaire_ajouter', args=[token, formation_id])

    if request.GET.get("ajax"):
        return render_to_response(
            "formation/commentaire/form.html",
            vm.get_data().update({'form_url': form_url}),
            RequestContext(request)
        )

    if request.method == "POST":
        if vm.form.is_valid():
            commentaire = vm.form.save(commit=False)
            commentaire.formation = vm.formation

            commentaire.user = None
            if request.user.is_authenticated():
                commentaire.user = request.user

            commentaire.save()

            return HttpResponseRedirect(reverse(
                "formation_modifier_commentaires", args=[token, formation_id]))
        else:
            messages.warning(
                request, u"Veuillez entrer un commentaire"
            )

    return HttpResponseRedirect(
        reverse("formation_modifier_commentaires", args=[token, formation_id])
    )


@token_required
def commentaire_modifier(request, token, formation_id, commentaire_id):
    from cartographie.formation.viewModels.formation.commentaire \
        import CommentaireModifierViewModel

    vm = CommentaireModifierViewModel(
        request, token, formation_id, commentaire_id
    )
    data = vm.get_data()

    if request.method == "POST":
        texte = request.POST.get("commentaire")
        commentaire_courant = data["commentaire"]
        commentaire_courant.commentaire = texte
        commentaire_courant.save()
        # pour que l'objet commentaire soit jsonisable
        data["commentaire"] = commentaire_courant.id

    return HttpResponseRedirect(
        reverse(
            "formation_modifier_commentaires",
            args=[token, formation_id]
        )
    )


@token_required
def commentaire_supprimer(request, token, formation_id, commentaire_id):

    from cartographie.formation.viewModels.formation.commentaire \
        import CommentaireSupprimerViewModel

    vm = CommentaireSupprimerViewModel(
        request, token, formation_id, commentaire_id
    )
    return HttpResponse(
        simplejson.dumps(vm.get_data()),
        mimetype="application/json"
    )


def personne_valider_compte(request, token, personne_id):
    try:
        personne = Personne.objects.get(pk=personne_id)
        personne.utilisateur.is_active = True
        personne.utilisateur.save()
        # envoyer courriel
        personne.envoyer_courriel_motdepasse()
        return redirect('formation_personne_liste', token)
    except Personne.DoesNotExist:
        return HttpResponseRedirect('/')


def personne_modifier_password(request, secret):
    user = None

    try:
        # Essaie de remonter vers la personne pour laquelle le secret a été
        # assigné
        personne = Personne.objects.filter(
            jeton_password__jeton=secret).get()
        user = personne.utilisateur
    except Personne.DoesNotExist:
        # Il n'y a pas de personne assignée, donc le jeton est invalide
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = PersonneModifierPasswordForm(request.POST)

        if form.is_valid():
            password1 = form.cleaned_data['new_password1']
            password2 = form.cleaned_data['new_password2']
            if password1 and password2 and (password1 == password2):
                user.set_password(password1)
                user.save()
                messages.success(
                    request,
                    u'Votre mot de passe a été mis à jour avec succès!')

                return HttpResponseRedirect('/')
    else:
        form = PersonneModifierPasswordForm()

    return render(request, 'personne/modifier_password.html', {
        'secret': secret,
        'form': form,
    })


@token_required
def liste_personne(request, token):

    from cartographie.formation.viewModels.personne.liste \
        import ListeViewModel

    return render_to_response(
        "liste.html",
        ListeViewModel(token, request.user, onglet_actif="personne").get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_personne(request, token):

    from cartographie.formation.viewModels.personne.ajouter \
        import AjouterViewModel

    vm = AjouterViewModel(request, token)

    if request.method == "POST":
        if vm.form.is_valid():
            # on ne veut pas sauvegarder le ForeignKey tout de suite
            nouvelle_personne = vm.form.save(commit=False)
            # on assigne automatiquement l'etablissement courant
            # car le champ est disabled dans le formulaire
            nouvelle_personne.etablissement = vm.etablissement
            nouvelle_personne.save()

            return HttpResponseRedirect(
                reverse("formation_personne_liste", args=[token])
            )

    return render_to_response(
        "personne/ajouter.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def commentaire_avant_changement_statut(
        request, token, formation_id, nouveau_statut):

    from cartographie.formation.viewModels.formation.commentaire import (
        CommentaireAjouterViewModel)
    from cartographie.formation.forms.formation import (
        CommentaireOptionnelForm, FormationCommentaireForm)

    suppression = int(nouveau_statut) == 999

    vm = CommentaireAjouterViewModel(
        request, token, formation_id, suppression=suppression)
    form_url = reverse(
        'formation_commentaire_avant_changement_statut',
        args=[token, formation_id, nouveau_statut])

    if request.method == "POST":
        if vm.form.is_valid():
            # Si on a un formulaire avec commentaire optionnel, et qu'il y a un
            # commentaire écrit, on échange le formulaire avec celui à
            # commentaire obligatoire.
            instance = isinstance(vm.form, CommentaireOptionnelForm)
            content = vm.form.cleaned_data['commentaire']
            if instance and content:
                import pdb; pdb.set_trace()
                vm.form = FormationCommentaireForm(request.POST)
                vm.form.is_valid()

            if content:
                commentaire = vm.form.save(commit=False)
                commentaire.formation = vm.formation

                commentaire.user = None
                if request.user.is_authenticated():
                    commentaire.user = request.user

                commentaire.commentaire = (
                    "[Statut: %s] %s" % (
                        statusIdToStatusLabel(nouveau_statut),
                        commentaire.commentaire))
                commentaire.save()

            return HttpResponse(simplejson.dumps({
                'error': False,
                'next_url': reverse(
                    'formation_modifier_workflow',
                    args=[token, formation_id, nouveau_statut])
            }))

        else:
            return HttpResponse(
                simplejson.dumps({
                    'error': True,
                    'msg': (
                        'Un commentaire est nécessaire pour ce changement ' +
                        'de statut'),
                }), mimetype="application/json"
            )

    data = vm.get_data()
    data.update({
        'form_url': form_url,
        'json_request': True,
        'statut_final': is_statut_final(nouveau_statut),
        'retour_arriere': True,
    })

    return render_to_response(
        "formation/commentaire/form.html",
        data,
        RequestContext(request)
    )


@token_required
def personne_ajouter_popup(request, token):
    from cartographie.formation.viewModels.personne.ajouter import (
        AjouterViewModel)

    vm = AjouterViewModel(request, token, json_request=True)

    if request.method == "POST":
        if vm.form.is_valid():
            nouvelle_personne = vm.form.save(commit=False)
            nouvelle_personne.etablissement = vm.etablissement
            nouvelle_personne.save()

            data = {
                "msg": "", "error": False,
                "personne": {
                    "id": nouvelle_personne.id,
                    "nom": nouvelle_personne.nom,
                    "prenom": nouvelle_personne.prenom,
                    "actif": nouvelle_personne.actif
                }
            }
        else:
            data = {"msg": "Le champ nom et prénom sont requis", "error": True}

        return HttpResponse(
            simplejson.dumps(data), mimetype="application/json"
        )

    return render_to_response(
        "personne/form.html",
        vm.get_data(),
        RequestContext(request)
    )
    pass


@token_required
def modifier_personne(request, token, personne_id):
    from cartographie.formation.viewModels.personne.modifier import (
        ModifierViewModel)

    vm = ModifierViewModel(request, token, personne_id)

    if request.method == "POST":
        if vm.form.is_valid():
            vm.form.save()

            return HttpResponseRedirect(
                reverse("formation_personne_liste", args=[token])
            )

    return render_to_response(
        "personne/modifier.html",
        vm.get_data(),
        RequestContext(request)
    )
    pass


@token_required
def liste_partenaire_autre(request, token):
    from cartographie.formation.viewModels.partenaire_autre.liste import (
        ListeViewModel)

    return render_to_response(
        "liste.html",
        ListeViewModel(token, request.user, onglet_actif="partenaire-autre").get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_partenaire_autre(request, token):
    from cartographie.formation.viewModels.partenaire_autre.ajouter import (
        AjouterViewModel)

    vm = AjouterViewModel(request, token, json_request=False)

    if request.method == "POST":
        if vm.form.is_valid():
            nouveau_partenaire_autre = vm.form.save(commit=False)
            nouveau_partenaire_autre.etablissement = vm.etablissement
            nouveau_partenaire_autre.save()

            return HttpResponseRedirect(
                reverse("formation_partenaire_autre_liste", args=[token])
            )

    return render_to_response(
        "partenaire-autre/ajouter.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_partenaire_autre_popup(request, token):
    from cartographie.formation.viewModels.partenaire_autre.ajouter import (
        AjouterViewModel)

    vm = AjouterViewModel(request, token, json_request=True)

    if request.method == "POST":
        if vm.form.is_valid():
            nouveau_partenaire_autre = vm.form.save(commit=False)
            nouveau_partenaire_autre.etablissement = vm.etablissement
            nouveau_partenaire_autre.save()
            data = {
                "msg": "", "error": False,
                "partenaire_autre": {
                    "id": nouveau_partenaire_autre.id,
                    "nom": nouveau_partenaire_autre.nom
                }
            }
        else:
            data = {"msg": "Le champ nom est requis", "error": True}

        return HttpResponse(
            simplejson.dumps(data), mimetype="application/json"
        )

    return render_to_response(
        "partenaire-autre/form.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def modifier_partenaire_autre(request, token, partenaire_autre_id):
    from cartographie.formation.viewModels.partenaire_autre.modifier import (
        ModifierViewModel)

    vm = ModifierViewModel(request, token, partenaire_autre_id)

    if request.method == "POST":
        if vm.form.is_valid():
            vm.form.save()

            return HttpResponseRedirect(
                reverse("formation_partenaire_autre_liste", args=[token])
            )

    return render_to_response(
        "partenaire-autre/modifier.html",
        vm.get_data(),
        RequestContext(request)
    )
    pass


@token_required
def liste_composante(request, token):
    from cartographie.formation.viewModels.composante.liste import (
        ListeViewModel)

    return render_to_response(
        "liste.html",
        ListeViewModel(token, request.user, onglet_actif="composante").get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_composante(request, token):
    from cartographie.formation.viewModels.composante.ajouter \
        import AjouterViewModel

    vm = AjouterViewModel(request, token, json_request=False)

    if request.method == "POST":
        if vm.form.is_valid():
            nouvelle_composante = vm.form.save(commit=False)
            # assignation forcée de l'établissement lié
            nouvelle_composante.etablissement = vm.etablissement
            nouvelle_composante.save()

            return HttpResponseRedirect(
                reverse("formation_composante_liste", args=[token])
            )

    return render_to_response(
        "composante/ajouter.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_composante_popup(request, token):
    from cartographie.formation.viewModels.composante.ajouter \
        import AjouterViewModel

    vm = AjouterViewModel(request, token, json_request=True)

    if request.method == "POST":
        if vm.form.is_valid():
            nouvelle_composante = vm.form.save(commit=False)
            # assignation forcée de l'établissement lié
            nouvelle_composante.etablissement = vm.etablissement
            nouvelle_composante.save()

            data = {
                "msg": "", "error": False,
                "composante": {
                    "id": nouvelle_composante.id,
                    "nom": nouvelle_composante.nom
                }
            }
        else:
            data = {"msg": "Le champ nom est requis", "error": True}

        return HttpResponse(
            simplejson.dumps(data), mimetype="application/json"
        )

    return render_to_response(
        "composante/form.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def modifier_composante(request, token, composante_id):

    from cartographie.formation.viewModels.composante.modifier \
        import ModifierViewModel

    vm = ModifierViewModel(request, token, composante_id)

    if request.method == "POST":
        if vm.form.is_valid():
            vm.form.save()

            return HttpResponseRedirect(
                reverse("formation_composante_liste", args=[token])
            )

    return render_to_response(
        "composante/modifier.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def liste_langue(request, token):

    from cartographie.formation.viewModels.langue.liste import ListeViewModel

    return render_to_response(
        "liste.html",
        ListeViewModel(token, request.user, onglet_actif="langue").get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_langue(request, token):
    from cartographie.formation.viewModels.langue.ajouter import (
        AjouterViewModel)

    vm = AjouterViewModel(request, token)

    if request.method == "POST":
        if vm.form.is_valid():
            vm.form.save()

            return HttpResponseRedirect(
                reverse("formation_langue_liste", args=[token])
            )

    return render_to_response(
        "langue/ajouter.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_langue_popup(request, token):
    from cartographie.formation.viewModels.langue.ajouter import (
        AjouterViewModel)

    vm = AjouterViewModel(request, token, json_request=True)

    if request.method == "POST":
        if vm.form.is_valid():
            nouvelle_langue = vm.form.save()

            data = {
                "msg": "", "error": False,
                "langue": {
                    "id": nouvelle_langue.id,
                    "nom": nouvelle_langue.nom,
                    "actif": nouvelle_langue.actif
                }
            }
        else:
            data = {"msg": "Le champ nom est requis", "error": True}

        return HttpResponse(
            simplejson.dumps(data), mimetype="application/json"
        )

    return render_to_response(
        "langue/form.html",
        vm.get_data(),
        RequestContext(request)
    )


@token_required
def modifier_langue(request, token, langue_id):
    from cartographie.formation.viewModels.langue.modifier import (
        ModifierViewModel)

    vm = ModifierViewModel(request, token, langue_id)

    if request.method == "POST":
        if vm.form.is_valid():
            vm.form.save()

            return HttpResponseRedirect(
                reverse("formation_langue_liste", args=[token])
            )

    return render_to_response(
        "langue/modifier.html",
        vm.get_data(),
        RequestContext(request)
    )
    pass


@token_required
def fichiers(request, token, formation_id=None, fichier_id=None):
    def file_in_formation(fil, formation):
        return fil.formation == formation

    def token_is_valid(acces, formation):
        return acces.etablissement == formation.etablissement

    formation = get_object_or_404(Formation, pk=formation_id)
    acces = get_object_or_404(Acces, token=token)
    fil = get_object_or_404(Fichier, pk=fichier_id)

    if fil.is_public or (
            token_is_valid(acces, formation)
            and file_in_formation(fil, formation)):
        return send_file(fil.file)

    raise Http404

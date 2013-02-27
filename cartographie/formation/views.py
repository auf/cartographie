# coding: utf-8

from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib import messages

from cartographie.formation.decorators import token_required
# from cartographie.formation.models import FormationModification


def erreur(request):
    """
    Page d'erreur lorsque le token fait défaut
    """
    return render_to_response(
        "erreur.html", {}, RequestContext(request)
    )


@token_required
def liste(request, token):
    """
        Afficher la liste de formation pour l'utilisateur courant
    """

    from cartographie.formation.viewModels.formation.liste import ListeViewModel

    return render_to_response(
        "liste.html",
        ListeViewModel(token, onglet_actif="formation").get_data(),
        RequestContext(request)
    )


@token_required
def ajouter(request, token):
    """
        Formulaire d'ajout d'une fiche formation
    """

    from cartographie.formation.viewModels.formation.ajouter import AjouterViewModel

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
def modifier(request, token, formation_id=None):
    """
        Formulaire d'édition d'une fiche formation
    """

    from cartographie.formation.viewModels.formation.modifier import ModifierViewModel

    modifVM = ModifierViewModel(request, token, formation_id)

    if modifVM.form.is_valid():
        # pas nécessaire de gérer les m2m ici, contrairement à l'ajout
        # d'une nouvelle fiche
        formation_courante = modifVM.form.save()
        # TODO: overrider la fonction save du formulaire pour donner la request
        # à la fonction save du Model. Pour l'instant, on fait le save_modification() de la ligne
        # suivante:
        formation_courante.save_modification(request)
        # obtenir les infos de nouveau pour rafraîchir la page
        modifVM = ModifierViewModel(request, token, formation_courante.id)

    return render_to_response(
        "formation/modifier.html",
        modifVM.get_data(),
        RequestContext(request)
    )


@token_required
def modifier_workflow(request, token, formation_id, statut):
    """
        Modifier le statut de workflow de la fiche courante
    """

    # verifier que le statut existe
    # obtenir la formation courante
    # modifier le statut avec les fonctions de WorkflowMixin
    # catcher les erreurs et les afficher correctement à l'usager
    # rediriger vers la page de modification global si réussiste
    messages.success(
        request, u"test du messaging django !"
    )

    return HttpResponseRedirect(
        reverse(
            "formation_modifier",
            args=[token, formation_id]
        )
    )

    pass


@token_required
def modifier_etablissements(request, token, formation_id=None):

    from cartographie.formation.viewModels.formation.modifier import ModifierViewModel

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
def liste_personne(request, token):

    from cartographie.formation.viewModels.personne.liste import ListeViewModel

    return render_to_response(
        "liste.html",
        ListeViewModel(token, onglet_actif="personne").get_data(),
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
def ajouter_personne_popup(request, token):

    from cartographie.formation.viewModels.personne.ajouter import AjouterViewModel

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

    from cartographie.formation.viewModels.personne.modifier \
        import ModifierViewModel

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

    from cartographie.formation.viewModels.partenaire_autre.liste \
        import ListeViewModel

    return render_to_response(
        "liste.html",
        ListeViewModel(token, onglet_actif="partenaire-autre").get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_partenaire_autre(request, token):

    from cartographie.formation.viewModels.partenaire_autre.ajouter \
        import AjouterViewModel

    vm = AjouterViewModel(request, token, json_request=False)

    if request.method == "POST":
        if vm.form.is_valid():
            vm.form.save()

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
    from cartographie.formation.viewModels.partenaire_autre.ajouter \
        import AjouterViewModel

    vm = AjouterViewModel(request, token, json_request=True)

    if request.method == "POST":
        if vm.form.is_valid():
            nouveau_partenaire_autre = vm.form.save()

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

    from cartographie.formation.viewModels.partenaire_autre.modifier \
        import ModifierViewModel

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

    from cartographie.formation.viewModels.composante.liste import ListeViewModel

    return render_to_response(
        "liste.html",
        ListeViewModel(token, onglet_actif="composante").get_data(),
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
        ListeViewModel(token, onglet_actif="langue").get_data(),
        RequestContext(request)
    )


@token_required
def ajouter_langue(request, token):

    from cartographie.formation.viewModels.langue.ajouter import AjouterViewModel

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
    from cartographie.formation.viewModels.langue.ajouter import AjouterViewModel

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
    from cartographie.formation.viewModels.langue.modifier import ModifierViewModel

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

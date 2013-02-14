# coding: utf-8

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from cartographie.formation.decorators import token_required
from cartographie.formation.models import FormationModification


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


# @token_required
# def consulter(request, token, formation_id=None):
#     """
#         Voir la fiche formation sans modification possible
#     """

#     return render_to_response(
#         "formation/consulter.html", {}, RequestContext(request)
#     )


# @token_required
# def consulter_etablissements(request, token, formation_id=None):
#     return render_to_response(
#         "formation/consulter_etablissements.html", {}, RequestContext(request)
#     )


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

        # laisser une trace des modifications
        modif = FormationModification()

        if request.user.is_authenticated():
            modif.save_modification(formation_courante.id, request.user)
        else:
            modif.save_modification(formation_courante.id)

        # obtenir les infos de nouveau pour rafraîchir la page
        modifVM = ModifierViewModel(request, token, formation_courante.id)

    return render_to_response(
        "formation/modifier.html",
        modifVM.get_data(),
        RequestContext(request)
    )


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
            reverse("formation_modifier", args=[token, formation_id])
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
    return render_to_response(
        "personne/ajouter.html",
        {},
        RequestContext(request)
    )


@token_required
def modifier_personne(request, token, personne_id):
    return render_to_response(
        "personne/modifier.html",
        {},
        RequestContext(request)
    )
    pass


@token_required
def ajouter_partenaire_autre(request, token):
    return render_to_response(
        "partenaire-autre/ajouter.html",
        {},
        RequestContext(request)
    )


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
def modifier_partenaire_autre(request, token, personne_id):
    return render_to_response(
        "partenaire-autre/modifier.html",
        {},
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

    vm = AjouterViewModel(request, token)

    if request.method == "POST":
        if vm.form.is_valid():
            vm.form.save()

            return HttpResponseRedirect(
                reverse("formation_composante_liste", args=[token])
            )

    return render_to_response(
        "composante/ajouter.html",
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

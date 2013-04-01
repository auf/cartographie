var AUF = {};

AUF.formation = function(){
    return {
        init: function(){
            console.log("AUF.formation.init()");

            this.selectCurrentEtablissement();
            this.beautifulSelects();
            this.formPopups();
            this.commentaire_actions();
        },
        selectCurrentEtablissement: function(){
            console.log("AUF.formation.selectCurrentEtablissement()");
            var id = $(".content").data("etablissement-id");

            $("#id_etablissement option[value=" + id + "]").attr(
                "selected", "selected"
            );

            $("#id_etablissement").attr("disabled", "disabled");
        },
        beautifulSelects : function(){
            /*
                Utilisation de chosen pour augmenter l'utilisabilité
                des SELECT à choix unique et multiple
             */
            console.log("AUF.formation.beautifulSelects()");

            if (typeof $.fn.chosen !== "undefined") {
                $(".form-auf select").chosen({
                    placeholder_text_multiple: "Veuillez choisir une ou plusieurs options"
                });
            }
        },
        _formPopupFactory: function(quoi){
            /*
                Ajouter l'activation d'une fenetre modal sur le clique
                d'un lien dans la class est "a.modal-{quoi}"
             */
            console.log("AUF.formation._formPopupFactory()", quoi);

            $("a.modal-" + quoi).on("click", function(){
                var lien = $(this);

                $("#popup-form-" + quoi).modal({
                    remote: lien.attr("href")
                });

                return false;
            });
        },
        _popupSubmitFactory: function(modal_selector, done_callback){
             console.log("AUF.formation._popupSubmitFactory()", modal_selector);
            /*
                Fonction utiliser par le bouton de soumission d'un formulaire dans un
                popup
             */

            var form = $(modal_selector + " form");
            var submit_url = form.attr("action");

            $.ajax({
                url: submit_url,
                method: "post",
                data: form.serialize(),
                dataType: "json"
            }).done(function(data){
                console.log(data);

                if (data.error === true) {
                    window.alert(data.msg)
                }else{
                    $(modal_selector).modal("hide");
                    done_callback(data);
                }
            });
        },
        formPopups: function(){
            console.log("AUF.formation.formPopups()");

            // popup langue
            this._formPopupFactory("langue");
            // popup responsable
            this._formPopupFactory("responsable");
            // popup contact
            this._formPopupFactory("contact");
            // popup composante
            this._formPopupFactory("composante");
            // popup partenaire autre (non membre)
            this._formPopupFactory("partenaire-autre");
            // popup partenaire autre (non membre)
            this._formPopupFactory("commentaire");
        },
        popupLangueSubmit : function(){
            console.log("AUF.formation.popupLangueSubmit()");
            /*
                Fonction utiliser par le bouton de soumission du
                formulaire d'ajout de langue
             */

            this._popupSubmitFactory(
                "#popup-form-langue",
                function(data){
                    var langue = data.langue;

                    if (langue.actif) {
                        // Ajouter l'option dans la liste et
                        // avertir Chosen que la liste a été mis à jour
                        $("#id_langue").append(
                            "<option value=" + langue.id + ">" + langue.nom + "</option>"
                        ).trigger("liszt:updated");
                    }
                }
            );
        },

        popupCommentaireSubmit: function() {
            console.log("AUF.formation.popupCommentaireSubmit()");
            /*
             * Fonction utilisée par le bouton d'envoi du formulaire
             * d'ajout d'un commentaire 
             */
            this._popupSubmitFactory(
                '#popup-form-commentaire',
                function(data) {
                    document.location.href = data.next_url;
                }
            );
        },

        popupPersonneSubmit: function(){
            console.log("AUF.formation.popupResponsableSubmit()");
            /*
                Fonction utiliser par le bouton de soumission du
                formulaire d'ajout d'un responsable ou d'un contact
             */

            // détection du popup actif pour déterminer quel formulaire
            // de popup utilisé pour l'envoi de données.
            var quoi = "responsable";
            if ($("div[id*=popup-form-][aria-hidden=false]").attr("id") === "popup-form-contact") {
                quoi = "contact";
            }
            this._popupSubmitFactory(
                "#popup-form-" + quoi,
                function(data){
                    var personne = data.personne;

                    if (personne.actif) {
                        // Ajouter l'option dans les listes et
                        // avertir Chosen que les listes a été mis à jour
                        $("#id_responsables, #id_contacts").append(
                            "<option value=" + personne.id + ">" +
                                personne.prenom + " " + personne.nom.toUpperCase() +
                            "</option>"
                        ).trigger("liszt:updated");
                    }
                }
            );
        },
        popupComposanteSubmit: function(){
            console.log("AUF.formation.popupComposanteSubmit()");
            this._popupSubmitFactory(
                "#popup-form-composante",
                function(data){
                    var composante = data.composante;
                    if (composante) {
                        // Ajouter l'option dans la liste et
                        // avertir Chosen que la liste a été mis à jour
                        $("select[id^=id_composante-]").append(
                            "<option value=" + composante.id + ">" + composante.nom + "</option>"
                        ).trigger("liszt:updated");
                    }
                }
            );
        },
        popupPartenaireAutreSubmit: function(){
            console.log("AUF.formation.popupPartenaireAutreSubmit()");
            this._popupSubmitFactory(
                "#popup-form-partenaire-autre",
                function(data){
                    var partenaire_autre = data.partenaire_autre;

                    if (partenaire_autre) {
                        // Ajouter l'option dans la liste et
                        // avertir Chosen que la liste a été mis à jour
                        $("select[id^=id_partenaires-autre-]").append(
                            "<option value=" + partenaire_autre.id + ">" + partenaire_autre.nom + "</option>"
                        ).trigger("liszt:updated");
                    }
                }
            );
        },
        commentaire_actions: function(){
            console.log("AUF.formation.commentaire_actions()");

            // afficher le formulaire d'édition d'un commentaire
            $(".commentaire_actions .modifier").click(function(){
                $(this).parents("li").find("p.commentaire").addClass("hidden");
                return false;
            });

            // annulation de la modification d'un commentaire
            $(".commentaires li form button.annuler").click(function(){
                $(this).parents("li").find("p.commentaire").removeClass("hidden");
                return false;
            });

            // suppression d'un commentaire
            $(".commentaire_actions .supprimer").click(function(){
                if (confirm("Désirez-vous vraiment supprimer ce commentaire ?")) {
                    $.get(
                        $(this).attr("href"),
                        function(data, textStatus, xhr, dataType){
                            if (data.success === true) {
                                window.location = data.redirect_url;
                            }
                        }
                    );
                }
                return false;
            });
        }
    }
}();

$(document).ready(function(){
    AUF.formation.init();
});

var AUF = {};

AUF.formation = function(){
    return {
        init: function(){
            console.log("AUF.formation.init()");

            this.selectCurrentEtablissement();
            this.beautifulSelects();
            this.formPopups();
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
        _formPopupsFactory: function(quoi){
            /*
                Ajouter l'activation d'une fenetre modal sur le clique
                d'un lien dans la class est "a.modal-{quoi}"
             */
            console.log("AUF.formation._formPopupsFactory()", quoi);

            $("a.modal-" + quoi).on("click", function(){
                var lien = $(this);

                $("#popup-form-" + quoi).modal({
                    remote: lien.attr("href")
                });

                return false;
            });
        },
        formPopups: function(){
            console.log("AUF.formation.formPopups()");

            // popup langue
            this._formPopupsFactory("langue");
            // popup responsable
            this._formPopupsFactory("responsable");
            // popup contact
            this._formPopupsFactory("contact");
        },
        popupLangueSubmit : function(){
            console.log("AUF.formation.popupLangueSubmit()");
            /*
                Fonction utiliser par le bouton de soumission du
                formulaire d'ajout de langue
             */
            var form = $("#popup-form-langue form");
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
                    $("#popup-form-langue").modal("hide");
                    var langue = data.langue;

                    if (langue.actif) {
                        // Ajouter l'option dans la liste et
                        // avertir Chosen que la liste a été mis à jour
                        $("#id_langue").append(
                            "<option value=" + langue.id + ">" + langue.nom + "</option>"
                        ).trigger("liszt:updated");
                    }
                }
            });
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

            var form = $("#popup-form-" + quoi + " form");
            var submit_url = form.attr("action");

            $.ajax({
                url: submit_url,
                method: "post",
                data: form.serialize(),
                dataType: "json"
            }).done(function(data){
                console.log(data);

                if (data.error === true) {
                    window.alert(data.msg);
                }else{
                    $("#popup-form-" + quoi).modal("hide");
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
            });
        }
    }
}();

$(document).ready(function(){
    AUF.formation.init();
});
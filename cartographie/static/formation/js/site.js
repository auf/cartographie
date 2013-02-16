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
        formPopups: function(){
            console.log("AUF.formation.formPopups()");

            // popup langue
            $("a.modal-langue").on("click", function(){
                var lien = $(this);

                $("#popupFormLangue").modal({
                    remote: lien.attr("href")
                });

                return false;
            });
        },
        popupLangueSubmit : function(){
            /*
                Fonction utiliser par le bouton de soumission du
                formulaire d'ajout de langue
             */
            var form = $("#popupFormLangue form");
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
                    $("#popupFormLangue").modal("hide");
                    var langue = data.langue;
                    // Ajouter l'option dans la liste et
                    // avertir Chosen que la liste a été mis à jour
                    $("#id_langue").append(
                        "<option value=" + langue.id + ">" + langue.nom + "</option>"
                    ).trigger("liszt:updated");
                }
            });
        }
    }
}();

$(document).ready(function(){
    AUF.formation.init();
});
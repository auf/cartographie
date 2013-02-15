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

            var options = {
                remote: true
            };

            // popup langue
            $("a.modal-langue").on("click", function(){
                $("#popupFormLangue").modal(options);

                return false;
            });
        }
    }
}();

$(document).ready(function(){
    AUF.formation.init();
});
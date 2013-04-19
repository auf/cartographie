var AUF = {};

AUF.home = function(){
    return {
        init: function(){
            console.log("AUF.home.init()");
            this.searchForm();
            this.beautifulSelects(); 
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


        searchForm: function(){
            console.log("AUF.home.searchForm()");

            $(".actions .btn").click(function(){
                $(this).parents("form").submit();
                return false;
            });
        }
    };
}();

$(document).ready(function(){
    AUF.home.init();

    $("#recherche select").change(function() {
        $("#recherche").submit();
    });
});

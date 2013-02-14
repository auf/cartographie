var AUF = {};

AUF.home = function(){
    return {
        init: function(){
            console.log("AUF.home.init()");
            this.searchForm();
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
});
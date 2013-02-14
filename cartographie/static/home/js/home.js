var AUF = {};

AUF.home = function(){
    return {
        init: function(){
            console.log("AUF.home.init()");
        }
    };
}();

$(document).ready(function(){
    AUF.home.init();
});
var AUF = {};

AUF.dashboard = function(){
    return {
        init: function(){
            console.log("AUF.dashboard.init()");
        }
    };
}();

$(document).ready(function(){
    AUF.dashboard.init();
});
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

  $('.formations-collapse').accordion({
    'active': false,
    'collapsible': true,
    'heightStyle': 'content',
    'icons': {
      'header': 'icon icon-chevron-down',
      'activeHeader': 'icon icon-chevron-up',
    },
  });
});

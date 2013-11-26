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

$('.select-check').click(function() {
    updateEnabled = $('.select-check:checked').length !== 0;

    if (updateEnabled) {
        $('#select-update').removeClass('disabled');
    } else {
        $('#select-update').addClass('disabled');
    }

    return true;

});

$('#select-update').click(function() {

    if (updateEnabled) {
        $('#select-form').submit();
    }

    return false;

});

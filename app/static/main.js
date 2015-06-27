window.Checks = {};

(function() {
  "use strict";

  var root = this,
    $ = root.jQuery,
    Checks = root.Checks;

  Checks.register = function() {
    $('.radio-label input').iCheck({
      checkboxClass: 'icheckbox_square-pink',
      radioClass: 'iradio_square-pink',
      increaseArea: '20%'
    }).on('ifToggled', function(event){
      $(this).closest('.radio-label').toggleClass('checked')
    });
  };

}.call(this));

$(document).ready(function() {
  window.Checks.register();
});

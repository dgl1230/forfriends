/* Top Menu */
$(document).ready(
  function () {
    $('.nav li').hover(
      function () { 
        $('ul', this).fadeIn("fast");
      },
      function () { 
        $('ul', this).fadeOut("fast");
      }
    );
  }
);

 $(function() {
$( "#tabs" ).tabs({
event: "mouseover"
});
});

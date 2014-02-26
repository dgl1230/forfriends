/* Top Menu */
$(document).ready(
  function () {
    $('.nav li').hover(
      function () { 
        $('.nav li ul li').css('display', 'inline');
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

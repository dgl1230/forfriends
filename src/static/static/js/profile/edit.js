//Submit forms with ajax
$(document).ready(function(){
$('#info_form').ajaxForm(function() {
  $("#info_change").show();
  $("#job_change").hide();
  $("#location_change").hide();
})
$('#location_form').ajaxForm(function() {
  $("#location_change").show();
  $("#job_change").hide();
  $("#info_change").hide();
})
$('#job_form').ajaxForm(function() {
  $("#job_change").show();
  $("#location_change").hide();
  $("#info_change").hide();
})
});
//Form Alphanum Plugin Initiate
$('#username_form').alphanum();
$('#first_name_form').alpha();
$('#last_name_form').alphanum({
  allow : " -'",
  disallow:'0123456789'
});

//Switch through tabs

$('#myTab a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})
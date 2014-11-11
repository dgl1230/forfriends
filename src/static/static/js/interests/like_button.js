//Submit Form via Ajax//
$(document).ready(function(){
$('.interests_form_1').ajaxForm(function() {
});
$('.interests_form_1a').ajaxForm(function() {
});
$('.interests_form_1b').ajaxForm(function() {
});
$('.interests_form_1c').ajaxForm(function() {
});
$('.interests_form_2').ajaxForm(function() {
});
$('.interests_form_3').ajaxForm(function() {
});
$('.interests_form_4').ajaxForm(function() {
});
$('.interests_form_5').ajaxForm(function() {
});
$('.interests_form_6').ajaxForm(function() {
});
$('.interests_form_7').ajaxForm(function() {
});
$('.interests_form_8').ajaxForm(function() {
});
});

 //Change Button Value//
$('.btn-lg').click(function(){
	if($(this).val() == "Like it!") {
	$(this).val("Unlike");
	}
	else {
		$(this).val("Like it!");
	}
	$(this).toggleClass('liked');
	$(this).toggleClass('btn-lg');
});
$('.liked').click(function(){
	if($(this).val() == "Like it!") {
	$(this).val("Unlike");
	}
	else {
		$(this).val("Like it!");
	}
	$(this).toggleClass('btn-lg');
	$(this).toggleClass('liked');
});
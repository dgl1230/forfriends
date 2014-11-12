//Submit Form via Ajax//
$(document).ready(function(){
$('.interests_form_1').ajaxForm(function() {
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
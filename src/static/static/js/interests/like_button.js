//Submit Form via Ajax//
$(document).ready(function(){
$('.interests_form_1').ajaxForm(function() {
});
});

 //Change Button Value//
$('.btn-lg').click(function(){
	if($(this).val() == "Like it!") {
	$(this).val("Unlike");
	liked +=1;
	if (liked >= 10){
	$('.btn-lg').attr('disabled','disabled')
	}
	else{
		$('.btn-lg').removeAttr('disabled');
		$('.liked').removeAttr('disabled');		
	}
	}
	else {
		$(this).val("Like it!");
		liked -=1;
		if (liked >= 10){
		$('.btn-lg').attr('disabled','disabled')
		}
		else{
			$('.btn-lg').removeAttr('disabled');
			$('.liked').removeAttr('disabled');		
		}
	}
	$(this).toggleClass('liked');
	$(this).toggleClass('btn-lg');
	$('.liked').removeAttr('disabled');	
});


$('.liked').click(function(){
	if($(this).val() == "Like it!") {
	$(this).val("Unlike");
	liked +=1;
	if (liked >= 10){
	$('.btn-lg').attr('disabled','disabled')
	}
	else{
		$('.btn-lg').removeAttr('disabled');
		$('.liked').removeAttr('disabled');		
	}
	}
	else {
		$(this).val("Like it!");
		liked -=1;
		if (liked >= 10){
		$('.btn-lg').attr('disabled','disabled')
		}
		else{
			$('.btn-lg').removeAttr('disabled')	
			$('.liked').removeAttr('disabled');	
		}
	}
	$(this).toggleClass('btn-lg');
	$(this).toggleClass('liked');
	$('.liked').removeAttr('disabled');
});
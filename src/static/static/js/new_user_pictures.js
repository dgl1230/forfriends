$(document).ready(function() {
	var cookiename='user_pictures'
	var count = parseInt($.cookie('user_pictures'));
	if (count < 2) {
		$('#new_user_modal').modal('show');
	}
	else {
		$('#new_user_modal').modal('hide');
	}
});
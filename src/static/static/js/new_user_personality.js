$(document).ready(function() {
	var cookiename='user_personality';
	var count = parseInt($.cookie('user_personality'));
	if (count < 2) {
		$('#new_user_modal').modal('show');
	}
	else {
		$('#new_user_modal').modal('hide');
	}
});
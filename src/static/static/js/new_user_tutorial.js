$(document).ready(function() {
	var cookiename='user';
	var count = parseInt($.cookie('user'));
	if (count < 2) {
		$('#new_user_modal').modal('show');
	}
	else {
		$('#new_user_modal').modal('show');
	}
});
$(document).ready(function() {
	var cookiename='user_interests';
	var count = parseInt($.cookie('user_interests'));
	if (count < 2) {
		$('#new_user_modal').modal('show');
	}
	else {
		$('#new_user_modal').modal('hide');
	}
});
$(document).ready(function(){
		var cookiename='user_interests';
    if($.cookie(cookiename)) {
		$.cookie('user_interests',(parseInt($.cookie('user_interests')) + 1), {expires: 365, path: '/' });
	} else {
		$.cookie('user_interests',1,{expires:365,path:'/'});
		}
});
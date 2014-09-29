$(document).ready(function(){
		var cookiename='user_pictures';
    if($.cookie(cookiename)) {
		$.cookie('user_pictures',(parseInt($.cookie('user_pictures')) + 1), {expires: 365, path: '/' });
	} else {
		$.cookie('user_pictures',1,{expires:365,path:'/'});
		}
});
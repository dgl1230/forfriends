$(document).ready(function(){
		var cookiename='user_personality';
    if($.cookie(cookiename)) {
		$.cookie('user_personality',(parseInt($.cookie('user_personality')) + 1), {expires: 365, path: '/' });
	} else {
		$.cookie('user_personality',1,{expires:365,path:'/'});
		}
});
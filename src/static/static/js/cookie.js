$(document).ready(function(){
		var cookiename='user';
    if($.cookie(cookiename)) {
		$.cookie('user',(parseInt($.cookie('user')) + 1), {expires: 365, path: '/' });
	} else {
		$.cookie('user',1,{expires:365,path:'/'});
		}
});
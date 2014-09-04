//FWDR3DCarUtils
(function (window){
	
	var FWDR3DCarUtils = function(){};
	
	FWDR3DCarUtils.dumy = document.createElement("div");
	
	//###################################//
	/* String */
	//###################################//
	FWDR3DCarUtils.trim = function(str){
		if (str)
		{
			return str.replace(/\s/g, "");
		}
		else
		{
			return undefined;
		}
	};
			
	FWDR3DCarUtils.trimAndFormatUrl = function(str){
		str = str.toLocaleLowerCase();
		str = str.replace(/ /g, "-");
		str = str.replace(/ä/g, "a");
		str = str.replace(/â/g, "a");
		str = str.replace(/â/g, "a");
		str = str.replace(/à/g, "a");
		str = str.replace(/è/g, "e");
		str = str.replace(/é/g, "e");
		str = str.replace(/ë/g, "e");
		str = str.replace(/ï/g, "i");
		str = str.replace(/î/g, "i");
		str = str.replace(/ù/g, "u");
		str = str.replace(/ô/g, "o");
		str = str.replace(/ù/g, "u");
		str = str.replace(/û/g, "u");
		str = str.replace(/ÿ/g, "y");
		str = str.replace(/ç/g, "c");
		str = str.replace(/œ/g, "ce");
		return str;
	};
	
	FWDR3DCarUtils.splitAndTrim = function(str, trim_bl){
		var array = str.split(",");
		var length = array.length;
		for(var i=0; i<length; i++){
			if(trim_bl) array[i] = FWDR3DCarUtils.trim(array[i]);
		};
		return array;
	};

	//#############################################//
	//Array //
	//#############################################//
	FWDR3DCarUtils.indexOfArray = function(array, prop){
		var length = array.length;
		for(var i=0; i<length; i++){
			if(array[i] === prop) return i;
		};
		return -1;
	};
	
	FWDR3DCarUtils.randomizeArray = function(aArray) {
		var randomizedArray = [];
		var copyArray = aArray.concat();
			
		var length = copyArray.length;
		for(var i=0; i< length; i++) {
				var index = Math.floor(Math.random() * copyArray.length);
				randomizedArray.push(copyArray[index]);
				copyArray.splice(index,1);
			}
		return randomizedArray;
	};
	

	//#############################################//
	/*DOM manipulation */
	//#############################################//
	FWDR3DCarUtils.parent = function (e, n){
		if(n === undefined) n = 1;
		while(n-- && e) e = e.parentNode;
		if(!e || e.nodeType !== 1) return null;
		return e;
	};
	
	FWDR3DCarUtils.sibling = function(e, n){
		while (e && n !== 0){
			if(n > 0){
				if(e.nextElementSibling){
					 e = e.nextElementSibling;	 
				}else{
					for(var e = e.nextSibling; e && e.nodeType !== 1; e = e.nextSibling);
				}
				n--;
			}else{
				if(e.previousElementSibling){
					 e = e.previousElementSibling;	 
				}else{
					for(var e = e.previousSibling; e && e.nodeType !== 1; e = e.previousSibling);
				}
				n++;
			}
		}
		return e;
	};
	
	FWDR3DCarUtils.getChildAt = function (e, n){
		var kids = FWDR3DCarUtils.getChildren(e);
		if(n < 0) n += kids.length;
		if(n < 0) return null;
		return kids[n];
	};
	
	FWDR3DCarUtils.getChildById = function(id){
		return document.getElementById(id) || undefined;
	};
	
	FWDR3DCarUtils.getChildren = function(e, allNodesTypes){
		var kids = [];
		for(var c = e.firstChild; c != null; c = c.nextSibling){
			if(allNodesTypes){
				kids.push(c);
			}else if(c.nodeType === 1){
				kids.push(c);
			}
		}
		return kids;
	};
	
	FWDR3DCarUtils.getChildrenFromAttribute = function(e, attr, allNodesTypes){
		var kids = [];
		for(var c = e.firstChild; c != null; c = c.nextSibling){
			if(allNodesTypes && FWDR3DCarUtils.hasAttribute(c, attr)){
				kids.push(c);
			}else if(c.nodeType === 1 && FWDR3DCarUtils.hasAttribute(c, attr)){
				kids.push(c);
			}
		}
		return kids.length == 0 ? undefined : kids;
	};
	
	FWDR3DCarUtils.getChildFromNodeListFromAttribute = function(e, attr, allNodesTypes){
		for(var c = e.firstChild; c != null; c = c.nextSibling){
			if(allNodesTypes && FWDR3DCarUtils.hasAttribute(c, attr)){
				return c;
			}else if(c.nodeType === 1 && FWDR3DCarUtils.hasAttribute(c, attr)){
				return c;
			}
		}
		return undefined;
	};
	
	FWDR3DCarUtils.getAttributeValue = function(e, attr){
		if(!FWDR3DCarUtils.hasAttribute(e, attr)) return undefined;
		return e.getAttribute(attr);	
	};
	
	FWDR3DCarUtils.hasAttribute = function(e, attr){
		if(e.hasAttribute){
			return e.hasAttribute(attr); 
		}else {
			var test = e.attributes[attr];
			return  test ? true : false;
		}
	};
	
	FWDR3DCarUtils.insertNodeAt = function(parent, child, n){
		var children = FWDR3DCarUtils.children(parent);
		if(n < 0 || n > children.length){
			throw new Error("invalid index!");
		}else {
			parent.insertBefore(child, children[n]);
		};
	};
	
	FWDR3DCarUtils.hasCanvas = function(){
		return Boolean(document.createElement("canvas"));
	};
	
	//###################################//
	/* DOM geometry */
	//##################################//
	FWDR3DCarUtils.hitTest = function(target, x, y){
		var hit = false;
		if(!target) throw Error("Hit test target is null!");
		var rect = target.getBoundingClientRect();
		
		if(x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) return true;
		return false;
	};
	
	FWDR3DCarUtils.getScrollOffsets = function(){
		//all browsers
		if(window.pageXOffset != null) return{x:window.pageXOffset, y:window.pageYOffset};
		
		//ie7/ie8
		if(document.compatMode == "CSS1Compat"){
			return({x:document.documentElement.scrollLeft, y:document.documentElement.scrollTop});
		}
	};
	
	FWDR3DCarUtils.getViewportSize = function(){
		if(FWDR3DCarUtils.hasPointerEvent && navigator.msMaxTouchPoints > 1){
			return {w:document.documentElement.clientWidth || window.innerWidth, h:document.documentElement.clientHeight || window.innerHeight};
		}
		
		if(FWDR3DCarUtils.isMobile) return {w:window.innerWidth, h:window.innerHeight};
		return {w:document.documentElement.clientWidth || window.innerWidth, h:document.documentElement.clientHeight || window.innerHeight};
	};
	
	FWDR3DCarUtils.getViewportMouseCoordinates = function(e){
		var offsets = FWDR3DCarUtils.getScrollOffsets();
		
		if(e.touches){
			return{
				screenX:e.changedTouches[0] == undefined ? e.changedTouches.pageX - offsets.x :e.changedTouches[0].pageX - offsets.x,
				screenY:e.changedTouches[0] == undefined ? e.changedTouches.pageY - offsets.y :e.changedTouches[0].pageY - offsets.y
			};
		}
		
		return{
			screenX: e.clientX == undefined ? e.pageX - offsets.x : e.clientX,
			screenY: e.clientY == undefined ? e.pageY - offsets.y : e.clientY
		};
	};
	
	
	//###################################//
	/* Browsers test */
	//##################################//
	FWDR3DCarUtils.hasPointerEvent = (function(){
		return Boolean(window.navigator.msPointerEnabled);
	}());
	
	FWDR3DCarUtils.isMobile = (function (){
		if(FWDR3DCarUtils.hasPointerEvent && navigator.msMaxTouchPoints > 1) return true;
		var agents = ['android', 'webos', 'iphone', 'ipad', 'blackberry'];
	    for(i in agents) {
	    	 if(navigator.userAgent.toLowerCase().indexOf(agents[i].toLowerCase()) != -1) {
	            return true;
	        }
	    }
	    return false;
	}());
	
	FWDR3DCarUtils.isAndroid = (function(){
		 return (navigator.userAgent.toLowerCase().indexOf("android".toLowerCase()) != -1);
	}());
	
	FWDR3DCarUtils.isChrome = (function(){
		return navigator.userAgent.toLowerCase().indexOf('chrome') != -1;
	}());
	
	FWDR3DCarUtils.isSafari = (function(){
		return navigator.userAgent.toLowerCase().indexOf('safari') != -1 && navigator.userAgent.toLowerCase().indexOf('chrome') == -1;
	}());
	
	FWDR3DCarUtils.isOpera = (function(){
		return navigator.userAgent.toLowerCase().indexOf('opera') != -1 && navigator.userAgent.toLowerCase().indexOf('chrome') == -1;
	}());
	
	FWDR3DCarUtils.isFirefox = (function(){
		return navigator.userAgent.toLowerCase().indexOf('firefox') != -1;
	}());
	
	FWDR3DCarUtils.isIE = (function(){
		return navigator.userAgent.toLowerCase().indexOf('msie') != -1;
	}());
	
	FWDR3DCarUtils.isIEAndLessThen9 = (function(){
		return navigator.userAgent.toLowerCase().indexOf("msie 7") != -1 || navigator.userAgent.toLowerCase().indexOf("msie 8") != -1;
	}());
	
	FWDR3DCarUtils.isIEAndLessThen10 = (function(){
		return navigator.userAgent.toLowerCase().indexOf("msie 7") != -1 || navigator.userAgent.toLowerCase().indexOf("msie 8") != -1 || navigator.userAgent.toLowerCase().indexOf("msie 9") != -1;
	}());

	FWDR3DCarUtils.isIEAndMoreThen8 = (function(){
		return FWDR3DCarUtils.isIE9 || FWDR3DCarUtils.isIE10 || FWDR3DCarUtils.isIE11;
	}());
	
	FWDR3DCarUtils.isIE7 = (function(){
		return navigator.userAgent.toLowerCase().indexOf("msie 7") != -1;
	}());

	FWDR3DCarUtils.isIE9 = (function(){
		return navigator.userAgent.toLowerCase().indexOf("msie 9") != -1;
	}());
	
	FWDR3DCarUtils.isIE10 = (function(){
		return navigator.userAgent.toLowerCase().indexOf("msie 10") != -1;
	}());
	
	FWDR3DCarUtils.isIE11 = (function(){
		return Boolean(!FWDR3DCarUtils.isIE && document.documentElement.msRequestFullscreen);
	}());
	
	FWDR3DCarUtils.isIEAndMoreThen9 = (function(){
		return FWDR3DCarUtils.isIE10 || FWDR3DCarUtils.isIE11;
	}());
	
	FWDR3DCarUtils.isApple = (function(){
		return navigator.appVersion.toLowerCase().indexOf('mac') != -1;;
	}());
	
	FWDR3DCarUtils.isAndroidAndWebkit = (function(){
		return  (FWDR3DCarUtils.isOpera || FWDR3DCarUtils.isChrome) && FWDR3DCarUtils.isAndroid;
	}());
	
	FWDR3DCarUtils.hasFullScreen = (function(){
		return FWDR3DCarUtils.dumy.requestFullScreen || FWDR3DCarUtils.dumy.mozRequestFullScreen || FWDR3DCarUtils.dumy.webkitRequestFullScreen || FWDR3DCarUtils.dumy.msieRequestFullScreen;
	}());
	
	function get3d(){
	    var properties = ['transform', 'msTransform', 'WebkitTransform', 'MozTransform', 'OTransform', 'KhtmlTransform'];
	    var p;
	    var position;
	    while (p = properties.shift()) {
	       if (typeof FWDR3DCarUtils.dumy.style[p] !== 'undefined') {
	    	   FWDR3DCarUtils.dumy.style.position = "absolute";
	    	   position = FWDR3DCarUtils.dumy.getBoundingClientRect().left;
	    	   FWDR3DCarUtils.dumy.style[p] = 'translate3d(500px, 0px, 0px)';
	    	   position = Math.abs(FWDR3DCarUtils.dumy.getBoundingClientRect().left - position);
	    	   
	           if(position > 100 && position < 900){
	        	   try{document.documentElement.removeChild(FWDR3DCarUtils.dumy);}catch(e){}
	        	   return true;
	           }
	       }
	    }
	    try{document.documentElement.removeChild(FWDR3DCarUtils.dumy);}catch(e){}
	    return false;
	};
	
	function get2d(){
	    var properties = ['transform', 'msTransform', 'WebkitTransform', 'MozTransform', 'OTransform', 'KhtmlTransform'];
	    var p;
	    while (p = properties.shift()) {
	       if (typeof FWDR3DCarUtils.dumy.style[p] !== 'undefined') {
	    	   return true;
	       }
	    }
	    try{document.documentElement.removeChild(FWDR3DCarUtils.dumy);}catch(e){}
	    return false;
	};
	
	//###############################################//
	/* various utils */
	//###############################################//
	FWDR3DCarUtils.onReady = function(callbalk){
		if (document.addEventListener) {
			document.addEventListener( "DOMContentLoaded", function(){
				FWDR3DCarUtils.checkIfHasTransofrms();
				callbalk();
			});
		}else{
			document.onreadystatechange = function () {
				FWDR3DCarUtils.checkIfHasTransofrms();
				if (document.readyState == "complete") callbalk();
			};
		 }
		
	};
	
	FWDR3DCarUtils.checkIfHasTransofrms = function()
	{
		if (FWDR3DCarUtils.isReadyMethodCalled_bl)
			return;
		
		document.documentElement.appendChild(FWDR3DCarUtils.dumy);
		FWDR3DCarUtils.hasTransform3d = get3d();
		FWDR3DCarUtils.hasTransform2d = get2d();
		
		FWDR3DCarUtils.isReadyMethodCalled_bl = true;
	};
	
	FWDR3DCarUtils.disableElementSelection = function(e){
		try{e.style.userSelect = "none";}catch(e){};
		try{e.style.MozUserSelect = "none";}catch(e){};
		try{e.style.webkitUserSelect = "none";}catch(e){};
		try{e.style.khtmlUserSelect = "none";}catch(e){};
		try{e.style.oUserSelect = "none";}catch(e){};
		try{e.style.msUserSelect = "none";}catch(e){};
		try{e.msUserSelect = "none";}catch(e){};
		e.onselectstart = function(){return false;};
	};
	
	FWDR3DCarUtils.getUrlArgs = function urlArgs(string){
		var args = {};
		var query = string.substr(string.indexOf("?") + 1) || location.search.substring(1);
		var pairs = query.split("&");
		for(var i=0; i< pairs.length; i++){
			var pos = pairs[i].indexOf("=");
			var name = pairs[i].substring(0,pos);
			var value = pairs[i].substring(pos + 1);
			value = decodeURIComponent(value);
			args[name] = value;
		}
		return args;
	};
	
	FWDR3DCarUtils.validateEmail = function(mail){  
		if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail)){  
			return true;  
		}  
		return false;  
    }; 
    
	//################################//
	/* resize utils */
	//################################//
	FWDR3DCarUtils.resizeDoWithLimit = function(
			displayObject,
			containerWidth,
			containerHeight,
			doWidth,
			doHeight,
			removeWidthOffset,
			removeHeightOffset,
			offsetX,
			offsetY,
			animate,
			pDuration,
			pDelay,
			pEase
		) {
		var containerWidth = containerWidth - removeWidthOffset;
		var containerHeight = containerHeight - removeHeightOffset;
			
		var scaleX = containerWidth/doWidth;
		var scaleY = containerHeight/doHeight;
		var totalScale = 0;
				
		if(scaleX <= scaleY){
			totalScale = scaleX;
		}else if(scaleX >= scaleY){
			totalScale = scaleY;
		}
			
		var finalWidth = Math.round((doWidth * totalScale));
		var finalHeight = Math.round((doHeight * totalScale));
		var x = Math.floor((containerWidth -  (doWidth * totalScale))/2  + offsetX);
		var y = Math.floor((containerHeight -  (doHeight * totalScale))/2 + offsetY);
			
		if(animate){
			FWDR3DCarModTweenMax.to(displayObject, pDuration, {x:x, y:y, w:finalWidth, h:finalHeight, delay:pDelay, ease:pEase});
		}else{
			displayObject.x = x;
			displayObject.y = y;
			displayObject.w = finalWidth;
			displayObject.h = finalHeight;
		}
	};
	
	//#########################################//
	/* request animation frame */
	//########################################//
	window.requestAnimFrame = (function(){
	    return  window.requestAnimationFrame || 
	        window.webkitRequestAnimationFrame || 
	        window.mozRequestAnimationFrame || 
	        window.oRequestAnimationFrame || 
	        window.msRequestAnimationFrame || 
	        function(/* function */ callback, /* DOMElement */ element){
	            return window.setTimeout(callback, 1000 / 60);
	        };
	})();
	
	window.cancelRequestAnimFrame = ( function() {
	    return window.cancelAnimationFrame ||
	        window.webkitCancelRequestAnimationFrame ||
	        window.mozCancelRequestAnimationFrame ||
	        window.oCancelRequestAnimationFrame ||
	        window.msCancelRequestAnimationFrame ||
	        clearTimeout;
	} )();
	
	FWDR3DCarUtils.isReadyMethodCalled_bl = false;
	
	window.FWDR3DCarUtils = FWDR3DCarUtils;
}(window));

(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame']
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }
 
    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); },
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
 
    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());
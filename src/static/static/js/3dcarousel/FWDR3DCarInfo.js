/* Info screen */
(function (window){
	
	var FWDR3DCarInfo = function(){
		
		var self = this;
		var prototype = FWDR3DCarInfo.prototype;
		
		/* init */
		this.init = function(){
			this.setWidth(500);
			this.setBkColor("#FF0000");
			this.getStyle().padding = "10px";
		};
		
		this.showText = function(txt){
			this.setInnerHTML(txt);
		};
		
		/* destroy */
		this.destroy = function(){

			prototype.destroy();
			FWDR3DCarInfo.prototype = null;
			self = null;
		};
		
		this.init();
	};
		
	/* set prototype */
	FWDR3DCarInfo.setPrototype = function(){
		FWDR3DCarInfo.prototype = new FWDR3DCarDisplayObject("div", "relative");
	};
	
	FWDR3DCarInfo.prototype = null;
	window.FWDR3DCarInfo = FWDR3DCarInfo;
}(window));
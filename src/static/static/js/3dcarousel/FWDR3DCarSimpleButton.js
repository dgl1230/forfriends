/* FWDR3DCarSimpleButton */
(function (window){
var FWDR3DCarSimpleButton = function(nImg, sImg){
		
		var self = this;
		var prototype = FWDR3DCarSimpleButton.prototype;
		
		this.nImg = nImg;
		this.sImg = sImg;
		
		this.n_do;
		this.s_do;
		
		this.isMobile_bl = FWDR3DCarUtils.isMobile;
		this.hasPointerEvent_bl = FWDR3DCarUtils.hasPointerEvent;
		
		//##########################################//
		/* initialize this */
		//##########################################//
		this.init = function(){
			this.setupMainContainers();
		};
		
		//##########################################//
		/* setup main containers */
		//##########################################//
		this.setupMainContainers = function(){
			this.n_do = new FWDR3DCarSimpleDisplayObject("img");	
			this.n_do.setScreen(this.nImg);
			this.s_do = new FWDR3DCarSimpleDisplayObject("img");
			this.s_do.setScreen(this.sImg);
			this.addChild(this.s_do);
			this.addChild(this.n_do);
			
			this.setWidth(this.nImg.width);
			this.setHeight(this.nImg.height);
			this.setButtonMode(true);
			
			if(self.isMobile_bl){
				if(self.hasPointerEvent_bl){
					self.screen.addEventListener("MSPointerOver", self.onMouseOver);
					self.screen.addEventListener("MSPointerOut", self.onMouseOut);
					self.screen.addEventListener("MSPointerUp", self.onClick);
				}else{
					self.screen.addEventListener("touchstart", self.onClick);
				}
			}else if(self.screen.addEventListener){	
				self.screen.addEventListener("mouseover", self.onMouseOver);
				self.screen.addEventListener("mouseout", self.onMouseOut);
				self.screen.addEventListener("mouseup", self.onClick);
			}else if(self.screen.attachEvent){
				self.screen.attachEvent("onmouseover", self.onMouseOver);
				self.screen.attachEvent("onmouseout", self.onMouseOut);
				self.screen.attachEvent("onmouseup", self.onClick);
			}
		};
		
		this.onMouseOver = function(e){
			if(!e.pointerType || e.pointerType == e.MSPOINTER_TYPE_MOUSE){
				FWDR3DCarModTweenMax.to(self.n_do, .9, {alpha:0, ease:Expo.easeOut});
			}
		};
			
		this.onMouseOut = function(e){
			if(!e.pointerType || e.pointerType == e.MSPOINTER_TYPE_MOUSE){
				FWDR3DCarModTweenMax.to(self.n_do, .9, {alpha:1, ease:Expo.easeOu});	
			}
		};
			
		this.onClick = function(e){
			self.dispatchEvent(FWDR3DCarSimpleButton.CLICK);
		};
		
		//##############################//
		/* destroy */
		//##############################//
		this.destroy = function(){
			
			if(self.isMobile_bl){
				if(self.hasPointerEvent_bl){
					self.screen.removeEventListener("MSPointerOver", self.onMouseOver);
					self.screen.removeEventListener("MSPointerOut", self.onMouseOut);
					self.screen.removeEventListener("MSPointerUp", self.onClick);
				}else{
					self.screen.removeEventListener("touchstart", self.onClick);
				}
			}else if(self.screen.removeEventListener){	
				self.screen.removeEventListener("mouseover", self.onMouseOver);
				self.screen.removeEventListener("mouseout", self.onMouseOut);
				self.screen.removeEventListener("mouseup", self.onClick);
			}else if(self.screen.detachEvent){
				self.screen.detachEvent("onmouseover", self.onMouseOver);
				self.screen.detachEvent("onmouseout", self.onMouseOut);
				self.screen.detachEvent("onmouseup", self.onClick);
			}
			
			FWDR3DCarModTweenMax.killTweensOf(self.n_do);
			self.n_do.destroy();
			self.s_do.destroy();
			
			self.nImg = null;
			self.sImg = null;
			self.n_do = null;
			self.s_do = null;
			
			nImg = null;
			sImg = null;
			
			self.setInnerHTML("");
			prototype.destroy();
			self = null;
			prototype = null;
			FWDR3DCarSimpleButton.prototype = null;
		};
	
		this.init();
	};
	
	/* set prototype */
	FWDR3DCarSimpleButton.setPrototype = function(){
		FWDR3DCarSimpleButton.prototype = null;
		FWDR3DCarSimpleButton.prototype = new FWDR3DCarDisplayObject("div");
	};
	
	FWDR3DCarSimpleButton.CLICK = "onClick";
	
	FWDR3DCarSimpleButton.prototype = null;
	window.FWDR3DCarSimpleButton = FWDR3DCarSimpleButton;
}(window));
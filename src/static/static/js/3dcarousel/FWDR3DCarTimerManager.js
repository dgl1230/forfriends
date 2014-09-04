/* Slide show time manager */
(function(window){
	
	var FWDR3DCarTimerManager = function(delay, autoplay){
		
		var self = this;
		var prototpype = FWDR3DCarTimerManager.prototype;
		
		this.timeOutId;
		this.delay = delay;
		this.isStopped_bl = !autoplay;
		
		this.stop = function(){
			clearTimeout(this.timeOutId);
			this.dispatchEvent(FWDR3DCarTimerManager.STOP);
		};
		
		this.start = function(){
			if(!this.isStopped_bl){
				this.timeOutId = setTimeout(this.onTimeHanlder, this.delay);
				this.dispatchEvent(FWDR3DCarTimerManager.START);
			}
		};
		
		this.onTimeHanlder = function(){
			self.dispatchEvent(FWDR3DCarTimerManager.TIME);
		};
		
		/* destroy */
		this.destroy = function(){
			
			clearTimeout(this.timeOutId);
			
			prototpype.destroy();
			self = null;
			prototpype = null;
			FWDR3DCarTimerManager.prototype = null;
		};
	};

	FWDR3DCarTimerManager.setProtptype = function(){
		FWDR3DCarTimerManager.prototype = new FWDR3DCarEventDispatcher();
	};
	
	FWDR3DCarTimerManager.START = "start";
	FWDR3DCarTimerManager.STOP = "stop";
	FWDR3DCarTimerManager.TIME = "time";
	
	FWDR3DCarTimerManager.prototype = null;
	window.FWDR3DCarTimerManager = FWDR3DCarTimerManager;
	
}(window));
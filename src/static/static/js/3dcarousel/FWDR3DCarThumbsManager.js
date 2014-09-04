/* thumbs manager */
(function(window)
{
	var FWDR3DCarThumbsManager = function(data, parent)
	{
		var self = this;
		var prototype = FWDR3DCarThumbsManager.prototype;

		this.data = data;
		this.parent = parent;
		
		this.stageWidth = parent.stageWidth;
		this.stageHeight = parent.stageHeight;
		
		this.thumbsHolderDO;

		this.totalThumbs;
		this.thumbsAr = [];
		
		this.dataListId = data.startAtCategory;
		
		this.curDataListAr;
		
		this.nrThumbsToDisplay = data.nrThumbsToDisplay;
		
		this.dragCurId;
		this.prevCurId;
		this.curId;
		
		this.thumbWidth = data.thumbWidth;
		this.thumbHeight = data.thumbHeight;
		
		this.borderSize = data.thumbBorderSize;
		
		this.perspective = self.thumbWidth;
		
		this.sizeRatio = self.thumbWidth / 400;
		
		this.countLoadedThumbsLeft;
		this.countLoadedThumbsRight;
		
		this.controlsDO;
		this.prevButtonDO;
		this.nextButtonDO;
		this.scrollbarDO;
		this.slideshowButtonDO;
		
		this.showSlideshowButton = self.data.showSlideshowButton || self.data.autoplay;
		
		this.controlsHeight = self.data.nextButtonNImg.height;
		this.showText = self.data.showText;
		
		this.textDO;
		this.textHolderDO;
		this.textGradientDO;
		this.thumbOverDO;
		
		this.showRefl = data.showRefl;
		this.reflHeight = data.reflHeight;
		this.reflDist = data.reflDist;
		this.reflAlpha = data.reflAlpha;
		
		this.isThumbOver = false;
		this.hasThumbText = false;
		
		this.introFinished = false;
		this.isPlaying = false;
		this.disableThumbClick = false;
		this.isTextSet = false;
		this.allowToSwitchCat = false;
		
		this.hasPointerEvent = FWDR3DCarUtils.hasPointerEvent;
		this.isMobile = FWDR3DCarUtils.isMobile;

		this.loadWithDelayIdLeft;
		this.loadWithDelayIdRight;
		this.slideshowTimeoutId;
		this.textTimeoutId;
		this.zSortingId;
		this.hideThumbsFinishedId;
		this.loadHtmlContentsId;
		this.loadImagesId;
		this.setTextHeightId;
		this.setIntroFinishedId;
		this.showControlsId;

		/* init */
		this.init = function()
		{
			self.thumbsHolderDO = new FWDR3DCarDisplayObject3D("div", "absolute", "visible");
			self.addChild(self.thumbsHolderDO);
			
			self.thumbsHolderDO.setZ(100000);
			
			self.thumbsHolderDO.setPerspective(self.perspective);
			
			self.thumbsHolderDO.setX(Math.floor(self.stageWidth/2));
			self.thumbsHolderDO.setY(Math.floor(self.stageHeight/2 - self.data.prevButtonNImg.height/2));
			
			if ((!self.isMobile && !FWDR3DCarUtils.isSafari) || FWDR3DCarUtils.isAndroidAndWebkit)
			{
				self.thumbsHolderDO.setPreserve3D();
			}		
			
			if (!self.isMobile)
			{
				if (self.screen.addEventListener)
				{
					window.addEventListener("mousemove", self.onThumbMove);
				}
				else
				{
					document.attachEvent("onmousemove", self.onThumbMove);
				}
			}
			
			if (self.hasPointerEvent)
			{
				window.addEventListener("MSPointerMove", self.onThumbMove);
			}
			
			self.showScrollbar = data.showScrollbar;
			self.showNextButton = data.showNextButton;
			self.showPrevButton = data.showPrevButton;
			
			if (self.isMobile)
			{
				if (data.disableScrollbarOnMobile)
				{
					self.showScrollbar = false;
				}
				
				if (data.disableNextAndPrevButtonsOnMobile)
				{
					self.showNextButton = false;
					self.showPrevButton = false;
				}	
			}
			
			if (self.showText)
			{
				self.setupText();
				
				if (self.isMobile)
				{
					self.setupThumbOver();
				}
			}
			
			self.showCurrentCat(-1);
			
			self.setupControls();
		};
		
		this.onThumbMove = function(e)
		{
			if (!self.textHolderDO)
				return;
			
			if (self.disableThumbClick)
				return;
			
			var viewportMouseCoordinates = FWDR3DCarUtils.getViewportMouseCoordinates(e);
			
			self.thumbMouseX = viewportMouseCoordinates.screenX - parent.rect.left - (self.stageWidth - self.thumbWidth)/2;
			self.thumbMouseY = viewportMouseCoordinates.screenY - parent.rect.top - (self.stageHeight - data.prevButtonNImg.height - self.thumbHeight)/2;
			
			if (self.isTextSet)
			{
				if (self.isMobile)
				{
					self.checkThumbOver();
				}
				else
				{
					self.thumbsAr[self.curId].checkThumbOver();
				}
			}
		};
		
		//##############################################//
		/* show current cat */
		//##############################################//
		this.showCurrentCat = function(id)
		{
			if ((id != self.dataListId) && (id >= 0))
			{
				self.allowToSwitchCat = false;
				self.hideCurrentCat();
				self.dataListId = id;
				
				return;
			}
			
			self.thumbsAr = [];
			self.curDataListAr = self.data.dataListAr[self.dataListId];
			self.totalThumbs = self.curDataListAr.length;
			
			if (self.totalThumbs == 0)
			{
				var message = "This category doesn't contain any thumbnails!";

				self.dispatchEvent(FWDR3DCarThumbsManager.LOAD_ERROR, {text : message});
				
				return;
			}
			
			if (self.isMobile)
			{
				 self.totalThumbs = Math.min(self.totalThumbs, data.maxNumberOfThumbsOnMobile);
			}
			
			switch (self.data.carouselStartPosition)
			{
				case "left":
					self.curId = 0;
					break;
				case "right":
					self.curId = self.totalThumbs-1;
					break;
				default:
					self.curId = Math.floor((self.totalThumbs-1)/2);
			}
			
			if (self.showScrollbar && self.scrollbarDO)
			{
				self.scrollbarDO.totalItems = self.totalThumbs;
				self.scrollbarDO.curItemId = self.curId;
				self.scrollbarDO.gotoItem2();
			}
			
			self.setupThumbs();
			
			self.prevCurId = self.curId;
			
			self.startIntro();
		};
		
		//################################################//
		/* hide current cat */
		//################################################//
		this.hideCurrentCat = function()
		{
			clearTimeout(self.loadWithDelayIdLeft);
			clearTimeout(self.loadWithDelayIdRight);
			clearTimeout(self.textTimeoutId);
			clearInterval(self.zSortingId);
			clearTimeout(self.hideThumbsFinishedId);
			clearTimeout(self.loadHtmlContentsId);
			clearTimeout(self.loadImagesId);
			clearTimeout(self.setTextHeightId);
			clearTimeout(self.setIntroFinishedId);
			clearTimeout(self.showControlsId);
			
			self.stopSlideshow();
			
			self.disableThumbClick = true;
			
			if (self.image)
			{
				self.image.onload = null;
				self.image.onerror = null;
			}
			
			if (self.imageLeft)
			{
				self.imageLeft.onload = null;
				self.imageLeft.onerror = null;
			}
			
			if (self.imageRight)
			{
				self.imageRight.onload = null;
				self.imageRight.onerror = null;
			}
			
			self.hideThumbs();
		};
		
		this.hideThumbs = function()
		{
			var delay;
			
			var newX = -self.thumbWidth/2;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				
				if (i == self.curId)
				{
					self.hideThumbsFinishedId = setTimeout(self.hideThumbsFinished, 1200 + 500);
				}
				else if (Math.abs(i - self.curId) <= self.nrThumbsToDisplay)
				{
					delay = (self.nrThumbsToDisplay - Math.abs(i - self.curId) + 1) * 300;
					FWDR3DCarModTweenMax.to(thumb, .5, {x:Math.floor(newX), delay:delay/1000, ease:Expo.easeIn});
					thumb.hide((delay - 250)/1000);
				}
				else
				{
					thumb.setX(newX);
				}
			}
		};
		
		this.hideThumbsFinished = function()
		{
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				
				if (i == self.curId)
				{
					thumb.hide(0);
					FWDR3DCarModTweenMax.to(thumb, .6, {alpha:0, delay:.2, onComplete:self.allThumbsAreTweened});
					
					if (self.isMobile && self.textHolderDO)
					{
						FWDR3DCarModTweenMax.to(self.textHolderDO, .6, {alpha:0, delay:.2, ease:Expo.easeOut});
						FWDR3DCarModTweenMax.to(self.textGradientDO, .6, {alpha:0, delay:.2, ease:Expo.easeOut});
					}
				}
				else
				{
					thumb.setAlpha(0);
				}
			}
		};
		
		this.allThumbsAreTweened = function()
		{
			self.destroyCurrentCat();
			self.showCurrentCat();
		};
		
		this.destroyCurrentCat = function()
		{
			var thumb;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				FWDR3DCarModTweenMax.killTweensOf(thumb);
				self.thumbsHolderDO.removeChild(thumb);
				thumb.destroy();
				thumb = null;
			}
		};
		
		this.startIntro = function()
		{
			self.disableThumbClick = true;
			
			thumb = self.thumbsAr[self.curId];
			
			var newX = -self.thumbWidth/2;
			var newY = -self.thumbHeight/2;
			
			thumb.setGradient(0);
			
			thumb.setX(Math.floor(newX));
			thumb.setY(Math.floor(newY));
			
			thumb.setAlpha(0);
			FWDR3DCarModTweenMax.to(thumb, .8, {alpha:1});
			
			self.thumbsHolderDO.addChild(thumb);
			
			if (self.data.showThumbnailsHtmlContent)
			{
				self.loadCenterHtmlContent();
				self.loadHtmlContentsId = setTimeout(self.loadHtmlContents, 600);
			}
			else
			{
				self.loadCenterImage();
				self.loadImagesId = setTimeout(self.loadImages, 600);
			}
		};

		/* setup thumbs */
		this.setupThumbs = function()
		{
			var thumb;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				FWDR3DCarThumb.setPrototype();
				
				thumb = new FWDR3DCarThumb(i, self.data, self);
				
				self.thumbsAr.push(thumb);
				
				thumb.addListener(FWDR3DCarThumb.CLICK, self.onThumbClick);
			}
		};
		
		this.onThumbClick = function(e)
		{
			if (self.disableThumbClick)
				return;
			
			self.curId = e.id;
			
			self.thumbClickHandler();
		};
		
		this.thumbClickHandler = function()
		{
			if (self.curId != self.prevCurId)
			{
				self.gotoThumb();
			}
			else
			{
				var type = self.curDataListAr[self.curId].mediaType;
				var tempId = self.curId;
				
				if (type == "none")
				{
					return;
				}
				
				if (type != "link")
				{
					for (var i=0; i<self.totalThumbs; i++)
					{
						if ((i < self.curId) && ((self.curDataListAr[i].mediaType == "link") || (self.curDataListAr[i].mediaType == "none")))
						{
							tempId -= 1;
						}
					};
				}
				
				if (type == "link")
				{
					window.open(self.curDataListAr[self.curId].secondObj.url, self.curDataListAr[self.curId].secondObj.target);
				}
				else
				{
					self.dispatchEvent(FWDR3DCarThumbsManager.THUMB_CLICK, {id:tempId});
				}
			}
		};
		
		this.resizeHandler = function()
		{
			if ((self.stageWidth == parent.stageWidth) && (self.stageHeight == parent.stageHeight))
					return;
			
			self.stageWidth = parent.stageWidth;
			self.stageHeight = parent.stageHeight;
			
			self.thumbsHolderDO.setX(Math.floor(self.stageWidth/2));
			self.thumbsHolderDO.setY(Math.floor(self.stageHeight/2 - self.data.prevButtonNImg.height/2));
			
			self.positionControls();
			
			if (self.textHolderDO && self.isMobile)
			{
				self.textHolderDO.setX(Math.floor((self.stageWidth - self.thumbWidth)/2) + self.borderSize);
				self.textHolderDO.setY(Math.floor((self.stageHeight - self.thumbHeight)/2 - self.data.prevButtonNImg.height/2) + self.borderSize);
			}
			
			if (self.thumbOverDO)
			{
				self.thumbOverDO.setX(Math.floor((self.stageWidth - self.thumbWidth)/2));
				self.thumbOverDO.setY(Math.floor((self.stageHeight - self.thumbHeight - self.data.prevButtonNImg.height)/2));
			}
		};
		
		this.setupText = function()
		{
			self.textHolderDO = new FWDR3DCarDisplayObject3D("div");
			self.addChild(self.textHolderDO);
			
			if (self.isMobile)
			{
				self.textHolderDO.setZ(200000);
			}
			
			self.textHolderDO.setWidth(self.thumbWidth - self.borderSize * 2);
			self.textHolderDO.setHeight(self.thumbHeight - self.borderSize * 2);
			
			if (self.isMobile)
			{
				self.textHolderDO.setX(Math.floor((self.stageWidth - self.thumbWidth)/2) + self.borderSize);
				self.textHolderDO.setY(Math.floor((self.stageHeight - self.thumbHeight - self.data.prevButtonNImg.height)/2) + self.borderSize);
			}
			else
			{
				self.textHolderDO.setX(-1000);
			}
			
			if (self.data.showTextBackgroundImage)
			{
				self.textGradientDO = new FWDR3DCarSimpleDisplayObject("img");
				self.textHolderDO.addChild(self.textGradientDO);
				
				self.textGradientDO.setWidth(self.thumbWidth - self.borderSize * 2);
				self.textGradientDO.setHeight(self.thumbHeight - self.borderSize * 2);
				
				self.textGradientDO.screen.src = data.thumbTitleGradientPath;
			}
			else
			{
				self.textGradientDO = new FWDR3DCarSimpleDisplayObject("div");
				self.textHolderDO.addChild(self.textGradientDO);
				
				self.textGradientDO.setWidth(self.thumbWidth - self.borderSize * 2);
				self.textGradientDO.setHeight(self.thumbHeight - self.borderSize * 2);
				
				self.textGradientDO.setBkColor(self.data.textBackgroundColor);
				self.textGradientDO.setAlpha(self.data.textBackgroundOpacity);
			}
			
			self.textDO = new FWDR3DCarSimpleDisplayObject("div");
			self.textHolderDO.addChild(self.textDO);
			
			self.textDO.setWidth(self.thumbWidth - self.borderSize * 2);
			
			self.textDO.getStyle().fontSmoothing = "antialiased";
			self.textDO.getStyle().webkitFontSmoothing = "antialiased";
			self.textDO.getStyle().textRendering = "optimizeLegibility";
		};
		
		this.setupThumbOver = function()
		{
			self.thumbOverDO = new FWDR3DCarDisplayObject("div");
			self.addChild(self.thumbOverDO);
			
			if (!self.isMobile)
			{
				self.thumbOverDO.setButtonMode(true);
			}
			
			if (FWDR3DCarUtils.isIE)
			{
				self.thumbOverDO.setBkColor("#000000");
				self.thumbOverDO.setAlpha(.001);
			}
			
			self.thumbOverDO.setWidth(self.thumbWidth);
			self.thumbOverDO.setHeight(self.thumbHeight);
			
			self.thumbOverDO.setX(Math.floor((self.stageWidth - self.thumbWidth)/2));
			self.thumbOverDO.setY(Math.floor((self.stageHeight - self.thumbHeight - self.data.prevButtonNImg.height)/2));
			
			if (self.isMobile)
			{
				if (self.hasPointerEvent)
				{
					self.thumbOverDO.screen.addEventListener("MSPointerUp", self.onThumbOverTouch);
				}
				else
				{
					self.thumbOverDO.screen.addEventListener("touchend", self.onThumbOverTouch);
				}
			}
			else
			{
				if (self.screen.addEventListener)
				{
					self.thumbOverDO.screen.addEventListener("click", self.onThumbOverClick);
				}
				else
				{
					self.thumbOverDO.screen.attachEvent("onclick", self.onThumbOverClick);
				}
			}
		};
		
		this.onThumbOverClick = function()
		{
			if (self.disableThumbClick)
				return;
			
			self.thumbClickHandler();
		};
		
		this.onThumbOverTouch = function(e)
		{
			if(e.preventDefault) e.preventDefault();
			
			if (self.disableThumbClick)
				return;
			
			self.thumbClickHandler();
		};
		
		this.addThumbText = function()
		{
			self.textHolderDO.setY(Math.floor((self.stageHeight - self.thumbHeight - self.data.prevButtonNImg.height)/2) + self.borderSize);

			self.textDO.setInnerHTML(self.curDataListAr[self.curId].thumbText);
			
			self.textTitleOffset = self.curDataListAr[self.curId].textTitleOffset;
			self.textDescriptionOffsetTop = self.curDataListAr[self.curId].textDescriptionOffsetTop;
			self.textDescriptionOffsetBottom = self.curDataListAr[self.curId].textDescriptionOffsetBottom;
			
			self.textGradientDO.setY(self.thumbHeight - self.borderSize * 2 - self.textTitleOffset);
			self.textDO.setY(self.thumbHeight - self.borderSize * 2 - self.textTitleOffset + self.textDescriptionOffsetTop);
			
			self.textHolderDO.setAlpha(0);
	
			self.setTextHeightId = setTimeout(self.setTextHeight, 10);
		};
	
		this.setTextHeight = function()
		{	
			self.textHeight = self.textDO.getHeight();
			
			FWDR3DCarModTweenMax.to(self.textHolderDO, .8, {alpha:1, ease:Expo.easeOut});
			FWDR3DCarModTweenMax.to(self.textGradientDO, .8, {alpha:1, ease:Expo.easeOut});
			
			self.hasThumbText = true;
			
			self.checkThumbOver();
		};
		
		this.removeThumbText = function()
		{
			if (self.isMobile)
			{
				self.removeTextFinish();
			}
			else
			{
				FWDR3DCarModTweenMax.to(self.textHolderDO, .6, {alpha:0, ease:Expo.easeOut, onComplete:self.removeTextFinish});
			}
		};
		
		this.removeTextFinish = function()
		{
			FWDR3DCarModTweenMax.killTweensOf(self.textHolderDO);
			FWDR3DCarModTweenMax.killTweensOf(self.textGradientDO);
			FWDR3DCarModTweenMax.killTweensOf(self.textDO);
			
			self.hasThumbText = false;
			self.isThumbOver = false;
			
			self.textHolderDO.setY(2000);
		};
		
		this.checkThumbOver = function()
		{
			if (!self.hasThumbText)
				return;
			
			if ((self.thumbMouseX >= 0) && (self.thumbMouseX <= self.thumbWidth) && (self.thumbMouseY >= 0) && (self.thumbMouseY <= self.thumbHeight))
			{
				self.onThumbOverHandler();
			}
			else
			{
				self.onThumbOutHandler();
			}
		};
		
		this.onThumbOverHandler = function()
		{
			if (!self.isThumbOver)
			{
				self.isThumbOver = true;
				
				FWDR3DCarModTweenMax.to(self.textGradientDO, .8, {y:self.thumbHeight - self.borderSize * 2 - self.textDescriptionOffsetTop - self.textHeight - self.textDescriptionOffsetBottom, ease:Expo.easeOut});
				FWDR3DCarModTweenMax.to(self.textDO, .8, {y:self.thumbHeight - self.borderSize * 2 - self.textHeight - self.textDescriptionOffsetBottom, ease:Expo.easeOut});
			}
		};

		this.onThumbOutHandler = function()
		{
			if (self.isThumbOver)
			{
				self.isThumbOver = false;
				
				FWDR3DCarModTweenMax.to(self.textGradientDO, .8, {y:self.thumbHeight - self.borderSize * 2 - self.textTitleOffset, ease:Expo.easeOut});
				FWDR3DCarModTweenMax.to(self.textDO, .8, {y:self.thumbHeight - self.borderSize * 2 - self.textTitleOffset + self.textDescriptionOffsetTop, ease:Expo.easeOut});
			}
		};
		
		this.loadImages = function()
		{
			if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
			{	
				self.setupIntro3D();
			}
			else
			{
				self.setupIntro2D();
			}
			
			self.countLoadedThumbsLeft = self.curId - 1;
			self.loadWithDelayIdLeft = setTimeout(self.loadThumbImageLeft, 100);
			
			self.countLoadedThumbsRight = self.curId + 1;
			self.loadWithDelayIdRight = setTimeout(self.loadThumbImageRight, 100);
		};
		
		this.loadCenterImage = function()
		{
			self.imagePath = self.curDataListAr[self.curId].thumbPath;

			self.image = new Image();
			self.image.onerror = self.onImageLoadErrorHandler;
			self.image.onload = self.onImageLoadHandlerCenter;
			self.image.src = self.imagePath;
		};
		
		this.onImageLoadHandlerCenter = function(e)
		{
			var thumb = self.thumbsAr[self.curId];
			
			thumb.addImage(self.image);
			
			if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
			{
				thumb.showThumb3D();
			}
			else
			{
				thumb.showThumb2D();
			}
			
			if (self.showText)
			{
				self.isTextSet = true;
				
				if (self.isMobile)
				{
					self.addThumbText();
				}
				else
				{
					thumb.addText(self.textHolderDO, self.textGradientDO, self.textDO);
				}
			}
		};

		this.loadThumbImageLeft = function()
		{
			if (self.countLoadedThumbsLeft < 0)
					return;
			
			self.imagePath = self.curDataListAr[self.countLoadedThumbsLeft].thumbPath;

			self.imageLeft = new Image();
			self.imageLeft.onerror = self.onImageLoadErrorHandler;
			self.imageLeft.onload = self.onImageLoadHandlerLeft;
			self.imageLeft.src = self.imagePath;
		};

		this.onImageLoadHandlerLeft = function(e)
		{
			var thumb = self.thumbsAr[self.countLoadedThumbsLeft];

			thumb.addImage(self.imageLeft);
			
			if (Math.abs(self.countLoadedThumbsLeft - self.curId) <= self.nrThumbsToDisplay)
			{
				if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
				{
					thumb.showThumb3D();
				}
				else
				{
					thumb.showThumb2D();
				}
			}
			
			self.countLoadedThumbsLeft--;
			
			self.loadWithDelayIdLeft = setTimeout(self.loadThumbImageLeft, 200);
		};
		
		this.loadThumbImageRight = function()
		{
			if (self.countLoadedThumbsRight > self.totalThumbs-1)
				return;
			
			self.imagePath = self.curDataListAr[self.countLoadedThumbsRight].thumbPath;

			self.imageRight = new Image();
			self.imageRight.onerror = self.onImageLoadErrorHandler;
			self.imageRight.onload = self.onImageLoadHandlerRight;
			self.imageRight.src = self.imagePath;
		};

		this.onImageLoadHandlerRight = function(e)
		{
			var thumb = self.thumbsAr[self.countLoadedThumbsRight];

			thumb.addImage(self.imageRight);

			if (Math.abs(self.countLoadedThumbsRight - self.curId) <= self.nrThumbsToDisplay)
			{
				if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
				{
					thumb.showThumb3D();
				}
				else
				{
					thumb.showThumb2D();
				}
			}
			
			self.countLoadedThumbsRight++;
			
			self.loadWithDelayIdRight = setTimeout(self.loadThumbImageRight, 200);
		};

		this.onImageLoadErrorHandler = function(e)
		{
			if (!self || !self.data)
				return;

			var message = "Thumb can't be loaded, probably the path is incorrect <font color='#FFFFFF'>" + self.imagePath + "</font>";

			self.dispatchEvent(FWDR3DCarThumbsManager.LOAD_ERROR, {text : message});
		};
		
		this.loadHtmlContents = function()
		{
			if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
			{	
				self.setupIntro3D();
			}
			else
			{
				self.setupIntro2D();
			}
			
			self.countLoadedThumbsLeft = self.curId - 1;
			self.loadWithDelayIdLeft = setTimeout(self.loadThumbHtmlContentLeft, 100);
			
			self.countLoadedThumbsRight = self.curId + 1;
			self.loadWithDelayIdRight = setTimeout(self.loadThumbHtmlContentRight, 100);
		};
		
		this.loadCenterHtmlContent = function()
		{
			var thumb = self.thumbsAr[self.curId];

			thumb.addHtmlContent();
			
			if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
			{
				thumb.showThumb3D();
			}
			else
			{
				thumb.showThumb2D();
			}
			
			if (self.showText)
			{
				self.isTextSet = true;
				
				if (self.isMobile)
				{
					self.addThumbText();
				}
				else
				{
					thumb.addText(self.textHolderDO, self.textGradientDO, self.textDO);
				}
			}
		};

		this.loadThumbHtmlContentLeft = function()
		{
			if (self.countLoadedThumbsLeft < 0)
					return;
			
			var thumb = self.thumbsAr[self.countLoadedThumbsLeft];

			thumb.addHtmlContent();
			
			if (Math.abs(self.countLoadedThumbsLeft - self.curId) <= self.nrThumbsToDisplay)
			{
				if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
				{
					thumb.showThumb3D();
				}
				else
				{
					thumb.showThumb2D();
				}
			}
			
			self.countLoadedThumbsLeft--;
			
			self.loadWithDelayIdLeft = setTimeout(self.loadThumbHtmlContentLeft, 200);
		};

		this.loadThumbHtmlContentRight = function()
		{
			if (self.countLoadedThumbsRight > self.totalThumbs-1)
				return;
			
			var thumb = self.thumbsAr[self.countLoadedThumbsRight];

			thumb.addHtmlContent();

			if (Math.abs(self.countLoadedThumbsRight - self.curId) <= self.nrThumbsToDisplay)
			{
				if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
				{
					thumb.showThumb3D();
				}
				else
				{
					thumb.showThumb2D();
				}
			}
			
			self.countLoadedThumbsRight++;
			
			self.loadWithDelayIdRight = setTimeout(self.loadThumbHtmlContentRight, 200);
		};
		
		this.setupIntro3D = function()
		{
			var newX;
			var newY;
			var newZ;
			
			var newAngleX;
			var newAngleY;
			var newAngleZ;
			
			var delay;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				
				newX = 0;
				newY = 0;
				newZ = 0;
				
				newAngleX = 0;
				newAngleY = 0;
				newAngleZ = 0;
				
				newX -= self.thumbWidth/2;
				newY -= self.thumbHeight/2;
				
				var sgn = 0;
				
				if (i < self.curId)
				{
					sgn = -1;
				}
				else if (i > self.curId)
				{
					sgn = 1;
				}
				
				var lastX;
				var lastY;
				var lastZ;
				var lastAngleX;
				var lastAngleY;
				var lastAngleZ;
				
				switch (self.nrThumbsToDisplay)
				{
					case 1:
						lastX = 250 * sgn;
						lastY = -5;
						lastZ = -220;
						
						lastAngleX = 15;
						lastAngleY = 25 * sgn;
						lastAngleZ = -4 * sgn;
						break;
					case 2:
						lastX = 630 * sgn;
						lastY = 0;
						lastZ = -500;
						
						lastAngleX = 25;
						lastAngleY = 28 * sgn;
						lastAngleZ = -13 * sgn;
						break;
					case 3:
						lastX = 1130 * sgn;
						lastY = 0;
						lastZ = -900;
						
						lastAngleX = 32;
						lastAngleY = 28 * sgn;
						lastAngleZ = -20 * sgn;
						break;
					default:
						lastX = 1475 * sgn;
						lastY = -20;
						lastZ = -1200;
						
						lastAngleX = 50;
						lastAngleY = 20 * sgn;
						lastAngleZ = -28 * sgn;
				}
				
				switch (Math.abs(i - self.curId))
				{
					case 0:
						break;
					case 1:
							newZ = -120;
						break;
					case 2:
						if (self.nrThumbsToDisplay >= 2)
						{
							newZ = -400;
						}
						else
						{
							newZ = lastZ;
						}
						break;
					case 3:
						if (self.nrThumbsToDisplay >= 3)
						{
							newZ = -800;
						}
						else
						{
							newZ = lastZ;
						}
						break;
					case 4:
						if (self.nrThumbsToDisplay >= 4)
						{
							newZ = -1100;
						}
						else
						{
							newZ = lastZ;
						}
						break;
					default:
						newZ = lastZ;
				}
				
				thumb.setX(Math.floor(newX));
				thumb.setY(Math.floor(newY));
				thumb.setZ(Math.floor(newZ));
				
				newX = 0;
				newY = 0;
				newZ = 0;
				
				switch (Math.abs(i - self.curId))
				{
					case 0:
						if (FWDR3DCarUtils.isIEAndMoreThen9)
								thumb.setZIndex(5);
						break;
					case 1:
						newX = 350 * sgn;
						newY = -5;
						newZ = -126 - Math.floor(Math.max(self.thumbHeight - 266, 0) / 2.5);
						
						newAngleX = 15;
						newAngleY = 25 * sgn;
						newAngleZ = -4 * sgn;
						
						if (FWDR3DCarUtils.isIEAndMoreThen9)
							thumb.setZIndex(4);
						break;
					case 2:
						if (self.nrThumbsToDisplay >= 2)
						{
							newX = 730 * sgn;
							newZ = -400;
							
							newAngleX = 25;
							newAngleY = 28 * sgn;
							newAngleZ = -13 * sgn;
						}
						else
						{
							newX = lastX;
							newY = lastY;
							newZ = lastZ;
							
							newAngleX = lastAngleX;
							newAngleY = lastAngleY;
							newAngleZ = lastAngleZ;
						}
						
						if (FWDR3DCarUtils.isIEAndMoreThen9)
							thumb.setZIndex(3);
						break;
					case 3:
						if (self.nrThumbsToDisplay >= 3)
						{
							newX = 1230 * sgn;
							newZ = -800;
							
							newAngleX = 32;
							newAngleY = 28 * sgn;
							newAngleZ = -20 * sgn;
						}
						else
						{
							newX = lastX;
							newY = lastY;
							newZ = lastZ;
							
							newAngleX = lastAngleX;
							newAngleY = lastAngleY;
							newAngleZ = lastAngleZ;
						}
						
						if (FWDR3DCarUtils.isIEAndMoreThen9)
							thumb.setZIndex(2);
						break;
					case 4:
						if (self.nrThumbsToDisplay >= 4)
						{
							newX = 1575 * sgn;
							newY = -20;
							newZ = -1100;
							
							newAngleX = 50;
							newAngleY = 20 * sgn;
							newAngleZ = -28 * sgn;
						}
						else
						{
							newX = lastX;
							newY = lastY;
							newZ = lastZ;
							
							newAngleX = lastAngleX;
							newAngleY = lastAngleY;
							newAngleZ = lastAngleZ;
						}
						
						if (FWDR3DCarUtils.isIEAndMoreThen9)
							thumb.setZIndex(1);
						break;
					default:
						newX = lastX;
						newY = lastY;
						newZ = lastZ;
						
						newAngleX = lastAngleX;
						newAngleY = lastAngleY;
						newAngleZ = lastAngleZ;
						
						if (FWDR3DCarUtils.isIEAndMoreThen9)
							thumb.setZIndex(0);
				}
				
				newX += self.data.thumbSpaceOffset3D * sgn * -newZ/300;
				
				newX *= self.sizeRatio;
				newY *= self.sizeRatio;
				newZ *= self.sizeRatio;
				
				var ratio = self.thumbHeight / self.thumbWidth;
				
				if (ratio > 0.7)
				{
					newX *= Math.min(1/ratio, 0.8);
					newY *= Math.max(ratio, 1.1) * 1.5;
				}
				
				newX = Math.floor(newX) - Math.floor(self.thumbWidth/2);
				newY = Math.floor(newY) - Math.floor(self.thumbHeight/2);
				
				thumb.setGradient(sgn);
				
				delay = Math.min(Math.abs(i - self.curId), self.nrThumbsToDisplay) * 200;
				
				FWDR3DCarModTweenMax.to(thumb, .8, {x:Math.floor(newX), y:Math.floor(newY), z:Math.floor(newZ), angleX:newAngleX, angleY:newAngleY, angleZ:newAngleZ, delay:delay/1000, ease:Expo.easeOut});
				self.thumbsHolderDO.addChild(thumb);
			}
			
			self.setIntroFinishedId = setTimeout(self.setIntroFinished, delay + 800);
			self.showControlsId = setTimeout(self.showControls, delay);
		};
		
		this.setupIntro2D = function()
		{
			var newX;
			var newScale;
			var delay;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				
				newX = 0;

				newScale = 1;
				
				var sgn = 0;
				
				if (i < self.curId)
				{
					sgn = -1;
				}
				else if (i > self.curId)
				{
					sgn = 1;
				}
				
				var lastX;
				var lastScale;
				
				switch (self.nrThumbsToDisplay)
				{
					case 1:
						lastX = 100 * sgn;
						lastScale = .8;
						break;
					case 2:
						lastX = 140 * sgn;
						lastScale = .7;
						break;
					case 3:
						lastX = 200 * sgn;
						lastScale = .6;
						break;
					default:
						lastX = 250 * sgn;
						lastScale = .5;
				}
				
				switch (Math.abs(i - self.curId))
				{
					case 0:
						thumb.setZIndex(5);
						break;
					case 1:
						newX = 150 * sgn;
						newScale = .9;
						
						thumb.setZIndex(4);
						break;
					case 2:
						if (self.nrThumbsToDisplay >= 2)
						{
							newX = 240 * sgn;
							newScale = .8;
						}
						else
						{
							newX = lastX;
							newScale = lastScale;
						}
						
						thumb.setZIndex(3);
						break;
					case 3:
						if (self.nrThumbsToDisplay >= 3)
						{
							newX = 300 * sgn;
							newScale = .7;
						}
						else
						{
							newX = lastX;
							newScale = lastScale;
						}
						
						thumb.setZIndex(2);
						break;
					case 4:
						if (self.nrThumbsToDisplay >= 4)
						{
							newX = 350 * sgn;
							newScale = .6;
						}
						else
						{
							newX = lastX;
							newScale = lastScale;
						}
						
						thumb.setZIndex(1);
						break;
					default:
						newX = lastX;
						newScale = lastScale;
						
						thumb.setZIndex(0);
				}
				
				newX += self.data.thumbSpaceOffset2D * sgn;
				
				if (Math.abs(i - self.curId) == 1)
				{
					newX -= self.data.thumbSpaceOffset2D/4 * sgn;
				}
				
				newX *= self.sizeRatio;
				
				var ratio = self.thumbHeight / self.thumbWidth;
				
				if (ratio > 0.7)
				{
					newX *= Math.min(1/ratio, 0.8);
				}
				
				newX -= self.thumbWidth/2;
				
				thumb.newX = Math.floor(newX);

				thumb.setGradient(sgn);
				
				delay = Math.min(Math.abs(i - self.curId), self.nrThumbsToDisplay) * 200;
				
				thumb.showThumbIntro2D(newScale, delay/1000);
				
				self.thumbsHolderDO.addChild(thumb);
			}
			
			self.setIntroFinishedId = setTimeout(self.setIntroFinished, delay + 800);
			self.showControlsId = setTimeout(self.showControls, delay);
		};
		
		this.setIntroFinished = function()
		{
			self.introFinished = true;
			self.allowToSwitchCat = true;
			self.disableThumbClick = false;
			
			self.dispatchEvent(FWDR3DCarThumbsManager.THUMBS_INTRO_FINISH);
			
			if (self.isMobile)
			{
				self.setupMobileDrag();
			}
			
			if (FWDR3DCarUtils.isIEAndMoreThen9 || !FWDR3DCarUtils.hasTransform3d || self.data.showDisplay2DAlways)
			{
				self.zSortingId = setInterval(self.sortZ, 16);
			}
			
			if (self.data.autoplay)
			{
				if (self.slideshowButtonDO)
				{
					self.slideshowButtonDO.onClick();
					self.slideshowButtonDO.onMouseOut();
				}
			}
		};
		
		this.gotoThumb = function()
		{
			if (!self.introFinished)
				return;

			if (self.showScrollbar && !self.scrollbarDO.isPressed)
			{
				self.scrollbarDO.gotoItem(self.curId, true);
			}

			if (self.isPlaying)
			{
				clearTimeout(self.slideshowTimeoutId);
				self.slideshowTimeoutId = setTimeout(self.startTimeAgain, self.data.transitionDelay);
				
				if (self.slideshowButtonDO.isCounting)
				{
					self.slideshowButtonDO.resetCounter();
				}
			}
			
			if (self.showText)
			{
				if (self.isTextSet)
				{
					self.isTextSet = false;
					
					if (self.isMobile)
					{
						self.removeThumbText();
					}
					else
					{
						 self.thumbsAr[self.prevCurId].removeText();
					}
					
					clearTimeout(self.textTimeoutId);
					self.textTimeoutId = setTimeout(self.setThumbText, 800);
				}
				else
				{
					clearTimeout(self.textTimeoutId);
					self.textTimeoutId = setTimeout(self.setThumbText, 800);
				}
			}
			
			self.prevCurId = self.curId;

			if (FWDR3DCarUtils.hasTransform3d && !self.data.showDisplay2DAlways)
			{	
				self.gotoThumb3D();
			}
			else
			{
				self.gotoThumb2D();
			}
			
			self.dispatchEvent(FWDR3DCarThumbsManager.THUMB_CHANGE, {id:self.curId});
		};
		
		this.setThumbText = function()
		{
			self.isTextSet = true;
			
			if (self.isMobile)
			{
				self.addThumbText();
			}
			else
			{
				self.thumbsAr[self.curId].addText(self.textHolderDO, self.textGradientDO, self.textDO);
			}
		};
		
		this.gotoThumb3D = function()
		{
			var newX;
			var newY;
			var newZ;
			
			var newAngleX;
			var newAngleY;
			var newAngleZ;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				
				newX = 0;
				newY = 0;
				newZ = 0;
				
				newAngleX = 0;
				newAngleY = 0;
				newAngleZ = 0;
				
				var sgn = 0;
				
				if (i < self.curId)
				{
					sgn = -1;
				}
				else if (i > self.curId)
				{
					sgn = 1;
				}
				
				var lastX;
				var lastY;
				var lastZ;
				var lastAngleX;
				var lastAngleY;
				var lastAngleZ;
				
				switch (self.nrThumbsToDisplay)
				{
					case 1:
						lastX = 250 * sgn;
						lastY = -5;
						lastZ = -220;
						
						lastAngleX = 15;
						lastAngleY = 25 * sgn;
						lastAngleZ = -4 * sgn;
						break;
					case 2:
						lastX = 630 * sgn;
						lastY = 0;
						lastZ = -500;
						
						lastAngleX = 25;
						lastAngleY = 28 * sgn;
						lastAngleZ = -13 * sgn;
						break;
					case 3:
						lastX = 1130 * sgn;
						lastY = 0;
						lastZ = -900;
						
						lastAngleX = 32;
						lastAngleY = 28 * sgn;
						lastAngleZ = -20 * sgn;
						break;
					default:
						lastX = 1475 * sgn;
						lastY = -20;
						lastZ = -1200;
						
						lastAngleX = 50;
						lastAngleY = 20 * sgn;
						lastAngleZ = -28 * sgn;
				}
				
				switch (Math.abs(i - self.curId))
				{
					case 0:
						break;
					case 1:
						newX = 350 * sgn;
						newY = -5;
						newZ = -126 - Math.floor(Math.max(self.thumbHeight - 266, 0) / 2.5);
						
						newAngleX = 15;
						newAngleY = 25 * sgn;
						newAngleZ = -4 * sgn;
						break;
					case 2:
						if (self.nrThumbsToDisplay >= 2)
						{
							newX = 730 * sgn;
							newZ = -400;
							
							newAngleX = 25;
							newAngleY = 28 * sgn;
							newAngleZ = -13 * sgn;
						}
						else
						{
							newX = lastX;
							newY = lastY;
							newZ = lastZ;
							
							newAngleX = lastAngleX;
							newAngleY = lastAngleY;
							newAngleZ = lastAngleZ;
						}
						break;
					case 3:
						if (self.nrThumbsToDisplay >= 3)
						{
							newX = 1230 * sgn;
							newZ = -800;
							
							newAngleX = 32;
							newAngleY = 28 * sgn;
							newAngleZ = -20 * sgn;
						}
						else
						{
							newX = lastX;
							newY = lastY;
							newZ = lastZ;
							
							newAngleX = lastAngleX;
							newAngleY = lastAngleY;
							newAngleZ = lastAngleZ;
						}
						break;
					case 4:
						if (self.nrThumbsToDisplay >= 4)
						{
							newX = 1575 * sgn;
							newY = -20;
							newZ = -1100;
							
							newAngleX = 50;
							newAngleY = 20 * sgn;
							newAngleZ = -28 * sgn;
						}
						else
						{
							newX = lastX;
							newY = lastY;
							newZ = lastZ;
							
							newAngleX = lastAngleX;
							newAngleY = lastAngleY;
							newAngleZ = lastAngleZ;
						}
						break;
					default:
						newX = lastX;
						newY = lastY;
						newZ = lastZ;
						
						newAngleX = lastAngleX;
						newAngleY = lastAngleY;
						newAngleZ = lastAngleZ;
				}
				
				newX += self.data.thumbSpaceOffset3D * sgn * -newZ/300;
				
				newX *= self.sizeRatio;
				newY *= self.sizeRatio;
				newZ *= self.sizeRatio;
				
				var ratio = self.thumbHeight / self.thumbWidth;
				
				if (ratio > 0.7)
				{
					newX *= Math.min(1/ratio, 0.8);
					newY *= Math.max(ratio, 1.1) * 1.5;
				}
				
				newX = Math.floor(newX) - Math.floor(self.thumbWidth/2);
				newY = Math.floor(newY) - Math.floor(self.thumbHeight/2);
				
				FWDR3DCarModTweenMax.killTweensOf(thumb);
				
				if ((thumb.getX() + Math.floor(self.thumbWidth/2)) * (newX + Math.floor(self.thumbWidth/2)) < 0)
				{
					FWDR3DCarModTweenMax.to(thumb, .8, {bezier:{values:[{x:-Math.floor(self.thumbWidth/2), y:-Math.floor(self.thumbHeight/2), z:0, angleX:0, angleY:0, angleZ:0},
					                                        {x:Math.floor(newX), y:Math.floor(newY), z:Math.floor(newZ), angleX:newAngleX, angleY:newAngleY, angleZ:newAngleZ}]}, ease:Quart.easeOut});
					thumb.setGradient(sgn);
				}
				else
				{
					if ((Math.abs(i - self.curId) < self.nrThumbsToDisplay) || (thumb.getX() != Math.floor(newX)))
					{
						FWDR3DCarModTweenMax.to(thumb, .8, {x:Math.floor(newX), y:Math.floor(newY), z:Math.floor(newZ), angleX:newAngleX, angleY:newAngleY, angleZ:newAngleZ, ease:Quart.easeOut});
						thumb.setGradient(sgn);
					}
				}	
			}
		};
		
		this.gotoThumb2D = function()
		{
			var newX;
			var newScale;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				
				newX = 0;
				newY = 0;

				newScale = 1;
				
				var sgn = 0;
				
				if (i < self.curId)
				{
					sgn = -1;
				}
				else if (i > self.curId)
				{
					sgn = 1;
				}
				
				var lastX;
				var lastScale;
				
				switch (self.nrThumbsToDisplay)
				{
					case 1:
						lastX = 100 * sgn;
						lastScale = .8;
						break;
					case 2:
						lastX = 140 * sgn;
						lastScale = .7;
						break;
					case 3:
						lastX = 200 * sgn;
						lastScale = .6;
						break;
					default:
						lastX = 250 * sgn;
						lastScale = .5;
				}
				
				switch (Math.abs(i - self.curId))
				{
					case 0:
						break;
					case 1:
						newX = 150 * sgn;
						newScale = .9;
						break;
					case 2:
						if (self.nrThumbsToDisplay >= 2)
						{
							newX = 240 * sgn;
							newScale = .8;
						}
						else
						{
							newX = lastX;
							newScale = lastScale;
						}
						break;
					case 3:
						if (self.nrThumbsToDisplay >= 3)
						{
							newX = 300 * sgn;
							newScale = .7;
						}
						else
						{
							newX = lastX;
							newScale = lastScale;
						}
						break;
					case 4:
						if (self.nrThumbsToDisplay >= 4)
						{
							newX = 350 * sgn;
							newScale = .6;
						}
						else
						{
							newX = lastX;
							newScale = lastScale;
						}
						break;
					default:
						newX = lastX;
						newScale = lastScale;
				}
				
				newX += self.data.thumbSpaceOffset2D * sgn;
				
				if (Math.abs(i - self.curId) == 1)
				{
					newX -= self.data.thumbSpaceOffset2D/4 * sgn;
				}
				
				newX *= self.sizeRatio;
				
				var ratio = self.thumbHeight / self.thumbWidth;
				
				if (ratio > 0.7)
				{
					newX *= Math.min(1/ratio, 0.8);
				}
				
				newX -= self.thumbWidth/2;
	
				if ((Math.abs(i - self.curId) < self.nrThumbsToDisplay) || (thumb.getX() != Math.floor(newX)))
				{
					thumb.newX = Math.floor(newX);
				
					thumb.setScale(newScale);
					thumb.setGradient(sgn);
				}
			}
		};
		
		this.sortZ = function()
		{
			var minX = 10000;
			var centerId;
			var zIndex;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				
				var tx = thumb.getX() + self.thumbWidth/2;
				
				if (Math.abs(tx) < minX)
				{
					minX = Math.abs(tx);
					centerId = i;
				}
			}
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				thumb = self.thumbsAr[i];
				
				switch (Math.abs(i - centerId))
				{
					case 0:
						zIndex = 5;
						break;
					case 1:
						zIndex = 4;
						break;
					case 2:
						zIndex = 3;
						break;
					case 3:
						zIndex = 2;
						break;
					case 4:
						zIndex = 1;
						break;
					default:
						zIndex = 0;
				}
				
				if (zIndex != thumb.getZIndex())
				{
					thumb.setZIndex(zIndex);
				}
			}
		};
		
		this.setupControls = function()
		{
			self.controlsDO = new FWDR3DCarDisplayObject3D("div");
			self.addChild(self.controlsDO);
			
			self.controlsDO.setZ(200000);
			
			self.controlsWidth = self.data.prevButtonNImg.width;
			
			if (self.showScrollbar)
			{
				self.setupScrollbar();
			}
			
			if (self.showPrevButton)
			{
				self.setupPrevButton();
			}
			
			if (self.showNextButton)
			{
				self.setupNextButton();
			}
			
			if (self.showSlideshowButton)
			{
				self.setupSlideshowButton();
			}
			
			if (self.data.enableMouseWheelScroll)
			{
				self.addMouseWheelSupport();
			}
			
			if (self.data.addKeyboardSupport)
			{
				self.addKeyboardSupport();
			}

			if (self.showScrollbar)
			{
				self.controlsWidth -= self.scrollbarDO.getWidth();
				self.scrollbarDO.scrollbarMaxWidth -=  self.controlsWidth;
				self.scrollbarDO.resize2();
				self.scrollbarDO.resize(self.stageWidth, self.controlsWidth);
				
				var newX = self.scrollbarDO.getX() + self.scrollbarDO.getWidth();

				if (self.showNextButton)
				{
					self.nextButtonDO.setX(newX);
					
					newX += self.nextButtonDO.getWidth();
				}
				
				if (self.showSlideshowButton)
				{
					self.slideshowButtonDO.setX(newX);
				}
			}
			
			if (self.showScrollbar)
			{
				self.controlsDO.setX(Math.floor((self.stageWidth - (self.controlsWidth + self.scrollbarDO.getWidth()))/2));
				self.controlsDO.setWidth(self.controlsWidth + self.scrollbarDO.getWidth());
			}
			else
			{
				self.controlsDO.setX(Math.floor((self.stageWidth - self.controlsWidth)/2));
				self.controlsDO.setWidth(self.controlsWidth);
			}

			self.controlsDO.setY(self.stageHeight);
			self.controlsDO.setHeight(self.data.prevButtonNImg.height);
		};
		
		this.showControls = function()
		{
			FWDR3DCarModTweenMax.to(self.controlsDO, .8, {y:self.stageHeight - self.controlsHeight, ease : Expo.easeOut});
		};
		
		this.positionControls = function()
		{
			if (self.showScrollbar)
			{
				self.scrollbarDO.resize(self.stageWidth, self.controlsWidth);
				
				var newX = self.scrollbarDO.getX() + self.scrollbarDO.getWidth();

				if (self.showNextButton)
				{
					self.nextButtonDO.setX(newX);
					
					newX += self.nextButtonDO.getWidth();
				}
				
				if (self.showSlideshowButton)
				{
					self.slideshowButtonDO.setX(newX);
				}
			}

			if (self.showScrollbar)
			{
				self.controlsDO.setX(Math.floor((self.stageWidth - (self.controlsWidth + self.scrollbarDO.getWidth()))/2));
				self.controlsDO.setWidth(self.controlsWidth + self.scrollbarDO.getWidth());
			}
			else
			{
				self.controlsDO.setX(Math.floor((self.stageWidth - self.controlsWidth)/2));
				self.controlsDO.setWidth(self.controlsWidth);
			}
			
			self.controlsDO.setY(self.stageHeight - self.controlsHeight);
		};
		
		this.setupPrevButton = function()
		{
			FWDR3DCarSimpleButton.setPrototype();
			
			self.prevButtonDO = new FWDR3DCarSimpleButton(self.data.prevButtonNImg, self.data.prevButtonSImg);
			self.prevButtonDO.addListener(FWDR3DCarSimpleButton.CLICK, self.prevButtonOnClickHandler);
			self.controlsDO.addChild(self.prevButtonDO);
		};
		
		this.prevButtonOnClickHandler = function()
		{
			if (self.curId > 0)
			{
				self.curId--;
				self.gotoThumb();
			}
		};
		
		this.setupNextButton = function()
		{
			FWDR3DCarSimpleButton.setPrototype();
			
			self.nextButtonDO = new FWDR3DCarSimpleButton(self.data.nextButtonNImg, self.data.nextButtonSImg);
			self.nextButtonDO.addListener(FWDR3DCarSimpleButton.CLICK, self.nextButtonOnClickHandler);
			self.controlsDO.addChild(self.nextButtonDO);
			
			self.nextButtonDO.setX(self.controlsWidth);
			self.controlsWidth += self.nextButtonDO.getWidth();
		};
		
		this.nextButtonOnClickHandler = function()
		{
			if (self.curId < self.totalThumbs-1)
			{
				self.curId++;
				self.gotoThumb();
			}
		};
		
		this.setupSlideshowButton = function()
		{
			FWDR3DCarSlideshowButton.setPrototype();
			
			self.slideshowButtonDO = new FWDR3DCarSlideshowButton(self.data);
			self.slideshowButtonDO.addListener(FWDR3DCarSlideshowButton.PLAY_CLICK, self.onSlideshowButtonPlayClickHandler);
			self.slideshowButtonDO.addListener(FWDR3DCarSlideshowButton.PAUSE_CLICK, self.onSlideshowButtonPauseClickHandler);
			self.slideshowButtonDO.addListener(FWDR3DCarSlideshowButton.TIME, self.onSlideshowButtonTime);
			self.controlsDO.addChild(self.slideshowButtonDO);
			
			self.slideshowButtonDO.setX(self.controlsWidth);
			self.controlsWidth += self.slideshowButtonDO.getWidth();
		};
		
		this.onSlideshowButtonPlayClickHandler = function()
		{
			self.isPlaying = true;
		};
		
		this.onSlideshowButtonPauseClickHandler = function()
		{
			self.isPlaying = false;
			clearTimeout(self.slideshowTimeoutId);
		};
		
		this.startSlideshow = function()
		{
			if (!self.isPlaying)
			{
				self.isPlaying = true;
				
				self.slideshowButtonDO.start();
				self.slideshowButtonDO.onMouseOut();
			}
		};
		
		this.stopSlideshow = function()
		{
			if (self.isPlaying)
			{
				self.isPlaying = false;
				clearTimeout(self.slideshowTimeoutId);
				
				self.slideshowButtonDO.stop();
				self.slideshowButtonDO.onMouseOut();
			}
		};
		
		this.onSlideshowButtonTime = function()
		{
			if (self.curId == self.totalThumbs-1)
			{
				self.curId = 0;
			}
			else
			{
				self.curId++;
			}
			
			self.gotoThumb();
		};
		
		this.startTimeAgain = function()
		{
			self.slideshowButtonDO.start();
		};

		this.setupScrollbar = function()
		{
			FWDR3DCarScrollbar.setPrototype();
			
			self.scrollbarDO = new FWDR3DCarScrollbar(self.data, self.totalThumbs, self.curId);
			self.scrollbarDO.addListener(FWDR3DCarScrollbar.MOVE, self.onScrollbarMove);
			self.controlsDO.addChild(self.scrollbarDO);
			
			self.scrollbarDO.setX(self.controlsWidth);
			self.controlsWidth += self.scrollbarDO.getWidth();
		};
		
		this.onScrollbarMove = function(e)
		{
			self.curId = e.id;
			self.gotoThumb();
		};
		
		this.addMouseWheelSupport = function()
		{
			if (window.addEventListener)
			{
				self.parent.mainDO.screen.addEventListener("mousewheel", self.mouseWheelHandler);
				self.parent.mainDO.screen.addEventListener('DOMMouseScroll', self.mouseWheelHandler);
			}
			else if (document.attachEvent)
			{
				self.parent.mainDO.screen.attachEvent("onmousewheel", self.mouseWheelHandler);
			}
		};
		
		this.mouseWheelHandler = function(e)
		{
			if (!self.introFinished || !self.allowToSwitchCat)
				return;
				
			if (self.showScrollbar && self.scrollbarDO.isPressed)
				return;
			
			var dir = e.detail || e.wheelDelta;	
			
			if (e.wheelDelta)
				dir *= -1;
			
			if (dir > 0)
			{
				if (self.curId < self.totalThumbs-1)
				{
					self.curId++;
					self.gotoThumb();
				}
			}
			else if (dir < 0)
			{
				if (self.curId > 0)
				{
					self.curId--;
					self.gotoThumb();
				}
			}
			
			if (e.preventDefault)
			{
				e.preventDefault();
			}
			else
			{
				return false;
			}
		};
		
		//##########################################//
		/* setup mobile drag */
		//##########################################//
		this.setupMobileDrag = function()
		{
			if (self.hasPointerEvent)
			{
				self.parent.mainDO.screen.addEventListener("MSPointerDown", self.mobileDragStartHandler);
			}
			else
			{
				self.parent.mainDO.screen.addEventListener("touchstart", self.mobileDragStartTest);
			}
		};
		
		this.mobileDragStartTest = function(e)
		{
			var viewportMouseCoordinates = FWDR3DCarUtils.getViewportMouseCoordinates(e);	
			
			if (viewportMouseCoordinates.screenY > self.controlsDO.getY())
				return;
			
			self.lastPressedX = viewportMouseCoordinates.screenX;
			self.lastPressedY = viewportMouseCoordinates.screenY;
			
			self.dragCurId = self.curId;
			
			window.addEventListener("touchmove", self.mobileDragMoveTest);
			window.addEventListener("touchend", self.mobileDragEndTest);
		};
		
		this.mobileDragMoveTest = function(e)
		{
			if (e.touches.length != 1) return;
			
			self.disableThumbClick = true;
			
			var viewportMouseCoordinates = FWDR3DCarUtils.getViewportMouseCoordinates(e);	
			
			self.mouseX = viewportMouseCoordinates.screenX;
			self.mouseY = viewportMouseCoordinates.screenY;
			
			var angle = Math.atan2(self.mouseY - self.lastPressedY, self.mouseX - self.lastPressedX);
			var posAngle = Math.abs(angle) * 180 / Math.PI;
			
			if ((posAngle > 120) || (posAngle < 60))
			{
				if(e.preventDefault) e.preventDefault();
				
				self.curId = self.dragCurId + Math.floor(-(self.mouseX - self.lastPressedX) / 100);
				
				if (self.curId < 0)
				{
					self.curId = 0;
				}
				else if (self.curId > self.totalThumbs-1)
				{
					self.curId = self.totalThumbs-1;
				}
				
				self.gotoThumb();
			}
			else
			{
				window.removeEventListener("touchmove", self.mobileDragMoveTest);
			}
		};
		
		this.mobileDragEndTest = function(e)
		{
			self.disableThumbClick = false;
			
			window.removeEventListener("touchmove", self.mobileDragMoveTest);
			window.removeEventListener("touchend", self.mobileDragEndTest);
		};
		
		this.mobileDragStartHandler = function(e)
		{
			var viewportMouseCoordinates = FWDR3DCarUtils.getViewportMouseCoordinates(e);		
			
			if (viewportMouseCoordinates.screenY > self.controlsDO.getY())
				return;

			self.lastPressedX = viewportMouseCoordinates.screenX;	
			
			self.dragCurId = self.curId;

			window.addEventListener("MSPointerUp", self.mobileDragEndHandler, false);
			window.addEventListener("MSPointerMove", self.mobileDragMoveHandler);
		};
		
		this.mobileDragMoveHandler = function(e)
		{
			if(e.preventDefault) e.preventDefault();
			
			self.disableThumbClick = true;
			
			var viewportMouseCoordinates = FWDR3DCarUtils.getViewportMouseCoordinates(e);	
			
			self.mouseX = viewportMouseCoordinates.screenX;;
			
			self.curId = self.dragCurId + Math.floor(-(self.mouseX - self.lastPressedX) / 100);
			
			if (self.curId < 0)
			{
				self.curId = 0;
			}
			else if (self.curId > self.totalThumbs-1)
			{
				self.curId = self.totalThumbs-1;
			}
			
			self.gotoThumb();
		};

		this.mobileDragEndHandler = function(e)
		{
			self.disableThumbClick = false;
			
			window.removeEventListener("MSPointerUp", self.mobileDragEndHandler);
			window.removeEventListener("MSPointerMove", self.mobileDragMoveHandler);
		};
		
		//####################################//
		/* add keyboard support */
		//####################################//
		this.addKeyboardSupport = function()
		{
			if(document.addEventListener){
				document.addEventListener("keydown",  this.onKeyDownHandler);	
				document.addEventListener("keyup",  this.onKeyUpHandler);	
			}else{
				document.attachEvent("onkeydown",  this.onKeyDownHandler);	
				document.attachEvent("onkeyup",  this.onKeyUpHandler);	
			}
		};
		
		this.onKeyDownHandler = function(e)
		{
			if (!self.introFinished || !self.allowToSwitchCat)
				return;
				
			if (self.showScrollbar && self.scrollbarDO.isPressed)
				return;
				
			if (parent.lightboxDO && parent.lightboxDO.isShowed_bl)
				return;
				
			if(document.removeEventListener){
				document.removeEventListener("keydown",  self.onKeyDownHandler);
			}else{
				document.detachEvent("onkeydown",  self.onKeyDownHandler);
			}
				
			if (e.keyCode == 39)
			{	
				if (self.curId < self.totalThumbs-1)
				{
					self.curId++;
					self.gotoThumb();
				}
				
				if(e.preventDefault){
					e.preventDefault();
				}else{
					return false;
				}
			}
			else if (e.keyCode == 37)
			{
				if (self.curId > 0)
				{
					self.curId--;
					self.gotoThumb();
				}
				
				if(e.preventDefault){
					e.preventDefault();
				}else{
					return false;
				}
			}
		};
		
		this.onKeyUpHandler = function(e)
		{
			if(document.addEventListener){
				document.addEventListener("keydown",  self.onKeyDownHandler);	
			}else{
				document.attachEvent("onkeydown",  self.onKeyDownHandler);	
			}
		};
		

		this.update = function(e)
		{
			self.showRefl = e.showRefl;
			self.reflDist = e.reflDist;
			
			for (var i=0; i<self.totalThumbs; i++)
			{
				self.thumbsAr[i].update();
			}
		};
		
		/* destroy */
		this.destroy = function()
		{
			clearTimeout(self.loadWithDelayIdLeft);
			clearTimeout(self.loadWithDelayIdRight);
			clearTimeout(self.slideshowTimeoutId);
			clearTimeout(self.textTimeoutId);
			clearInterval(self.zSortingId);
			clearTimeout(self.hideThumbsFinishedId);
			clearTimeout(self.loadHtmlContentsId);
			clearTimeout(self.loadImagesId);
			clearTimeout(self.setTextHeightId);
			clearTimeout(self.setIntroFinishedId);
			clearTimeout(self.showControlsId);
			
			if (!self.isMobile)
			{
				if (self.screen.addEventListener)
				{
					window.removeEventListener("mousemove", self.onThumbMove);
				}
				else
				{
					document.detachEvent("onmousemove", self.onThumbMove);
				}
			}
			
			if (self.hasPointerEvent)
			{
				window.removeEventListener("MSPointerMove", self.onThumbMove);
			}
			
			if (self.hasPointerEvent)
			{
				self.parent.mainDO.screen.removeEventListener("MSPointerDown", self.mobileDragStartHandler);
				window.removeEventListener("MSPointerUp", self.mobileDragEndHandler);
				window.removeEventListener("MSPointerMove", self.mobileDragMoveHandler);
			}
			else
			{
				if (window.addEventListener)
				{
					self.parent.mainDO.screen.removeEventListener("touchstart", self.mobileDragStartTest);
					window.removeEventListener("touchmove", self.mobileDragMoveTest);
					window.removeEventListener("touchend", self.mobileDragEndTest);
				}
			}
			
			if (window.addEventListener)
			{
				self.parent.mainDO.screen.removeEventListener("mousewheel", self.mouseWheelHandler);
				self.parent.mainDO.screen.removeEventListener('DOMMouseScroll', self.mouseWheelHandler);
			}
			else if (document.attachEvent)
			{
				self.parent.mainDO.screen.detachEvent("onmousewheel", self.mouseWheelHandler);
			}
			
			if (self.addKeyboardSupport)
			{
				if(document.removeEventListener){
					document.removeEventListener("keydown",  this.onKeyDownHandler);	
					document.removeEventListener("keyup",  this.onKeyUpHandler);	
				}else if(document.attachEvent){
					document.detachEvent("onkeydown",  this.onKeyDownHandler);	
					document.detachEvent("onkeyup",  this.onKeyUpHandler);	
				}
			}
			
			if (self.image)
			{
				self.image.onload = null;
				self.image.onerror = null;
				self.image.src = "";
			}

			if (self.imageLeft)
			{
				self.imageLeft.onload = null;
				self.imageLeft.onerror = null;
				self.imageLeft.src = "";
			}
			
			if (self.imageRight)
			{
				self.imageRight.onload = null;
				self.imageRight.onerror = null;
				self.imageRight.src = "";
			}
			
			self.image = null;
			self.imageLeft = null;
			self.imageRight = null;

			/* destroy thumbs */
			for (var i=0; i<self.totalThumbs; i++)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.thumbsAr[i]);
				self.thumbsAr[i].destroy();
				self.thumbsAr[i] = null;
			};

			self.thumbsAr = null;
			
			if (self.prevButtonDO)
			{
				self.prevButtonDO.destroy();
				self.prevButtonDO = null;
			}
			
			if (self.nextButtonDO)
			{
				self.nextButtonDO.destroy();
				self.nextButtonDO = null;
			}
			
			if (self.scrollbarDO)
			{
				self.scrollbarDO.destroy();
				self.scrollbarDO = null;
			}
			
			if (self.slideshowButtonDO)
			{
				self.slideshowButtonDO.destroy();
				self.slideshowButtonDO = null;
			}	
			
			if (self.textGradientDO && self.textGradientDO.screen)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.textGradientDO);
				self.textGradientDO.destroy();
				self.textGradientDO = null;
			}
			
			if (self.textDO && self.textDO.screen)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.textDO);
				self.textDO.destroy();
				self.textDO = null;
			}
			
			if (self.textHolderDO && self.textHolderDO.screen)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.textHolderDO);
				self.textHolderDO.destroy();
				self.textHolderDO = null;
			}
			
			if (self.thumbOverDO)
			{
				self.thumbOverDO.destroy();
				self.thumbOverDO = null;
			}

			if (self.thumbsHolderDO)
			{
				self.thumbsHolderDO.destroy();
				self.thumbsHolderDO = null;
			}
			
			if (self.controlsDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.controlsDO);
				self.controlsDO.destroy();
				self.controlsDO = null;
			}
			
			self.screen.innerHTML = "";
			self = null;
			prototype.destroy();
			prototype = null;
			FWDR3DCarThumbsManager.prototype = null;
		};
		
		this.init();
	};

	/* set prototype */
	FWDR3DCarThumbsManager.setPrototype = function()
	{
		FWDR3DCarThumbsManager.prototype = new FWDR3DCarDisplayObject3D("div", "relative", "visible");
	};
	
	FWDR3DCarThumbsManager.THUMB_CLICK = "onThumbClick";
	FWDR3DCarThumbsManager.LOAD_ERROR = "onLoadError";
	FWDR3DCarThumbsManager.THUMBS_INTRO_FINISH = "onThumbsIntroFinish";
	FWDR3DCarThumbsManager.THUMB_CHANGE = "onThumbChange";

	window.FWDR3DCarThumbsManager = FWDR3DCarThumbsManager;

}(window));
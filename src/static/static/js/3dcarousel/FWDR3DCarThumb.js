/* thumb */
(function(window)
{
	var FWDR3DCarThumb = function(id, data, parent)
	{
		var self = this;
		var prototype = FWDR3DCarThumb.prototype;

		this.id = id;
		this.borderSize = data.thumbBorderSize;
		this.backgroundColor = data.thumbBackgroundColor;
		this.borderColor1 = data.thumbBorderColor1;
		this.borderColor2 = data.thumbBorderColor2;

		this.mainDO = null;
		this.borderDO = null;
		this.bgDO = null;
		this.imageHolderDO = null;
		this.imageDO = null;
		this.htmlContentDO = null;
		this.reflCanvasDO = null;
		
		this.gradientDO = null;
		this.gradientLeftDO = null;
		this.gradientRightDO = null;
		
		this.textHolderDO = null;
		this.textGradientDO = null;
		this.textDO = null;
		
		this.thumbWidth = data.thumbWidth;
		this.thumbHeight = data.thumbHeight;
		
		this.mouseX = 0;
		this.mouseY = 0;
		
		this.pos;
		this.thumbScale = 1;
		
		this.showBoxShadow = data.showBoxShadow;
		
		this.curDataListAr;
		
		this.isOver = false;
		this.hasText = false;
		
		this.isMobile = FWDR3DCarUtils.isMobile;
		this.hasPointerEvent = FWDR3DCarUtils.hasPointerEvent;

		/* init */
		this.init = function()
		{
			self.setupScreen();
		};

		/* setup screen */
		this.setupScreen = function()
		{
			self.mainDO = new FWDR3DCarDisplayObject("div");
			self.addChild(self.mainDO);
			
			self.mainDO.setWidth(self.thumbWidth);
			self.mainDO.setHeight(self.thumbHeight);
			
			self.setWidth(self.thumbWidth);
			self.setHeight(self.thumbHeight);
			
			if (data.showThumbnailsHtmlContent || !data.transparentImages)
			{
				self.borderDO = new FWDR3DCarSimpleDisplayObject("div");
				self.bgDO = new FWDR3DCarSimpleDisplayObject("div");
				
				self.mainDO.addChild(self.borderDO);
				self.mainDO.addChild(self.bgDO);
				
				self.borderDO.setWidth(self.thumbWidth);
				self.borderDO.setHeight(self.thumbHeight);
				
				self.bgDO.setWidth(self.thumbWidth - self.borderSize * 2);
				self.bgDO.setHeight(self.thumbHeight - self.borderSize * 2);
				
				self.bgDO.setX(self.borderSize);
				self.bgDO.setY(self.borderSize);

				self.borderDO.setCSSGradient(self.borderColor1, self.borderColor2);
				
				self.bgDO.setBkColor(self.backgroundColor);
				
				if (FWDR3DCarUtils.isAndroid)
				{
					self.borderDO.setBackfaceVisibility();
					self.bgDO.setBackfaceVisibility();
				}
			}
			
			self.imageHolderDO = new FWDR3DCarDisplayObject("div");
			self.mainDO.addChild(self.imageHolderDO);
			
			self.curDataListAr = parent.curDataListAr;
			
			if (!self.isMobile && (self.curDataListAr[self.id].mediaType != "none"))
			{
				self.mainDO.setButtonMode(true);
			}
			
			if (!self.isMobile && !FWDR3DCarUtils.isIEAndLessThen9 && data.showGradient)
			{
				self.setupGradient();
			}
			
			if (FWDR3DCarUtils.isAndroid)
			{
				self.setBackfaceVisibility();
				self.mainDO.setBackfaceVisibility();
				self.imageHolderDO.setBackfaceVisibility();
			}
			
			if (self.showBoxShadow)
			{
				self.mainDO.screen.style.boxShadow = data.thumbBoxShadowCss;
			}
			
			if (self.isMobile)
			{
				if (self.hasPointerEvent)
				{
					self.mainDO.screen.addEventListener("MSPointerUp", self.onMouseTouchHandler);
				}
				else
				{
					self.mainDO.screen.addEventListener("touchend", self.onMouseTouchHandler);
				}
			}
			else
			{
				if (self.screen.addEventListener)
				{
					self.mainDO.screen.addEventListener("click", self.onMouseClickHandler);
				}
				else
				{
					self.mainDO.screen.attachEvent("onclick", self.onMouseClickHandler);
				}
			}
		};
		
		this.addReflection = function()
		{
			if (!self.imageDO || self.isMobile || FWDR3DCarUtils.isIEAndLessThen9)
				return;
			
			var imgW = self.thumbWidth - self.borderSize * 2;
			var imgH = self.thumbHeight - self.borderSize * 2;
			
			self.reflCanvasDO = new FWDR3DCarSimpleDisplayObject("canvas");
			self.addChild(self.reflCanvasDO);
			
			self.reflCanvasDO.screen.width = self.thumbWidth;
			self.reflCanvasDO.screen.height = parent.reflHeight;
			
			var context = self.reflCanvasDO.screen.getContext("2d");
		   
			context.save();
					
			context.translate(0, self.thumbHeight);
			context.scale(1, -1);
			
			if (data.showThumbnailsHtmlContent || !data.transparentImages)
			{
				context.fillStyle = self.borderColor1;
				context.fillRect(0, 0, self.thumbWidth, self.thumbHeight);
			}
			
			context.drawImage(self.imageDO.screen, self.borderSize, self.borderSize, imgW, imgH);

			context.restore();
			
			context.globalCompositeOperation = "destination-out";
			var gradient = context.createLinearGradient(0, 0, 0, parent.reflHeight);
			
			gradient.addColorStop(1, "rgba(255, 255, 255, 1.0)");
			gradient.addColorStop(0, "rgba(255, 255, 255, " + (1-parent.reflAlpha) + ")");

			context.fillStyle = gradient;
			context.fillRect(0, 0, self.thumbWidth, parent.reflHeight + 2);
			
			self.setWidth(self.thumbWidth);
			self.reflCanvasDO.setY(self.thumbHeight + parent.reflDist);
		};

		this.addImage = function(image)
		{
			self.imageDO = new FWDR3DCarSimpleDisplayObject("img");
			self.imageDO.setScreen(image);
			self.imageHolderDO.addChild(self.imageDO);
			
			self.imageDO.screen.ontouchstart = null;
			
			if (FWDR3DCarUtils.isAndroid)
			{
				self.imageDO.setBackfaceVisibility();
			}
			
			self.imageDO.setWidth(self.thumbWidth - self.borderSize * 2);
			self.imageDO.setHeight(self.thumbHeight - self.borderSize * 2);
			
			self.imageHolderDO.setX(self.borderSize);
			self.imageHolderDO.setY(self.borderSize);
			
			self.imageHolderDO.setWidth(self.thumbWidth - self.borderSize * 2);
			self.imageHolderDO.setHeight(self.thumbHeight - self.borderSize * 2);
			
			if (parent.showRefl)
			{
				self.addReflection();
			}
		};
		
		this.addHtmlContent = function()
		{
			self.htmlContentDO = new FWDR3DCarSimpleDisplayObject("div");
			self.htmlContentDO.setInnerHTML(self.curDataListAr[self.id].htmlContent);
			self.imageHolderDO.addChild(self.htmlContentDO);
			
			if (FWDR3DCarUtils.isAndroid)
			{
				self.htmlContentDO.setBackfaceVisibility();
			}
			
			self.htmlContentDO.setWidth(self.thumbWidth - self.borderSize * 2);
			self.htmlContentDO.setHeight(self.thumbHeight - self.borderSize * 2);
			
			self.imageHolderDO.setX(self.borderSize);
			self.imageHolderDO.setY(self.borderSize);
			
			self.imageHolderDO.setWidth(self.thumbWidth - self.borderSize * 2);
			self.imageHolderDO.setHeight(self.thumbHeight - self.borderSize * 2);
		};
		
		this.setupGradient = function()
		{
			self.gradientDO = new FWDR3DCarDisplayObject("div");
			self.mainDO.addChild(self.gradientDO);
			
			self.gradientDO.setWidth(self.thumbWidth);
			self.gradientDO.setHeight(self.thumbHeight);
			
			self.gradientLeftDO = new FWDR3DCarSimpleDisplayObject("img");
			self.gradientDO.addChild(self.gradientLeftDO);
			
			self.gradientLeftDO.setWidth(self.thumbWidth);
			self.gradientLeftDO.setHeight(self.thumbHeight);
			
			self.gradientLeftDO.screen.src = data.thumbGradientLeftPath;
			
			self.gradientRightDO = new FWDR3DCarSimpleDisplayObject("img");
			self.gradientDO.addChild(self.gradientRightDO);
			
			self.gradientRightDO.setWidth(self.thumbWidth);
			self.gradientRightDO.setHeight(self.thumbHeight);
			
			self.gradientRightDO.screen.src = data.thumbGradientRightPath;
			
			self.gradientLeftDO.setAlpha(0);
			self.gradientRightDO.setAlpha(0);
		};
		
		this.setGradient = function(pos)
		{
			if (self.pos == pos)
				return;

			self.pos = pos;
			
			if (!self.isMobile && !FWDR3DCarUtils.isIEAndLessThen9 && data.showGradient)
			{
				switch (self.pos)
				{
					case 0:
						FWDR3DCarModTweenMax.to(self.gradientLeftDO, .8, {alpha:0});
						FWDR3DCarModTweenMax.to(self.gradientRightDO, .8, {alpha:0, onComplete:self.setGradPos});
						break;
					case 1:
						self.gradientDO.setY(0);
						FWDR3DCarModTweenMax.to(self.gradientLeftDO, .8, {alpha:0});
						FWDR3DCarModTweenMax.to(self.gradientRightDO, .8, {alpha:1});
						break;
					case -1:
						self.gradientDO.setY(0);
						FWDR3DCarModTweenMax.to(self.gradientLeftDO, .8, {alpha:1});
						FWDR3DCarModTweenMax.to(self.gradientRightDO, .8, {alpha:0});
						break;
				}
			}
		};
		
		this.setGradPos = function()
		{
			self.gradientDO.setY(2000);
		};
		
		this.addText = function(textHolderDO, textGradientDO, textDO)
		{
			if (self.curDataListAr[self.id].emptyText)
				return;
			
			self.textHolderDO = textHolderDO;
			self.textGradientDO = textGradientDO;
			self.textDO = textDO;
			
			self.textHolderDO.setX(self.borderSize);
			self.textHolderDO.setY(self.borderSize);
			
			self.mainDO.addChild(self.textHolderDO);
			self.textDO.setInnerHTML(self.curDataListAr[self.id].thumbText);
			
			self.textTitleOffset = self.curDataListAr[self.id].textTitleOffset;
			self.textDescriptionOffsetTop = self.curDataListAr[self.id].textDescriptionOffsetTop;
			self.textDescriptionOffsetBottom = self.curDataListAr[self.id].textDescriptionOffsetBottom;
			
			self.textGradientDO.setY(self.thumbHeight - self.borderSize * 2 - self.textTitleOffset);
			self.textDO.setY(self.thumbHeight - self.borderSize * 2 - self.textTitleOffset + self.textDescriptionOffsetTop);
			
			self.textHolderDO.setAlpha(0);

			self.setTextHeightId = setTimeout(self.setTextHeight, 10);
		};
		
		this.setTextHeight = function()
		{
			if (!self.textHolderDO)
				return;
			
			self.textHeight = self.textDO.getHeight();
			
			FWDR3DCarModTweenMax.to(self.textHolderDO, .8, {alpha:1, ease:Expo.easeOut});
			
			self.hasText = true;
			
			self.checkThumbOver();
		};
		
		this.removeText = function()
		{
			if (self.textHolderDO)
			{
				FWDR3DCarModTweenMax.to(self.textHolderDO, .6, {alpha:0, ease:Expo.easeOut, onComplete:self.removeTextFinish});
			}
		};
		
		this.removeTextFinish = function()
		{
			FWDR3DCarModTweenMax.killTweensOf(self.textHolderDO);
			FWDR3DCarModTweenMax.killTweensOf(self.textGradientDO);
			FWDR3DCarModTweenMax.killTweensOf(self.textDO);
			
			self.mainDO.removeChild(self.textHolderDO);
			self.textHolderDO = null;
			self.textGradientDO = null;
			self.textDO = null;
			
			self.isOver = false;
			self.hasText = false;
		};
		
		this.checkThumbOver = function()
		{
			if (!self.hasText)
				return;

			if ((parent.thumbMouseX >= 0) && (parent.thumbMouseX <= self.thumbWidth) && (parent.thumbMouseY >= 0) && (parent.thumbMouseY <= self.thumbHeight))
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
			if (!self.isOver)
			{
				self.isOver = true;

				FWDR3DCarModTweenMax.to(self.textGradientDO, .8, {y:self.thumbHeight - self.borderSize * 2 - self.textDescriptionOffsetTop - self.textHeight - self.textDescriptionOffsetBottom, ease:Expo.easeOut});
				FWDR3DCarModTweenMax.to(self.textDO, .8, {y:self.thumbHeight - self.borderSize * 2 - self.textHeight - self.textDescriptionOffsetBottom, ease:Expo.easeOut});
			}
		};

		this.onThumbOutHandler = function()
		{
			if (self.isOver)
			{
				self.isOver = false;
				
				FWDR3DCarModTweenMax.to(self.textGradientDO, .8, {y:self.thumbHeight - self.borderSize * 2 - self.textTitleOffset, ease:Expo.easeOut});
				FWDR3DCarModTweenMax.to(self.textDO, .8, {y:self.thumbHeight - self.borderSize * 2 - self.textTitleOffset + self.textDescriptionOffsetTop, ease:Expo.easeOut});
			}
		};
		
		this.showThumb3D = function()
		{
			var imgW = self.thumbWidth - self.borderSize * 2;
			var imgH = self.thumbHeight - self.borderSize * 2;
			
			self.imageHolderDO.setX(parseInt(self.thumbWidth/2));
			self.imageHolderDO.setY(parseInt(self.thumbHeight/2));
			
			self.imageHolderDO.setWidth(0);
			self.imageHolderDO.setHeight(0);
			
			FWDR3DCarModTweenMax.to(self.imageHolderDO, .8, {x:self.borderSize, y:self.borderSize, w:imgW, h:imgH, ease:Expo.easeInOut});
			
			if (data.showThumbnailsHtmlContent)
			{
				self.htmlContentDO.setWidth(imgW);
				self.htmlContentDO.setHeight(imgH);
				
				self.htmlContentDO.setX(-parseInt(imgW/2));
				self.htmlContentDO.setY(-parseInt(imgH/2));
				
				FWDR3DCarModTweenMax.to(self.htmlContentDO, .8, {x:0, y:0, ease:Expo.easeInOut});
			}
			else
			{
				self.imageDO.setWidth(imgW);
				self.imageDO.setHeight(imgH);
				
				self.imageDO.setX(-parseInt(imgW/2));
				self.imageDO.setY(-parseInt(imgH/2));
				
				FWDR3DCarModTweenMax.to(self.imageDO, .8, {x:0, y:0, ease:Expo.easeInOut});
				
				if (self.reflCanvasDO)
				{
					self.reflCanvasDO.setAlpha(0);
					FWDR3DCarModTweenMax.to(self.reflCanvasDO, .8, {alpha:1, ease:Expo.easeInOut});
				}
			}
		};
		
		this.showThumb2D = function()
		{
			if (!FWDR3DCarUtils.hasTransform2d)
			{
				var scaleW = Math.floor(self.thumbWidth * self.thumbScale);
				var scaleH = Math.floor(self.thumbHeight * self.thumbScale);
				var borderScale = Math.floor(self.borderSize * self.thumbScale);
				
				if ((self.borderSize > 0) && (borderScale < 1))
				{
					borderScale = 1;
				}
			
				var imgW = scaleW - borderScale * 2;
				var imgH = scaleH - borderScale * 2;
				
				self.imageHolderDO.setX(parseInt(scaleW/2));
				self.imageHolderDO.setY(parseInt(scaleH/2));
				
				self.imageHolderDO.setWidth(0);
				self.imageHolderDO.setHeight(0);
				
				FWDR3DCarModTweenMax.to(self.imageHolderDO, .8, {x:borderScale, y:borderScale, w:imgW, h:imgH, ease:Expo.easeInOut});
				
				if (data.showThumbnailsHtmlContent)
				{
					if (self.htmlContentDO)
					{
						self.htmlContentDO.setWidth(imgW);
						self.htmlContentDO.setHeight(imgH);
						
						self.htmlContentDO.setX(-parseInt(imgW/2));
						self.htmlContentDO.setY(-parseInt(imgH/2));
						
						FWDR3DCarModTweenMax.to(self.htmlContentDO, .8, {x:0, y:0, ease:Expo.easeInOut});
					}
				}
				else
				{
					if (self.imageDO)
					{
						self.imageDO.setWidth(imgW);
						self.imageDO.setHeight(imgH);
						
						self.imageDO.setX(-parseInt(imgW/2));
						self.imageDO.setY(-parseInt(imgH/2));
						
						FWDR3DCarModTweenMax.to(self.imageDO, .8, {x:0, y:0, ease:Expo.easeInOut});
						
						if (self.reflCanvasDO)
						{
							FWDR3DCarModTweenMax.to(self.reflCanvasDO, .8, {alpha:1, ease:Expo.easeInOut});
						}
					}
				}
			}
			else
			{
				self.setScale2(self.thumbScale);
				
				var imgW = self.thumbWidth - self.borderSize * 2;
				var imgH = self.thumbHeight - self.borderSize * 2;
				
				self.imageHolderDO.setX(parseInt(self.thumbWidth/2));
				self.imageHolderDO.setY(parseInt(self.thumbHeight/2));
				
				self.imageHolderDO.setWidth(0);
				self.imageHolderDO.setHeight(0);
				
				FWDR3DCarModTweenMax.to(self.imageHolderDO, .8, {x:self.borderSize, y:self.borderSize, w:imgW, h:imgH, ease:Expo.easeInOut});
				
				if (data.showThumbnailsHtmlContent)
				{
					if (self.htmlContentDO)
					{
						self.htmlContentDO.setWidth(imgW);
						self.htmlContentDO.setHeight(imgH);
						
						self.htmlContentDO.setX(-parseInt(imgW/2));
						self.htmlContentDO.setY(-parseInt(imgH/2));
						
						FWDR3DCarModTweenMax.to(self.htmlContentDO, .8, {x:0, y:0, ease:Expo.easeInOut});
					}
				}
				else
				{
					if (self.imageDO)
					{
						self.imageDO.setWidth(imgW);
						self.imageDO.setHeight(imgH);
						
						self.imageDO.setX(-parseInt(imgW/2));
						self.imageDO.setY(-parseInt(imgH/2));
						
						FWDR3DCarModTweenMax.to(self.imageDO, .8, {x:0, y:0, ease:Expo.easeInOut});
						
						if (self.reflCanvasDO)
						{
							FWDR3DCarModTweenMax.to(self.reflCanvasDO, .8, {alpha:1, ease:Expo.easeInOut});
						}
					}
				}
			}
		};
		
		this.showThumbIntro2D = function(scale, del)
		{
			self.thumbScale = scale;

			if (!FWDR3DCarUtils.hasTransform2d)
			{
				var scaleW = Math.floor(self.thumbWidth * scale);
				var scaleH = Math.floor(self.thumbHeight * scale);
				var borderScale = Math.floor(self.borderSize * scale);
				
				if ((self.borderSize > 0) && (borderScale < 1))
				{
					borderScale = 1;
				}
				
				var imgW = scaleW - borderScale * 2;
				var imgH = scaleH - borderScale * 2;
				
				self.setWidth(scaleW);
				self.setHeight(scaleH);
				
				self.mainDO.setWidth(scaleW);
				self.mainDO.setHeight(scaleH);
				
				if (self.borderDO)
				{
					self.borderDO.setWidth(scaleW);
					self.borderDO.setHeight(scaleH);
				}
				
				if (self.bgDO)
				{
					self.bgDO.setX(borderScale);
					self.bgDO.setY(borderScale);
					
					self.bgDO.setWidth(imgW);
					self.bgDO.setHeight(imgH);
				}
				
				self.setX(-self.thumbWidth/2);
				self.setY(-self.thumbHeight/2);
				
				FWDR3DCarModTweenMax.to(self, .8, {x:Math.floor(self.newX + (self.thumbWidth - scaleW)/2), y:-Math.floor(scaleH/2), delay:del, ease:Expo.easeOut});
			}
			else
			{
				self.setScale2(self.thumbScale);
				
				self.setX(-self.thumbWidth/2);
				self.setY(-self.thumbHeight/2);

				FWDR3DCarModTweenMax.to(self, .8, {x:self.newX, scale:self.thumbScale, delay:del, ease:Quart.easeOut, onComplete:self.setThumbVisibility});
			}
		};
		
		this.setScale = function(scale)
		{
			self.thumbScale = scale;
			
			self.setVisible(true);
			
			if (!FWDR3DCarUtils.hasTransform2d)
			{
				var scaleW = Math.floor(self.thumbWidth * scale);
				var scaleH = Math.floor(self.thumbHeight * scale);
				var borderScale = Math.floor(self.borderSize * scale);
				
				if ((self.borderSize > 0) && (borderScale < 1))
				{
					borderScale = 1;
				}
				
				if (self.borderDO)
				{
					FWDR3DCarModTweenMax.to(self.borderDO, .8, {w:scaleW, h:scaleH, ease:Quart.easeOut});
				}
				
				if (self.bgDO)
				{
					FWDR3DCarModTweenMax.to(self.bgDO, .8, {x:borderScale, y:borderScale, w:scaleW - borderScale * 2, h:scaleH - borderScale * 2, ease:Quart.easeOut});
				}
				
				FWDR3DCarModTweenMax.to(self.mainDO, .8, {w:scaleW, h:scaleH, ease:Quart.easeOut});
				FWDR3DCarModTweenMax.to(self.imageHolderDO, .8, {x:borderScale, y:borderScale, w:scaleW - borderScale * 2, h:scaleH - borderScale * 2, ease:Quart.easeOut});
				FWDR3DCarModTweenMax.to(self, .8, {x:Math.floor(self.newX + (self.thumbWidth - scaleW)/2), y:-Math.floor(scaleH/2), w:scaleW, h:scaleH, ease:Quart.easeOut});
				
				if (data.showThumbnailsHtmlContent)
				{
					if (self.htmlContentDO)
					{
						FWDR3DCarModTweenMax.to(self.htmlContentDO, .8, {w:scaleW - borderScale * 2, h:scaleH - borderScale * 2, ease:Quart.easeOut});
					}
				}
				else
				{
					if (self.imageDO)
					{
						FWDR3DCarModTweenMax.to(self.imageDO, .8, {w:scaleW - borderScale * 2, h:scaleH - borderScale * 2, ease:Quart.easeOut});
					}
				}
			}
			else
			{
				FWDR3DCarModTweenMax.to(self, .8, {x:Math.floor(self.newX), scale:self.thumbScale, ease:Quart.easeOut, onComplete:self.setThumbVisibility});
			}
		};
		
		this.setThumbVisibility = function()
		{
			if (self.getZIndex() == 0)
			{
				self.setVisible(false);
			}
		};
		
		this.update = function()
		{
			if (parent.showRefl)
			{
				if (!self.reflCanvasDO)
				{
					self.addReflection();
				}
				else
				{
					self.reflCanvasDO.setAlpha(1);
					self.reflCanvasDO.setY(self.thumbHeight + parent.reflDist);
				}
			}
			else
			{
				if (self.reflCanvasDO)
				{
					self.reflCanvasDO.setAlpha(0);
				}
			}
		};
		
		this.hide = function(del)
		{
			var imgW = self.thumbWidth - self.borderSize * 2;
			var imgH = self.thumbHeight - self.borderSize * 2;
			
			FWDR3DCarModTweenMax.to(self.imageHolderDO, .8, {x:parseInt(self.thumbWidth/2), y:parseInt(self.thumbHeight/2), w:0, h:0, delay:del, ease:Expo.easeInOut});
			
			if (data.showThumbnailsHtmlContent)
			{
				if (self.htmlContentDO)
				{
					FWDR3DCarModTweenMax.to(self.htmlContentDO, .8, {x:-parseInt(imgW/2), y:-parseInt(imgH/2), delay:del, ease:Expo.easeInOut});
				}
			}
			else
			{
				if (self.imageDO)
				{
					FWDR3DCarModTweenMax.to(self.imageDO, .8, {x:-parseInt(imgW/2), y:-parseInt(imgH/2), delay:del, ease:Expo.easeInOut});
					
					if (self.reflCanvasDO)
					{
						FWDR3DCarModTweenMax.to(self.reflCanvasDO, .8, {alpha:0, delay:del, ease:Expo.easeInOut});
					}
				}
			}
		};

		this.onMouseClickHandler = function()
		{
			self.dispatchEvent(FWDR3DCarThumb.CLICK, {id:self.id});
		};
		
		this.onMouseTouchHandler = function(e)
		{
			if(e.preventDefault) e.preventDefault();
			
			self.dispatchEvent(FWDR3DCarThumb.CLICK, {id:self.id});
		};
		
		/* destroy */
		this.destroy = function()
		{
			FWDR3DCarModTweenMax.killTweensOf(self);
			FWDR3DCarModTweenMax.killTweensOf(self.mainDO);
			FWDR3DCarModTweenMax.killTweensOf(self.imageHolderDO);
			
			if (self.isMobile)
			{
				if (self.hasPointerEvent)
				{
					self.mainDO.screen.removeEventListener("MSPointerUp", self.onMouseTouchHandler);
				}
				else
				{
					self.mainDO.screen.removeEventListener("touchend", self.onMouseTouchHandler);
				}
			}
			else
			{
				if (self.screen.addEventListener)
				{
					self.mainDO.screen.removeEventListener("click", self.onMouseClickHandler);
				}
				else
				{
					self.mainDO.screen.detachEvent("onclick", self.onMouseClickHandler);
				}
			}
			
			clearTimeout(self.setTextHeightId);
			
			if (self.imageDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.imageDO);
				self.imageDO.disposeImage();
				self.imageDO.destroy();
			}
			
			if (self.htmlContentDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.htmlContentDO);
				self.htmlContentDO.destroy();
				self.htmlContentDO = null;
			}

			if (self.bgDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.bgDO);
				self.bgDO.destroy();
				self.bgDO = null;
			}
			
			if (self.borderDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.borderDO);
				self.borderDO.destroy();
				self.borderDO = null;
			}
			
			if (self.htmlContentDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.htmlContentDO);
				self.htmlContentDO.destroy();
			}
			
			if (self.gradientLeftDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.gradientLeftDO);
				self.gradientLeftDO.destroy();
			}
			
			if (self.gradientRightDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.gradientRightDO);
				self.gradientRightDO.destroy();
			}
			
			if (self.textGradientDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.textGradientDO);
				self.textGradientDO = null;
			}
			
			if (self.textDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.textDO);
				self.textDO = null;
			}
			
			if (self.textHolderDO)
			{
				FWDR3DCarModTweenMax.killTweensOf(self.textHolderDO);
				self.textHolderDO = null
			}

			self.imageHolderDO.destroy();
			self.mainDO.destroy();

			self.imageHolderDO = null;
			self.imageDO = null;
			self.htmlContentDO = null;
			
			self.mainDO = null;
			self.borderDO = null;
			self.bgDO = null;
			self.imageHolderDO = null;
			self.imageDO = null;
			self.htmlContentDO = null;
			self.gradientDO = null;
			self.gradientLeftDO = null;
			self.gradientRightDO = null;
			self.textHolderDO = null;
			self.textGradientDO = null;
			self.textDO = null;
			
			self.id = null;
			self.data = null;
			self.parent = null;
			self.backgroundColor = null;
			self.borderColor = null;
			
			self.screen.innerHTML = "";
			prototype.destroy();
			prototype = null;
			self = null;
			FWDR3DCarThumb.prototype = null;
		};

		this.init();
	};

	/* set prototype */
	FWDR3DCarThumb.setPrototype = function()
	{
		FWDR3DCarThumb.prototype = new FWDR3DCarDisplayObject3D("div", "absolute", "visible");
	};

	FWDR3DCarThumb.CLICK = "click";

	FWDR3DCarThumb.prototype = null;
	window.FWDR3DCarThumb = FWDR3DCarThumb;
}(window));
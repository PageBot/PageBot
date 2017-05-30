# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     image.py
#
from __future__ import division # Make integer division result in float.

import os
from drawBot import imageSize, imagePixelColor, save, restore, image, scale
from pagebot.elements.element import Element
from pagebot.style import DEFAULT_WIDTH, DEFAULT_HEIGHT, NO_COLOR # In case no image is defined.
from pagebot.toolbox.transformer import pointOffset, point2D
from pagebot.conditions import *

class Image(Element):
    u"""The Image element is a “normal” container, which contains one (or more) PixelMap elements and zero (or more)
    caption or other elements. This way the user can add mulitple PixelMaps, a title elements, etc. 
    The layout of the Image elements is defined in the same way as any other layout. Conditional rules can be 
    applied (e.g. if the image element changes size), or the child elements can be put on fixed positions."""
    
    def __init__(self, path=None, style=None, pixelMap=None, title=None, caption=None, clipRect=None, 
            mask=None, imo=None, w=None, h=None, imageConditions=None, conditions=None, **kwargs):
        self.image = None # Aviud setting of self.omage.w and self.omage.h while not initialized.
        Element.__init__(self, conditions=conditions, **kwargs)
        assert path is None or pixelMap is None # One or the other or both None.

        if imageConditions is None:
            imageConditions = (Top2TopSide(), Fit2Width())
        if pixelMap is None: # Path can also be None, making PixelMap show gray rectangle of missing image.
            pixelMap = PixelMap(path, name='PixelMap', clipRect=clipRect, mask=mask, imo=imo, w=w, h=h, 
                conditions=imageConditions, **kwargs) # Default width is leading.
        self.image = pixelMap # Property to add to self.elements and set pixelMap.parent to self.
        # Title can be any type of element, but most likely a text box.
        self.title = title # Property to add to self.elements and set caption.parent to self.
        # Caption can be any type of element, but most likely a text box.
        self.caption = caption # Property to add to self.elements and set caption.parent to self.
        self.solve() # Solve the optional conditions defined in pixelMap and caption.

    def _get_image(self):
        return self._image # Special element, as there normally is only one pixelMap. Use self.elements otherwise.
    def _set_image(self, pixelMap):
        self._image = pixelMap # Keep last pixel map as self.image attribute. Otherwise use self.elements.
        if pixelMap is not None: # Can be None to clear. 
            self.appendElement(pixelMap) # Add to self.elements and set pixelMap.parent to self.
    image = property(_get_image, _set_image)

    def _get_title(self):
        return self._title # Special element, as there normally is only one title. Use self.elements otherwise.
    def _set_title(self, e):
        self._title = e # Keep last title element as self.title attribute. Otherwise use self.elements.
        if e is not None: # Can be None to clear.
            self.appendElement(e) # Add to self.elements and set e.parent to self.
    title = property(_get_title, _set_title)

    def _get_caption(self):
        return self._caption # Special element, as there normally is only one caption. Use self.elements otherwise.
    def _set_caption(self, e):
        self._caption = e # Keep last caption element as self.title attribute. Otherwise use self.elements.
        if e is not None: # Can be None to clear.
            self.appendElement(e) # Add to self.elements and set e.parent to self.
    caption = property(_get_caption, _set_caption)

    def _get_w(self):
        return self._w 
    def _set_w(self, w):
        if w != self._w: # Only when changed
            self._w = w
            self.solve() # Rearrange the layout of the elements inside
            #if self.image is not None:
            #    self.image.w = w - self.pl - self.pr
            _, _, _, self._h = self.paddedBox()
    w = property(_get_w, _set_w)

    def _get_h(self):
        return self._h
    def _set_h(self, h): 
        if h != self._h: # Only when changed
            self._h = h
            self.solve() # Rearrange the layout of elements inside.
            #if self.image is not None:
            #    self.image.h = h - self.pb - self.pt
            # Take over the width from whatever it became
            _, _, self._w, _ = self.paddedBox()
    h = property(_get_h, _set_h)


class PixelMap(Element):
    u"""The PixelMap contains the reference to the actual binary image data. eId can be (unique) file path or eId."""
   
    def __init__(self, path, w=None, h=None, z=0, clipRect=None, clipPath=None, mask=None, 
        imo=None, **kwargs):
        Element.__init__(self, **kwargs)

        # One of the two needs to be defined, the other can be None.
        # If both are set, then the image scales disproportional.
        self.w = w
        self.h = h
        self.z = z # Make conditions work with captions inside the image frame element.

        self.mask = mask # Optional mask element.
        self.clipRect = clipRect # Optional clip rectangle
        self.clipPath = clipPath # Optional clip path.
        self.imo = imo # Optional ImageObject with filters defined. See http://www.drawbot.com/content/image/imageObject.html
        self.setPath(path) # If path is omitted, a gray/crossed rectangle will be drawn.
        
    def __repr__(self):
        return '[%s eId:%s path:%s]' % (self.__class__.__name__, self.eId, self.path)

    def setPath(self, path):
        u"""Set the path of the image. If the path exists, the get the real
        image size and store as self.iw, self.ih."""
        self.path = path
        self.initImageSize() # Get real size from the file.

    def initImageSize(self):
        if self.path is not None and os.path.exists(self.path):
            self.iw, self.ih = imageSize(self.path)
        else:
            self.iw = self.ih = 0 # Undefined, there is no image file.

    def getPixelColor(self, p, scaled=True):
        u"""Answer the color in either the scaled point (x, y) or original image size point."""
        assert self.path is not None
        x, y = point2D(p)
        if scaled:
            x = self.w / self.iw
            y = self.h / self.ih
        return imagePixelColor(self.path, (x, y))

    # Set the intended width and calculate the new scale, validating the
    # width to the image minimum width and the height to the image minimum height.
    # Also the proportion is calculated, depending on the ratio of """
    def _get_w(self):
        if not self._w: # Width is undefined
            if self._h and self.ih:
                return self.iw * self._h / self.ih  # Height is lead, calculate width.
            return DEFAULT_WIDTH # Undefined and without parent, answer default width.
        return self._w # Width is lead and defined as not 0 or None.
    def _set_w(self, w):
        self._w = w # If self._h is set too, do disproportional sizing. Otherwise set to 0 or None.
    w = property(_get_w, _set_w)

    def _get_h(self):
        if not self._h: # Width is undefined
            if self._w and self.iw:
                return self.ih * self._w / self.iw  # Width is lead, calculate height.
            return DEFAULT_HEIGHT # Undefined and without parent, answer default width.
        return self._h # Height is lead and defined as not 0 or None.
    def _set_h(self, h):
        self._h = h # If self._w is set too, do disproportional sizing. Otherwise set to 0 or None.
    h = property(_get_h, _set_h)

    def _getAlpha(self):
        u"""Use alpha channel of the fill color as opacity of the image."""
        sFill = self.css('fill', NO_COLOR)
        if isinstance(sFill, (tuple, list)) and len(sFill) == 4:
            _, _, _, alpha = sFill
        else:
            alpha = 1
        return alpha

    def draw(self, origin, view):
        u"""Draw the image in the calculated scale. Since we need to use the image
        by scale transform, all other measure (position, lineWidth) are scaled
        back to their original proportions.
        If stroke is defined, then use that to draw a frame around the image.
        Note that the (sx, sy) is already scaled to fit the padding position and size."""
        p = pointOffset(self.oPoint, origin)   
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        if self.path is None or not os.path.exists(self.path) or not self.iw or not self.ih:
            # TODO: Also show error, in case the image does not exist, to differ from empty box.
            self._drawMissingElementRect(page, px, py, self.w, self.h)
        else:
            save()
            sx = self.w / self.iw
            sy = self.h / self.ih
            scale(sx, sy)
            
            # If there is a clipRect defined, create the bezier path
            if self.clipRect is not None:
                clipRect = BezierPath()
                clX, clY, clW, clH = self.clipRect
                sclX = clX/sx
                sclY = clY/sx
                sclW = clW/sx
                sclH = clH/sy
                # move to a point
                clipRect.moveTo((sclX, sclY))
                # line to a point
                clipRect.lineTo((sclX, sclY+sclH))
                clipRect.lineTo((sclX+sclW, sclY+sclH))
                clipRect.lineTo((sclX+sclW, sclY))
                # close the path
                clipRect.closePath()
                # set the path as a clipping path
                clipPath(clipRect)
                # the image will be clipped inside the path
                #fill(1, 0, 0, 0.5)
                #drawPath(clipRect)
            elif self.clipPath is not None:
                #Otherwise if there is a clipPath, then use it.
                clipPath(self.clipPath)

            # Store page element Id in this image, in case we want to make an image index later.
            image(self.path, (px/sx, py/sy), pageNumber=0, alpha=self._getAlpha())
            # TODO: Draw optional (transparant) forground color?
            restore()

        # If there are child elements, draw them over the pixel image.
        self._drawElements(origin, view)

        self._restoreScale()
        view.drawElementMetaInfo(self, origin)

   

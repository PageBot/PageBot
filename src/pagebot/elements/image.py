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
import os
from drawBot import imageSize
from pagebot.elements.element import Element
from pagebot.style import DEFAULT_WIDTH, DEFAULT_HEIGHT # In case no image is defined.
from pagebot.toolbox.transformer import pointOffset

class Image(Element):
    u"""The Image element is a “normal” container, which contains one (or more) PixelMap elements and zero (or more)
    caption or other elements. This way the user can add mulitple PixelMaps, a title elements, etc. 
    The layout of the Image elements is defined in the same way as any other layout. Conditional rules can be 
    applied (e.g. if the image element changes size), or the child elements can be put on fixed positions."""
    
    def __init__(self, path=None, pixelMap=None, caption=None, clipRect=None, mask=None, imo=None, eId=None, 
            w=None, h=None, **kwargs):
        Element.__init__(self, w=w, h=h, eId=None, **kwargs)
        assert path is None or image is None

        if pixelMap is None: # Path can also be None, making PixelMap show gray rectangle of missing image.
            pixelMap = PixelMap(path, clipRect=clipRect, mask=mask, imo=imo, **kwargs) # Default width is leading.
        self.appendElement(pixelMap) # Add to self.elements and set image.parent to self.
        if caption is not None: # Caption can be any type of element, but most likely a text box.
            self.appendElement(caption) # Add to self.elements and set caption.parent to self.
        self.solve() # Solve the optional conditions defined in pixelMap and caption.

class PixelMap(Element):
    u"""The PixelMap contains the reference to the actual binary image data. """
   
    def __init__(self, path, clipRect=None, mask=None, imo=None, **kwargs):
        Element.__init__(self, **kwargs)
        
        self.mask = mask # Optional mask element.
        self.clipRect = clipRect
        self.imo = imo # Optional ImageObject with filters defined. See http://www.drawbot.com/content/image/imageObject.html
        self.setPath(path) # If path is omitted, a gray/crossed rectangle will be drawn.

    def __repr__(self):
        return '[%s %s]' % (self.__class__.__name__, self.eId or self.path)

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

    # Set the intended width and calculate the new scale, validating the
    # width to the image minimum width and the height to the image minimum height.
    # Also the proportion is calculated, depending on the ratio of """
    def _get_w(self):
        if not self._w: # Width is undefined
            if self._h and :

                return self._proportionalW()  # Height is lead, calculate width.
            if self.parent: # No size defined, parent width is lead
                return self.parent.w
            return DEFAULT_WIDTH # Undefined and without parent.
        return self._w # Width is lead and defined as not 0.
    def _set_w(self, w):
        self._w = w
    w = property(_get_w, _set_w)

    def _get_h(self):
        if not self._h: # Height is undefined
            if self._w and self.iw:
                return self._w * self.ih / self.iw # Width is lead, calculate height.
            if self.parent: # No size defined, parent width is lead
                return self.parent.w
            return DEFAULT_WIDTH # Undefined and without parent.
        return self._w # Width is lead and defined as not 0.
    def _set_h(self, h):
        self._h = h
    h = property(_get_h, _set_h)

    def setScale(self, w=None, h=None, proportional=True):
        u"""Answer the scale of the image, calculated from it's own width/height and
        the optional (self.w, self.h)"""

        if w is None:
            w = self.w
        if h is None:
            h = self.h
        _, _, pw, ph = self.paddedBox # Calculate padding, because it will adjust scale.
        if not self.iw or not self.ih:
            # Cannot calculate the scale if the image does not exist.
            sx = sy = 1 # self.w and self.h un
            self._w = self.css('w', DEFAULT_WIDTH) # Copy from original plain style, without scaling.
            self._h = self.css('h', DEFAULT_HEIGHT)
        elif w is None and h is None:
            sx = sy = 1 # Use default size of the image.
            self._w = self.css('w', DEFAULT_WIDTH) # Copy from original plain style, without scaling.
            self._h = self.css('h', DEFAULT_HEIGHT)
        elif not proportional and w is not None and h is not None: # Needs to be disproportional scale
            sx = 1.0 * pw / self.iw
            sy = 1.0 * ph / self.ih
            self._w = pw # Copy from original plain style, without scaling.
            self._h = ph
        elif w is not None and h is not None: # Calculate proportional size, fitting the largest in w/h
            sx = 1.0 * pw / self.iw
            sy = 1.0 * ph / self.ih
            sx = sy = min(sx, sy)  # Which one is the smallest fitting scale
            self._w = self.iw * sx # Take over requested (w, h) as target size, proportionally scaled.
            self._h = self.ih * sy
        elif w is not None:
            sx = sy = 1.0 * pw / self.iw
            self._w = pw
            self._h = self.ih * sy # Calculate proprtional height for the requested width.
        else:
            sx = sy = 1.0 * ph / self.ih
            self._w = self.iw * sx # Calculate proportional width for the requested height.
            self._h = ph
        # TODO Add fitting function
        #sx = sy = min(sx, sy) # Keep the smallest to make image fit available space.
        self.sx = sx
        self.sy = sy

    def getCaptionSize(self, page):
        """Figure out what the height of the text is, with the width of this text box."""
        return textSize(self.caption or '', width=self.w)

    def getImageSize(self):
        u"""Answer the w/h pixel size of the real image."""
        return self.iw, self.ih

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

        px, py, pw, ph = self.getPadded(px, py, self.w, self.h)
        # Calculate the height of the caption box, soe we can reduce the height of the image.
        # Draw the caption at the bottom of the image space.
        if self.caption is not None and self.iw is not None and self.ih is not None:
            # @@@@@@ TODO: need to solve bug with caption width here.
            capW = pw # Caption on original width of layout, not proportional scaled image width.
            _, capH = textSize(self.caption, width=capW)
            self.caption.draw((px, py))
            # Calculate new image size.
            px, py, pw, ph = self.getPadded(x, y+capH, self.w, self.h - capH)
            self.setScale(h=ph) # Force recalculation of the image scale on height
            # Caluclate new width from ratio, in case we need to draw a frame.
            pw = ph * self.iw / self.ih

        if self.path is None or not os.path.exists(self.path):
            # TODO: Also show error, in case the image does not exist, to differ from empty box.
            self._drawMissingElementRect(page, px, py, pw, ph)
        else:
            if self.sx is None: # In case not initialized yet.
                self.setScale(pw, ph)
            if self.sx is not None: # Check again if scale was set successfully.
                save()
                scale(self.sx, self.sy)

                # Draw the actual image, vertical aligned.
                yAlign = self.yAlign
                if yAlign == TOP:
                    psy = (py + self.h)/self.sy - self.ih # TODO: Solve vertical alignment.
                elif yAlign == MIDDLE:
                    psy = (py + self.h/2)/self.sy - self.ih/2
                else: # Must be bottom align then
                    psy = (py + self.h)/self.sy - self.ih
                
                # Calculate horizontal alignment.
                if self.align == RIGHT:
                    px -= pw
                elif self.align == CENTER:
                    px -= pw/2
                
                # If there is a clipRect defined, create the bezier path
                if self.clipRect is not None:
                    clipRect = BezierPath()
                    clX, clY, clW, clH = self.clipRect
                    sclX = clX/self.sx
                    sclY = clY/self.sx
                    sclW = clW/self.sx
                    sclH = clH/self.sy
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
                    fill(1, 0, 0, 0.5)
                    drawPath(clipRect)

                # Store page element Id in this image, in case we want to make an image index later.
                image(self.path, (px/self.sx, psy), pageNumber=page.eId or 0, alpha=self._getAlpha())

                 # Draw background color if requested.
                sFill = self.style.get('fill')
                if not sFill in (None, NO_COLOR): # In case we need to draw the background.
                    setFillColor(sFill)
                    setStrokeColor(None)
                    rect(px/self.sx, psy, pw/self.sx, ph/self.sy)

                # Draw the frame around the image, if requested.
                sStroke = self.style.get('stroke')
                sStrokeWidth = self.style.get('strokeWidth')
                if not sStroke in (None, NO_COLOR) and sStrokeWidth : # In case we need to draw the border.
                    setFillColor(None)
                    setStrokeColor(sStroke, sStrokeWidth/self.sx )
                    rect(px/self.sx, psy, pw/self.sx, ph/self.sy)

                # TODO: Draw optional (transparant) forground color?
                restore()
            else:
                print('Could not set scale of image "%s"' % self.path)

        # If there are child elements, draw them over the text.
        self._drawElements(origin)

        self._restoreScale()
        view.drawElementMetaInfo(self, origin)

   

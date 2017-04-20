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

class Image(Element):
    u"""Image element has special attributes self.iw and self.ih for the real image size.
    If the optional captionStyle is not defined, then use self.style for captions."""
    def __init__(self, path, point=None, parent=None, style=None, name=None, eId=None, captionStyle=None, caption=None, clipRect=None, mask=None, imo=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, name=name, eId=eId, **kwargs)
        self.mask = mask # Optional mask element.
        self.clipRect = clipRect
        self.imo = imo # Optional ImageObject with filters defined. See http://www.drawbot.com/content/image/imageObject.html
        self.captionStyle = captionStyle or self.style
        # Check if there is caption content. Tne make the FormattedString, so we know the heigh.
        if caption:
            self.caption = getFormattedString(self.captionStyle)
        else:
            self.caption = None
        # Set all size and scale values.
        self.setPath(path) # If path is omitted, a gray/crossed rectangle will be drawn.
        # Check on one of the (w, h) in the style. One of the can be undefined for proportional scaling.
        # Set default to 1 column
        if self.w is not None and self.h is not None:
            self.w = self.css('cw')
        #print self.ih, path

    def __repr__(self):
        return '[%s %s]' % (self.__class__.__name__, self.eId or self.path)

    def setPath(self, path):
        u"""Set the path of the image. If the path exists, the get the real
        image size and store as self.iw, self.ih."""
        self.path = path
        self.initImageSize()

    def initImageSize(self):
        if self.path is not None and os.path.exists(self.path):
            self._iw, self._ih = imageSize(self.path)
            self.setScale(self.w, self.h) # Calculate scale and scaled self.sw and self.sh
        else:
            self._iw = self._ih = 0 # Undefined, but calculating.

    def _get_iw(self):
        if not self._iw:
            self.initImageSize()
        return self._iw
    iw = property(_get_iw)

    def _get_ih(self):
        if not self._ih:
            self.initImageSize()
        return self._ih
    ih = property(_get_ih)

    def setSize(self, w, h):
        u"""Set the intended size and calculate the new scale."""
        self._w = max(w or 0, self.minW)
        self._h = max(h or 0, self.minH)
        self.sx = self.sy = None # Force calculation, overwriting any defined style scale.
        self.setScale()

    # Set the intended width and calculate the new scale, validating the
    # width to the image minimum width and the height to the image minimum height.
    # Also the proportion is calculated, depending on the ratio of """
    def _get_w(self):
        return self._w
    def _set_w(self, w):
        self._w = w
        self.setScale(w=w)
    w = property(_get_w, _set_w)

    def _get_h(self):
        return self._h
    def _set_h(self, h):
        self._h = h
        self.setScale(h=h)
    h = property(_get_h, _set_h)

    def setScale(self, w=None, h=None, proportional=True):
        u"""Answer the scale of the image, calculated from it's own width/height and
        the optional (self.w, self.h)"""

        if w is None:
            w = self.w
        if h is None:
            h = self.h
        _, _, pw, ph = self.getPaddedBox() # Calculate padding, because it will adjust scale.
        if not self.iw or not self.ih:
            # Cannot calculate the scale if the image does not exist.
            sx = sy = 1
            self._w = self.css('w') # Copy from original plain style, without scaling.
            self._h = self.css('h')
        elif w is None and h is None:
            sx = sy = 1 # Use default size of the image.
            self._w = self.css('w') # Copy from original plain style, without scaling.
            self._h = self.css('h')
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
        sFill = self.style.get('fill', NO_COLOR)
        if isinstance(sFill, (tuple, list)) and len(sFill) == 4:
            _, _, _, alpha = sFill
        else:
            alpha = 1
        return alpha

    def _drawCaption(self, caption, x, y, w, h):
        u"""Draw the caption, if there is one defined. It is assumed that self.caption contains
        a FormattedString and the (w,h) is already calculated rectangle of the formatted string."""
        if caption is not None:
            rectFill = self.captionStyle.get('fill')
            if rectFill != NO_COLOR:
                setFillColor(rectFill)
                rect(x, y, w, h)
            textBox(caption, (x, y, w, h))

    def draw(self, origin):
        u"""Draw the image in the calculated scale. Since we need to use the image
        by scale transform, all other measure (position, lineWidth) are scaled
        back to their original proportions.
        If stroke is defined, then use that to draw a frame around the image.
        Note that the (sx, sy) is already scaled to fit the padding position and size."""
        ox, oy = pointOffset(self.point, origin)
        px, py, pw, ph = self.getPadded(ox, oy, self.w, self.h)
        # Calculate the height of the caption box, soe we can reduce the height of the image.
        # Draw the caption at the bottom of the image space.
        if self.caption is not None and self.iw is not None and self.ih is not None:
            # @@@@@@ TODO: need to solve bug with caption width here.
            capW = pw # Caption on original width of layout, not proportional scaled image width.
            _, capH = textSize(self.caption, width=capW)
            self._drawCaption(self.caption, px, py, capW, capH)
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
                yAlign = self.style.get('yAlign')
                if yAlign == TOP_ALIGN:
                    psy = (py + self.h)/self.sy - self.ih # TODO: Solve vertical alignment.
                elif yAlign == CENTER:
                    psy = (py + self.h/2)/self.sy - self.ih/2
                else: # Must be bottom align then
                    psy = (py + self.h)/self.sy - self.ih
                
                # Calculate horizontal alignment.
                if self.style.get('align') == RIGHT_ALIGN:
                    px -= pw
                elif self.style.get('align') == CENTER:
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


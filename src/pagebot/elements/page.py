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
#     page.py
#
from datetime import datetime
#from math import cos, sin, radians, degrees, atan2

#from AppKit import NSBezierPath

from drawBot import stroke, newPath, drawPath, moveTo, lineTo, strokeWidth, oval, text, rect, fill, curveTo, \
    closePath, FormattedString

from pagebot import setFillColor, setStrokeColor
from pagebot.style import NO_COLOR, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot.toolbox.markers import drawCropMarks, drawRegistrationMarks

class Page(Element):
             
    def _drawPageInfo(self, origin):
        u"""Draw additional document information, color markers, page number, date, version, etc.
        outside the page frame, if drawing crop marks."""
        px, py, _ = pointOffset(self.point, origin) # Ignore z-axis for now
        if self.css('showPageInfo'):
            bleed = self.css('bleed')
            cms = self.css('cropMarkSize')
            dt = datetime.now()
            d = dt.strftime("%A, %d. %B %Y %I:%M%p")
            s = 'Page %s | %s | %s' % (self.name, d, self.parent.title or 'Untitled')
            fs = FormattedString(s, font='Verdana', fill=0, fontSize=6)
            text(fs, (px + bleed, py + self.h + cms)) # Draw on top of page.

    def _drawPageFrame(self, origin):
        u"""If the show flag is set, then draw the cropmarks or page frame."""
        px, py, _ = pointOffset(self.point, origin) # Ignore z-axis for now.
        if self.css('showPageFrame'):
            fill(None)
            stroke(0, 0, 1)
            strokeWidth(0.5)
            rect(px, py, self.w, self.h)

    def _drawPageMetaInfo(self, origin):
        # If there is an offset and drawing cropmarks (or frame)
        if self.css('showCropMarks'):
            bleed = self.css('bleed')
            cmSize = self.css('cropMarkSize')
            cmStrokeWidth = self.css('cropMarkStrokeWidth')
            drawCropMarks(origin, self.w, self.h, bleed, cmSize, cmStrokeWidth, self.css('folds'))
            drawRegistrationMarks(origin, self.w, self.h, cmSize, cmStrokeWidth) 
        # If there is an offset and drawing cropmarks (or frame):
        self._drawPageInfo(origin)
        # If there is an offset and drawing cropmarks (or frame)
        self._drawPageFrame(origin)
        # Check if we need to draw the flow arrows.
        self._drawFlowConnections(origin)

    def draw(self, origin):
        u"""If the size of the document is larger than the size of the page, then use the extra space
        to draw cropmarks and other print-related info. This also will make the bleeding of images 
        visible. Page drawing can have an offset too, in case it is used as placed element on another page.
        If self.scaleX and self.scaleY are not None, then scale the drawing of the entire page,
        keeping the x and y position unscaled."""
        px, py, pz = p = pointOffset(self.point, origin) # Ignoe z-axis for now.
        #ox, oy = self._applyScale(ox, oy) #@@@@@ WRONG
        # Now we may be in scaled mode.
        if self.parent.w > self.w: # Document larger than page, center and draw crop-marks
            px = (self.parent.w - self.w) / 2
        if self.parent.h > self.h:
            py = (self.parent.h - self.h) / 2

        # If there are child elements, draw them over the text.
        self._drawElements(p)
        # Draw addition page info, such as crop-mark, registration crosses, etc. if parameters are set.
        self._drawPageMetaInfo(origin)
        # Check if we are in scaled mode. Then restore.
        #self._restoreScale()


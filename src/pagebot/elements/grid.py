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
#     grid.py
#
from drawBot import rect, newPath, moveTo, lineTo, drawPath, text 

from pagebot import getFormattedString, setFillColor, setStrokeColor
from pagebot.elements.element import Element
from pagebot.style import LEFT_ALIGN, RIGHT_ALIGN, CENTER, NO_COLOR, makeStyle
from pagebot.toolbox.transformer import pointOrigin2D

class Grid(Element):

    def draw(self, origin):
        u"""Draw grid of lines and/or rectangles if colors are set in the style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        # Drawing the grid as squares.
        p = pointOrigin2D(self.point, origin)
        p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        px, py = self._applyAlignment(p)

        sGridFill = self.css('gridFill', NO_COLOR)
        gutter = self.css('g') # Gutter
        columnWidth = self.css('cw') # Column width
        columnHeight = self.css('ch') # Column height
        marginLeft = self.css('ml') # Margin left
        marginTop = self.css('mt') # Margin top
        marginRight = self.css('mr') # Margin right
        marginBottom = self.css('mb') # Margin bottom
        w = self.w
        h = self.h
        if self.css('showGridColumns') and sGridFill is not NO_COLOR:
            setFillColor(sGridFill)
            setStrokeColor(None)
            ox = px + marginLeft
            while ox < w - marginRight - columnWidth:
                oy = h - marginTop - columnHeight - gutter
                while oy >= 0:
                    rect(ox, oy + gutter, columnWidth, columnHeight)
                    oy -= columnHeight + gutter
                ox += columnWidth + gutter
        # Drawing the grid as lines.
        if self.css('showGrid') and self.css('gridStroke', NO_COLOR) is not NO_COLOR:
            setFillColor(None)
            setStrokeColor(self.css('gridStroke', NO_COLOR), self.css('gridStrokeWidth'))
            # TODO: DrawBot align and fill don't work properly now.
            M = 16
            fs = getFormattedString('', self, dict(font='Verdana', align='right', fontSize=M/2,
                stroke=None, textFill=self.css('gridStroke')))
            ox = px + marginLeft
            index = 0
            oy = h - marginTop - py
            while ox < px + w - marginRight:
                newPath()
                moveTo((ox, py))
                lineTo((ox, py + h))
                moveTo((ox + columnWidth, py))
                lineTo((ox + columnWidth, py + h))
                drawPath()
                text(fs+repr(index), (ox + M * 0.3, oy + M / 4))
                index += 1
                ox += columnWidth + gutter
            index = 0
            while oy > py:
                newPath()
                moveTo((px, oy))
                lineTo((px + w, oy))
                moveTo((px, oy - columnHeight))
                lineTo((px+w, oy - columnHeight))
                drawPath()
                text(fs + repr(index), (px + marginLeft - M / 2, oy - M * 0.6))
                index += 1
                oy -= columnHeight + gutter

        self._restoreScale()

class BaselineGrid(Grid):

    def draw(self, origin):
        u"""Draw baseline grid if line color is set in the style.
        TODO: Make fixed values part of calculation or part of grid style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        if self.css('showBaselineGrid'):
            p = pointOrigin2D(self.point, origin)
            p = self._applyOrigin(p)    
            p = self._applyScale(p)    
            px, py = self._applyAlignment(p)

            oy = self.h - self.css('mt') - py
            line = 0
            M = 16
            # Format of line numbers.
            # TODO: DrawBot align and fill don't work properly now.
            fs = getFormattedString('', self, dict(font=self.css('fallbackFont','Verdana'), align='right', fontSize=M/2,
                stroke=None, textFill=self.css('gridStroke')))
            while oy > self.css('mb', 0):
                setFillColor(None)
                setStrokeColor(self.css('baselineGridStroke', NO_COLOR), self.css('gridStrokeWidth'))
                newPath()
                moveTo((px + M, py + oy))
                lineTo((px + self.parent.w - M, py + oy))
                drawPath()
                text(fs + repr(line), (px + M - 2, py + oy - M * 0.6))
                text(fs + repr(line), (px + self.parent.w - M - 8, py + oy - M * 0.6))
                line += 1 # Increment line index.
                oy -= self.css('baselineGrid') # Next vertical line position of baseline grid.

            self._restoreScale()


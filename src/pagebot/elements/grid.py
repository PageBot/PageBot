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
from pagebot.elements.element import Element
from pagebot.style import LEFT_ALIGN, RIGHT_ALIGN, CENTER, NO_COLOR, makeStyle

class Grid(Element):
    def __init__(self, point=None, parent=None, eId='grid', style=None, **kwargs):
        self._w = self._h = None
        Element.__init__(self, point, parent, eId, style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, origin):
        u"""Draw grid of lines and/or rectangles if colors are set in the style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        # Drawing the grid as squares.
        ox, oy = pointOrigin2D(self.point, origin)

        sGridFill = self.style.get('gridFill', NO_COLOR)
        gutter = self.style['g'] # Gutter
        columnWidth = self.style['cw'] # Column width
        columnHeight = self.style['ch'] # Column height
        marginLeft = self.style['ml'] # Margin left
        marginTop = self.style['mt'] # Margin top
        marginRight = self.style['mr'] # Margin right
        marginBottom = self.style['mb'] # Margin bottom
        w = self.w
        h = self.h
        if self.style.get('showGridColumns') and sGridFill is not NO_COLOR:
            setFillColor(sGridFill)
            setStrokeColor(None)
            ox = px + marginLeft
            while ox < w - marginRight - columnWidth:
                y = h - marginTop - columnHeight - gutter
                while oy >= 0:
                    rect(ox, oy+gutter, columnWidth, columnHeight)
                    oy -= columnHeight + gutter
                ox += columnWidth + gutter
        # Drawing the grid as lines.
        if self.style.get('showGrid') and self.style.get('gridStroke', NO_COLOR) is not NO_COLOR:
            setFillColor(None)
            setStrokeColor(self.style.get('gridStroke', NO_COLOR), self.style.get('gridStrokeWidth'))
            # TODO: DrawBot align and fill don't work properly now.
            M = 16
            fs = FormattedString('', font='Verdana', align='right', fontSize=M/2,
                stroke=None, fill=self.style['gridStroke'])
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
                text(fs+repr(index), (x + M * 0.3, y + M / 4))
                index += 1
                x += columnWidth + gutter
            index = 0
            while y > py:
                newPath()
                moveTo((px, oy))
                lineTo((px + w, oy))
                moveTo((px, oy - columnWidth))
                lineTo((px+w, oy - columnWidth))
                drawPath()
                text(fs + repr(index), (px + marginLeft - M / 2, oy - M * 0.6))
                index += 1
                y -= columnHeight + gutter

class BaselineGrid(Grid):

    def draw(self, origin):
        u"""Draw baseline grid if line color is set in the style.
        TODO: Make fixed values part of calculation or part of grid style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        if self.style.get('showBaselineGrid'):
            ox, oy = pointOrigin2D(self.point, origin)
            oy = self.h - self.style['mt'] - py
            line = 0
            M = 16
            # Format of line numbers.
            # TODO: DrawBot align and fill don't work properly now.
            fs = FormattedString('', font=self.style.get('fallbackFont','Verdana'), align='right', fontSize=M/2,
                stroke=None, fill=self.style.get('gridStroke'))
            while y > self.style.get('mb', 0):
                setFillColor(None)
                setStrokeColor(self.style.get('baselineGridStroke', NO_COLOR), self.style.get('gridStrokeWidth'))
                newPath()
                moveTo((px + M, py + y))
                lineTo((px + page.w - M, py + y))
                drawPath()
                text(fs + repr(line), (px + M - 2, py + y - M * 0.6))
                text(fs + repr(line), (px + page.w - M - 8, py + y - M * 0.6))
                line += 1 # Increment line index.
                oy -= self.style.get('baselineGrid') # Next vertical line position of baseline grid.



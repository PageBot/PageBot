#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     textbox.py
#
from pagebot.style import (LEFT, RIGHT, CENTER, MIN_WIDTH, MIDDLE,
                           BOTTOM, DEFAULT_WIDTH)
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset

class TextBox(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.
    isTextBox = True

    TEXT_MIN_WIDTH = 24 # Absolute minumum with of a text box.

    def __init__(self, bs=None, minW=None, w=DEFAULT_WIDTH, h=None, showBaselines=False, **kwargs):
        Element.__init__(self,  **kwargs)
        u"""Creates a TextBox element. Default is the storage of self.s
        (DrawBot FormattedString or Flat equivalent), but optional it can also be ts (tagged str)
        if output is mainly through build and HTML/CSS. Since both strings cannot be conversted lossless
        one into the other, it is safer to keep them both if they are available.

        """
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.minW = max(minW or 0, MIN_WIDTH, self.TEXT_MIN_WIDTH)
        self._textLines = self._baseLines = None # Force initiaize upon first usage.
        self.size = w, h
        self.bs = self.newString(bs) # Source can be any type: BabelString instance or plain unicode string.
        self.showBaselines = showBaselines # Force showing of baseline if view.showBaselines is False.

    def _get_w(self): # Width
        u"""Property for self.w, holding the width of the textbox.

        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> tb = TextBox(parent=page, w=125)
        >>> page[tb.eId].w
        125
        >>> tb.w = 150
        >>> tb.w, tb.w == page[tb.eId].w
        (150, True)
        """
        return min(self.maxW, max(self.minW, self.style['w'], MIN_WIDTH)) # From self.style, don't inherit.
    def _set_w(self, w):
        self.style['w'] = w or MIN_WIDTH # Overwrite element local style from here, parent css becomes inaccessable.
        self._textLines = None # Force reset if being called
    w = property(_get_w, _set_w)

    def _get_h(self):
        u"""Answer the height of the textBox. If self.style['h'] is None, then answer the
        vertical space that the text needs.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> font = findFont('Roboto-Regular')
        >>> style = dict(font=font.path, fontSize=14)
        >>> tb = TextBox('This is content', parent=page, style=style, w=100, h=220)
        >>> page[tb.eId].h
        220
        """

        """
        TODO: Get the tests to work properly
        >>> tb.h = 220
        >>> tb.h, tb.h == page[tb.eId].h
        (220, True)
        >>> tb.h = None
        >>> tb.h, tb.style['h'] is None
        (37.0, True)
        """
        if self.style['h'] is None: # Elastic height
            h = self.getTextSize(w=self.w)[1] + self.pt + self.pb # Add paddings
        else:
            h = self.style['h']
        return min(self.maxH, max(self.minH, h)) # Should not be 0 or None
    def _set_h(self, h):
        # Overwrite style from here, unless self.style['elasticH'] is True
        self.style['h'] = h # If None, then self.h is elastic defined by content
    h = property(_get_h, _set_h)

    def _get_textLines(self):
        if self._textLines is None:
            return []
        return self._textLines
    textLines = property(_get_textLines)

    def __getitem__(self, lineIndex):
        return self.textLines[lineIndex]

    def __len__(self):
        return len(self.textLines)

    def __repr__(self):
        u"""Answer the representation string of the element.

        >>> e = TextBox('ABC')
        >>> e.eId in str(e) # TextBox:236DE32AAC108A45490 (0, 0)ABC'
        True
        >>> e = TextBox('ABC', x=100, y=100, w=200)
        >>> e.eId in str(e)
        True
        """
        if self.title:
            name = ':'+self.title
        elif self.name:
            name = ':'+self.name
        else: # No naming, show unique self.eId:
            name = ':'+self.eId

        if self.bs.s:
            s = ' S(%d)' % len(self.bs)
        else:
            s = ''

        if self.elements:
            elements = ' E(%d)' % len(self.elements)
        else:
            elements = ''
        return '%s%s (%d, %d)%s%s' % (self.__class__.__name__, name, int(round(self.point[0])), int(round(self.point[1])), self.bs.s, elements)

    def copy(self, parent=None):
        u"""Answer a full copy of self, where the "unique" fields are set to default.
        Also perform a deep copy on all child elements.

        >>> e = TextBox('Hello world', name='Child', w=100)
        >>> copyE = e.copy() # Copy the element attribute, including the string of self.
        >>> #copyE.bs # TODO: Needs development and testing
        Hello world
        """
        e = Element.copy(self, parent=parent)
        e.bs = self.bs # Copy the string separately.
        return e

    # BabelString support, answering the structure that holds strings for all builder types.

    def setText(self, bs, style=None):
        u"""Set the formatted string to s, using style or self.style. The bs as also be a number, in which
        case is gets converted into a string."""
        if isinstance(bs, (int, float)):
            bs = str(bs)
        if isinstance(bs, str):
            bs = self.newString(bs, e=self, style=style)
        self.bs = bs

    def _get_text(self):
        u"""Answer the plain text of the current self.bs"""
        return u'%s' % self.bs
    text = property(_get_text)

    def append(self, bs, style=None):
        u"""Append to the string type that is defined by the current view/builder type.
        Note that the string is already assumed to be styled or can be added as plain string.
        Don't calculate the overflow here, as this is a slow/expensive operation.
        Also we don't want to calculate the textLines/runs for every string appended,
        as we don't know how much more the caller will add. bs._textLines is set to None
        to force recalculation as soon as bs.textLines is called again.
        If bs is not a BabelString instance, then create one, defined by the self.context,
        and based on the style of self."""
        #assert isinstance(bs, (str, self.context.STRING_CLASS))
        #self.bs += self.newString(bs, e=self, style=style)
        self.bs += bs
        #self.bs = self.newString(bs, e=self, style=style)

    def appendMarker(self, markerId, arg=None):
        self.bs.appendMarker(markerId, arg)

    def getTextSize(self, bs=None, w=None):
        """Figure out what the width/height of the text self.bs is, with or given width or
        the styled width of this text box. If fs is defined as external attribute, then the
        size of the string is answers, as if it was already inside the text box.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> context.name in ('DrawBotContext', 'FlatContext', 'SvgContext')
        True

        """
        """
        TODO: Get these tests or similar to work.
        >>> font = findFont('Roboto-Regular')
        >>> bs = context.newString('ABC', style=dict(font=font.path, fontSize=124))
        >>> tb = TextBox(bs, w=100, h=None)
        >>> tb.bs
        ABC
        >>> tb.getTextSize()[1]
        436.0
        >>> bs = context.newString('ABC', style=dict(font=font.path, fontSize=24))
        >>> tb = TextBox(bs, w=100, h=None)
        >>> tb.getTextSize()[1]
        28.0
        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> c = FlatContext()
        >>> bs = c.newString('ABC', style=dict(font=font.path, fontSize=124))
        >>> tb = TextBox(bs, w=100, h=None)
        >>> tb.getTextSize()[1] # ???
        73.0
        """
        if bs is None:
            bs = self.bs
        return bs.textSize(w or self.w)

    def getOverflow(self, w=None, h=None):
        """Figure out what the overflow of the text is, with the given (w, h) or styled
        (self.w, self.h) of this text box. If h is None and self.h is None then by
        definintion overflow will allways be empty, as the box is elastic."""
        if self.h is None and h is None: # In case height is undefined, box will aways fit the content.
            return ''
        # Otherwise test if there is overflow of text in the given element size.
        if w is None:
            w = self.w-self.pr-self.pl
        if h is None:
            h = self.h-self.pt-self.pb
        return self.bs.textOverflow(w, h, LEFT)

    def NOTNOW_getBaselinePositions(self, y=0, w=None, h=None):
        u"""Answer the list vertical baseline positions, relative to y (default is 0)
        for the given width and height. If omitted use (self.w, self.h)"""
        baselines = []
        for _, baselineY in self.bs.baseLines(0, y, w or self.w, h or self.h):
            baselines.append(baselineY)
        return baselines

    def _findStyle(self, run):
        u"""Answer the name and style that desctibes this run best. If there is a doc
        style, then answer that one with its name. Otherwise answer a new unique style name
        and the style dict with its parameters."""
        print(run.attrs)
        return('ZZZ', run.style)

    def getStyledLines(self):
        u"""Answer the list with (styleName, style, textRun) tuples, reversed engeneered
        from the FormattedString self.bs. This list can be used to query the style parameters
        used in the textBox, or to create CSS styles from its content."""
        styledLines = []
        prevStyle = None
        for line in self.textLines:
            for run in line.runs:
                styleName, style = self._findStyle(run)
                if prevStyle is None or prevStyle != style:
                    styledLines.append([styleName, style, run.string])
                else: # In case styles of runs are identical (e.g. on line wraps), just add.
                    styledLines[-1][-1] += run.string
                prevStyle = style
        return styledLines

    #   F L O W

    def isOverflow(self, tolerance=0):
        u"""Answer the boolean flag if this element needs overflow to be solved.
        This method is typically called by conditions such as Overflow2Next or during drawing
        if the overflow marker needs to be drawn.
        Note: There is currently not a test if text actually went into the next element. It's just
        checking if there is a name defined, not if it exists or is already filled by another flow."""
        return self.nextElement is None and self.getOverflow() != ''

    def overflow2Next(self):
        u"""Try to fix if there is overflow."""
        result = True
        overflow = self.getOverflow()
        if overflow and self.nextElement: # If there is text overflow and there is a next element?
            result = False
            # Find the page of self
            page = self.getElementPage()
            if page is not None:
                # Try next page
                nextElement = page.getElementByName(self.nextElement) # Optional search  next page too.
                if nextElement is None or nextElement.bs and self.nextPage:
                    # Not found or not empty, search on next page.
                    page = self.doc.getPage(self.nextPage)
                    nextElement =  page.getElementByName(self.nextElement)
                if nextElement is not None and not nextElement.bs:
                    # Finally found one empty box on this page or next page?
                    nextElement.bs = overflow
                    nextElement.prevPage = page.name
                    nextElement.prevElement = self.name # Remember the back link
                    score = nextElement.solve() # Solve any overflow on the next element.
                    result = not score.fails # Test if total flow placement succeeded.
        return result

    #   B U I L D

    def build(self, view, origin, drawElements=True):
        u"""Draw the text on position (x, y). Draw background rectangle and/or frame if
        fill and/or stroke are defined."""
        context = view.context # Get current context

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        # TODO: Add marker if there is overflow text in the textbox.

        self.buildFrame(view, p) # Draw optional background, frame or borders.

        # Let the view draw frame info for debugging, in case view.showElementFrame == True
        view.drawElementFrame(self, p) 

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # Draw the text with horizontal and vertical alignment
        tw, th = self.bs.textSize()
        xOffset = yOffset = 0
        if self.css('yTextAlign') == MIDDLE:
            yOffset = (self.h - self.pb - self.pt - th)/2
        elif self.css('yTextAlign') == BOTTOM:
            yOffset = self.h - self.pb - self.pt - th
        if self.css('xTextAlign') == CENTER:
            xOffset = (self.w - self.pl - self.pr - tw)/2
        elif self.css('xTextAlign') == RIGHT:
            xOffset = self.w - self.pl - self.pr - tw

        textShadow = self.textShadow
        if textShadow:
            context.saveGraphicState()
            context.setShadow(textShadow)

        context.textBox(self.bs, (px + self.pl + xOffset, py + self.pb-yOffset,
            self.w-self.pl-self.pr, self.h-self.pb-self.pt))

        if textShadow:
            context.restoreGraphicState()

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p)

        # Draw markers on TextLine and TextRun positions.
        self._drawBaselines_drawBot(view, px, py)

        if view.showTextOverflowMarker and self.isOverflow():
            self._drawOverflowMarker_drawBot(view, px, py)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'

    def build_html(self, view, origin=None, showElements=True):
        u"""Build the HTML/CSS code through WebBuilder (or equivalent) that is the closest representation of self.
        If there are any child elements, then also included their code, using the
        level recursive indent."""

        context = view.context # Get current context.
        b = context.b

        self.build_css(view)
        # Use self.cssClass if defined, otherwise self class. #id is ignored if None
        b.div(cssClass=self.cssClass or self.__class__.__name__.lower(), cssId=self.cssId) 
        b.addHtml(self.bs.s) # Get HTML from BabelString in HtmlString context.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view)

        if showElements:
            for e in self.elements:
                e.build_html(view, origin)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view)

        b._div() # self.cssClass or self.__class__.__name__

    def _drawBaselines_drawBot(self, view, px, py):
        # Let's see if we can draw over them in exactly the same position.
        if not view.showTextBoxBaselines and not self.showBaselines:
            return

        c = self.context # Get current context and builder

        fontSize = self.css('baseLineMarkerSize')
        indexStyle = dict(font='Verdana', fontSize=8, textFill=(0, 0, 1))
        yStyle = dict(font='Verdana', fontSize=fontSize, textFill=(0, 0, 1))
        leadingStyle = dict(font='Verdana', fontSize=fontSize, textFill=(1, 0, 0))

        if view.showTextBoxY:
            bs = self.newString('0', style=indexStyle)
            _, th = c.textSize(bs)
            c.text(bs.s, (px + self.w + 3,  py + self.h - th/4))

        c.stroke((0, 0, 1), 0.5)
        prevY = 0
        for textLine in []: #self.textLines: TODO: not implemented yet.
            y = textLine.y
            # TODO: Why measures not showing?
            c.line((px, py+y), (px + self.w, py+y))
            if view.showTextBoxIndex:
                fs = self.newString(str(textLine.lineIndex), style=indexStyle)
                tw, th = c.textSize(fs) # Calculate right alignment
                c.text(fs.s, (px-3-tw, py + y - th/4))
            if view.showTextBoxY:
                fs = self.newString('%d' % round(y), style=yStyle)
                _, th = c.textSize(fs)
                c.text(fs.s, (px + self.w + 3, py + y - th/4))
            if view.showTextBoxLeading:
                leading = round(abs(y - prevY))
                fs = self.newString('%d' % leading, style=leadingStyle)
                _, th = c.textSize(fs)
                c.text(fs.s, (px + self.w + 3, py + prevY - leading/2 - th/4))
            prevY = y

    def _drawOverflowMarker_drawBot(self, view, px, py):
        u"""Draw the optional overflow marker, if text doesn't fit in the box."""
        b = self.b # Get current builder from self.doc.context.b
        fs = self.newString('[+]', style=dict(textFill=(1, 0, 0), font='Verdana-Bold', fontSize=8))
        tw, th = b.textSize(fs.s)
        if self.originTop:
            pass
        else:
            b.text(fs.s, (px + self.w - 3 - tw, py + th/2))

    #   C O N D I T I O N S

    # Text conditions

    def isBaselineOnTop(self, tolerance):
        u"""Answer the boolean if the top baseline is located at self.parent.pt."""
        return abs(self.top - (self.parent.h - self.parent.pt - self.textLines[0].y + self.h)) <= tolerance

    def isBaselineOnBottom(self, tolerance):
        u"""Answer the boolean if the bottom baseline is located at self.parent.pb."""
        return abs(self.bottom - self.parent.pb) <= tolerance

    def isAscenderOnTop(self, tolerance):
        return True

    def isCapHeightOnTop(self, tolerance):
        return True

    def isXHeightOnTop(self, tolerance):
        return True


    def baseline2Top(self):
        self.top = self.parent.h - self.parent.pt - self.textLines[0].y + self.h
        return True

    def baseline2Bottom(self):
        self.bottom = self.parent.pb # - self.textLines[-1].y
        return True

    def floatBaseline2Top(self):
        # ...
        return True

    def floatAscender2Top(self):
        # ...
        return True

    def floatCapHeight2Top(self):
        # ...
        return True

    def floatXHeight2Top(self):
        # ...
        return True

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

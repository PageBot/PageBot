# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     textbox.py
#
from pagebot.style import LEFT, RIGHT, CENTER, NO_COLOR, MIN_WIDTH, MIN_HEIGHT, \
    makeStyle, MIDDLE, BOTTOM, DEFAULT_WIDTH, DEFAULT_HEIGHT, ORIGIN
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot.fonttoolbox.objects.glyph import Glyph

class TextBox(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.
    isTextBox = True

    TEXT_MIN_WIDTH = 24 # Absolute minumum with of a text box.

    def __init__(self, bs=None, minW=None, w=DEFAULT_WIDTH, h=None, showBaselines=False, **kwargs):
        Element.__init__(self,  **kwargs)
        u"""Default is the storage of self.s (DrawBot FormattedString or Flat equivalent), 
        but optional it can be ts (tagged basestring)
        if output is mainly through build and HTML/CSS. Since both strings cannot be conversted lossless one into the other,
        it is safer to keep them both if they are available."""
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.minW = max(minW or 0, MIN_WIDTH, self.TEXT_MIN_WIDTH)
        self._textLines = self._baseLines = None # Force initiaize upon first usage.
        self.size = w, h
        self.bs = self.newString(bs) # Source can be any type: BabelString instance or plain unicode string.
        self.showBaselines = showBaselines # Force showing of baseline if view.showBaselines is False.

    def _get_w(self): # Width
        return min(self.maxW, max(self.minW, self.style['w'], MIN_WIDTH)) # From self.style, don't inherit.
    def _set_w(self, w):
        self.style['w'] = w or MIN_WIDTH # Overwrite element local style from here, parent css becomes inaccessable.
        self._textLines = None # Force reset if being called
    w = property(_get_w, _set_w)

    def _get_h(self):
        u"""Answer the height of the textBox. If self.style['elasticH'] is set, then answer the 
        vertical space that the text needs. This overwrites the setting of self._h."""
        if self.style['h'] is None: # Elastic height
            h = self.getTextSize(w=self.w)[1] + self.pt + self.pb # Add paddings
        else:
            h = self.style['h']
        return min(self.maxH, max(self.minH, h)) # Should not be 0 or None
    def _set_h(self, h):
        # Overwrite style from here, unless self.style['elasticH'] is True
        self.style['h'] = h # If None, then self.h is elastic from content
    h = property(_get_h, _set_h)

    def __getitem__(self, lineIndex):
        return self.textLines[lineIndex]

    def __len__(self):
        return len(self.textLines)
  
    def __repr__(self):
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

    # SuperString support, answering the structure that holds strings for all builder types.
  

    def setText(self, s):
        u"""Set the formatted string to s, using self.style."""
        self.x = self.newString(s, e=self)

    def _get_text(self):
        u"""Answer the plain text of the current self.bs"""
        return u'%s' % self.bs
    text = property(_get_text)
    
    def append(self, bs):
        u"""Append to the string type that is defined by the current view/builder type.
        Note that the string is already assumed to be styled or can be added as plain string.
        Don't calculate the overflow here, as this is slow/expensive operation.
        Also we don't want to calcualte the textLines/runs for every string appended,
        as we don't know how much more the caller will add. self._textLines is set to None
        to force recalculation as soon as self.textLines is called again.
        If bs is not a BabelString instance, then create one, defined by the self.context,
        and based on the style of self."""
        assert isinstance(bs, (basestring, self.context.STRING_CLASS))
        self.bs += self.newString(bs, e=self)

    def appendMarker(self, markerId, arg=None):
        marker = getMarker(markerId, arg=arg)
        if self.bs.type == 'html':
            marker = '<!-- %s -->' % marker
        self.append(marker)

    def getTextSize(self, bs=None, w=None):
        """Figure out what the width/height of the text self.bs is, with or given width or
        the styled width of this text box. If fs is defined as external attribute, then the
        size of the string is answers, as if it was already inside the text box."""
        if bs is None:
            bs = self.bs
        return bs.textSize(w or self.w)

    def getOverflow(self, w=None, h=None):
        """Figure out what the overflow of the text is, with the given (w,h) or styled
        (self.w, self.h) of this text box. If self.style['elasticH'] is True, then by
        definintion overflow will allways be empty."""
        if self.css('elasticH'): # In case elasticH is True, box will aways fit the content.
            return ''
        # Otherwise test if there is overflow of text in the given size.
        return self.bs.textOverflow(w or self.w-self.pr-self.pl, h or self.h-self.pt-self.pb, LEFT)

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
        print run.attrs
        print '#++@+', run.style
        return 'ZZZ', run.style

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
        return self.nextElement is None and len(self.getOverflow())

    def overflow2Next(self):
        u"""Try to fix if there is overflow."""
        result = True
        overflow = self.getOverflow(b)
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
                    result = len(score.fails) == 0 # Test if total flow placement succeeded.
        return result

    #   B U I L D

    def build(self, view, origin=ORIGIN, drawElements=True):
        u"""Draw the text on position (x, y). Draw background rectangle and/or frame if
        fill and/or stroke are defined."""
        context = view.context # Get current context

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
   
        # TODO: Add marker if there is overflow text in the textbox.

        self.buildFrame(view, p) # Draw optional frame or borders.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(view, p)

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
 
        if view.showTextOverflowMarker and self.isOverflow(b):
            self._drawOverflowMarker_drawBot(view, px, py)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'

    def build_html(self, view, origin=None, showElements=True):
        u"""Build the HTML/CSS code through WebBuilder (or equivalent) that is the closest representation of self. 
        If there are any child elements, then also included their code, using the
        level recursive indent."""
        
        context = view.context # Get current context.
        b = context.b

        self.build_css(view)
        if self.info.htmlPath is not None:
            b.includeHtml(self.htmlPath) # Add HTML content of file, if path is not None and the file exists.
        else:
            b.div(class_=self.class_)
            b.addHtml(self.bs.s) # Get HTML from BabelString in HtmlString context.

            if self.drawBefore is not None: # Call if defined
                self.drawBefore(self, view, origin)

            if showElements:
                for e in self.elements:
                    e.build_html(view, origin)

            if self.drawAfter is not None: # Call if defined
                self.drawAfter(self, view, origin)

            b._div() 

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
            bs = self.newString(`0`, style=indexStyle)
            _, th = c.textSize(bs)
            c.text(bs.s, (px + self.w + 3,  py + self.h - th/4))

        c.stroke((0, 0, 1), 0.5)
        prevY = 0
        for textLine in []: #self.textLines: TODO: not implemented yet.
            y = textLine.y
            # TODO: Why measures not showing?
            context.line((px, py+y), (px + self.w, py+y))
            if view.showTextBoxIndex:
                bs = self.newString(`textLine.lineIndex`, style=indexStyle)
                tw, th = c.textSize(fs) # Calculate right alignment
                c.text(bs.s, (px-3-tw, py + y - th/4))
            if view.showTextBoxY:
                bs = self.newString('%d' % round(y), style=yStyle)
                _, th = c.textSize(fs)
                c.text(bs.s, (px + self.w + 3, py + y - th/4))
            if view.showTextBoxLeading:
                leading = round(abs(y - prevY))
                bs = self.newString('%d' % leading, style=leadingStyle)
                _, th = c.textSize(fs)
                c.text(bs.s, (px + self.w + 3, py + prevY - leading/2 - th/4))
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





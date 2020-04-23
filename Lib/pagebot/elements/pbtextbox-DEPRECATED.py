# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     pbtext.py
#
#     Using the DrawBot textBox() instead of text() for better control
#     of alignment, position and leading (in case there are "\n" returns
#     in the string)
#
from pagebot.constants import MIDDLE, BOTTOM, CENTER, RIGHT, DEFAULT_LANGUAGE
from pagebot.elements.pbtext import Text
from pagebot.toolbox.units import pointOffset, point2D, pt, em, units, uRound, upt

class TextBox(Text):

    def _get_w(self):
        """Answer the calculate width of self.bs.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', leading=em(1), fontSize=pt(100))
        >>> bs = context.newString('ABCDEFGH', style)
        >>> e = Text(bs) # Context is taken from bs
        >>> e.w, e.h
        (482.7pt, 100pt)
        >>> e.size
        (482.7pt, 100pt)

        """
        return self.getTextSize()[0]
    def _set_w(self, w):
        pass # Ignore, will aways be overwritten by the width of self.bs
    w = property(_get_w, _set_w)
   
    def _get_h(self):
        """Answer the calculate height of self.bs.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', leading=em(1.4), fontSize=pt(100))
        >>> bs = context.newString('ABCDEFGH', style)
        >>> bs.context
        <DrawBotContext>
        >>> e = Text(bs) # Context to calculate size is bs.context
        >>> bs is e.bs # Using the same string as reference.
        True
        >>> e.h # Height includes the leading.
        140pt
        >>> bs.leading = em(1) # Set the leading of e.bs string.
        >>> e.bs.style['leading']
        1em
        >>> e.h # Dynamic calculation by the BabelString and context inside.
        100pt
        """
        return self.getTextSize()[1]
    def _set_h(self, h):
        pass # Ignore, will aways be overwritten by the height of self.bs
    h = property(_get_h, _set_h)
        
    def getTextSize(self, w=None):
        """Figure out what the width/height of the text self.pbs is. 
        Ignore w if it is defined.
        
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.document import Document
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> doc = Document(w=1000, h=1000, context=context)
        >>> style = dict(font='PageBot-Regular', leading=em(1.2), fontSize=pt(100))
        >>> bs = context.newString('ABCD', style)
        >>> e = Text(bs, parent=doc[1])
        >>> e.getTextSize(), e.size == e.getTextSize()
        ((250.9pt, 120pt), True)
        >>> bs.textSize == e.getTextSize()
        True
        >>> doc.export('_export/Text-getTextSize.pdf')
        """
        return self.bs.textSize

    def _get_xAlign(self): 
        """Answer the type of x-alignment. Since the orienation of the box is equivalent to the
        on the alignment of the text, it is stored as self.style, referring to the current run.
        That is why we redefine the default element.xAlign propety.

        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = context.newString('ABCD', dict(xAlign=CENTER))
        """
        return self._validateXAlign(self.bs.xAlign)
    def _set_xAlign(self, xAlign):
        self.bs.aAlign = self._validateXAlign(xAlign) # Save locally, blocking CSS parent scope for this param.
    xAlign = property(_get_xAlign, _set_xAlign)

    #   B U I L D

    def build(self, view, origin, drawElements=True, **kwargs):
        """Draws the text on position (x, y). Draw background rectangle and /
        or frame if fill and / or stroke are defined.

        >>> from pagebot.document import Document
        >>> from pagebot.elements import *
        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.units import pt
        >>> context = getContext('DrawBot')
        >>> doc = Document(w=500, h=100, context=context)
        >>> view = doc.view
        >>> view.showOrigin = True
        >>> view.padding = pt(30)
        >>> view.showCropMarks = True
        >>> view.showFrame = True
        >>> style = dict(font='PageBot-Regular', fontSize=pt(18), textFill=(1, 0, 0), xAlign=CENTER)
        >>> txt = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit valim mecto trambor.'
        >>> bs = context.newString(txt, style) # Creates a BabelString with context reference.
        >>> bs.context is context
        True
        >>> tb = Text(bs, x=100, y=50, parent=doc[1])
        >>> tb.context is context
        True
        >>> doc.export('_export/Text-build.pdf')
        """
        context = view.context # Get current context
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
        self._applyRotation(view, p)

        # Let the view draw frame info for debugging, in case view.showFrame == True.
        view.drawElementFrame(self, p, **kwargs)
        # Draw optional background, frame or borders.
        self.buildFrame(view, (self.left, self.bottom, self.w, self.h))

        # Call if defined.
        if self.drawBefore is not None:
            self.drawBefore(self, view, p)

        # self has its own baseline drawing, derived from the text, instance of
        # self.baselineGrid.
        #self.drawBaselines(view, px, py, background=True) # In case there is a baseline at the back

        textShadow = self.textShadow

        if textShadow:
            context.saveGraphicState()
            context.setShadow(textShadow)

        box = clipPath = None

        if self.clipPath is not None: # Use the elements as clip path:
            clipPath = self.clipPath
            clipPath.translate((px, py))
            context.text(self.bs, clipPath=clipPath)

        elif clipPath is None:
            # If there are child elements, then these are used as layout for
            # the clipping path.
            if 0 and self.elements:
                # Construct the clip path, so we don't need to restore
                # translate.
                clipPath = self.childClipPath
                if clipPath is not None:
                    clipPath.translate((self.pl, self.pb))
                clipPath.translate((self.pl, self.pb))
                context.text(self.bs, clipPath=clipPath)
            else:
                # One of box or clipPath are now defined.
                context.text(self.bs, (px+self.pl, py+self.pb))

        if textShadow:
            context.restoreGraphicState()

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p)

        if view.showTextOverflowMarker and self.isOverflow():
            # TODO: Make this work for FlatContext too
            self._drawOverflowMarker_drawBot(view, px, py)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'
        view.drawElementOrigin(self, p)

    #   C O N D I T I O N S

    def fitFontSize2Right(self):
        """Make the right padding of the parent, without moving the left
        position. Overwriting the default behavior of Element, as we want text
        to be fiting too.

        >>> from pagebot import getContext
        >>> from pagebot.conditions import *
        >>> e = Element(padding=pt(30), w=1000, h=1000)
        >>> bs = BabelString('Test', style=dict(fontSize=pt(20)))
        >>> t = Text(bs, parent=e, conditions=(Left2Left(), Fit2Width()))
        >>> result = t.solve()
        >>> t.w
        940pt
        """
        # FIXME
        #self.w = self.parent.w - self.parent.pr - self.x
        #self.bs = self.STRING_CLASS(self.bs.s, style=self.style, w=self.pw)
        return True

    # Shrinking box sizes, conditional testers and movers

    def isShrunkOnTextHeight(self, tolerance=0):
        """Answer the boolean flag if the element height fits the height of the text.

        >>> from pagebot.document import Document
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> doc = Document(context=context)
        >>> p = pt(1000)
        >>> t = Text(padding=pt(30), w=p, h=p, parent=doc[1])
        >>> t.context
        <DrawBotContext>
        >>> t.isShrunkOnTextHeight()

        """
        context = self.context
        assert context is not None
        if self.bs is not None:
            return abs(context.textSize(self.bs)[0] - self.h) <= tolerance
        return not self.h

    def shrink2TextHeight(self, tolerance=0):
        """Shrink the box vertical to fit the vertical bounding box of the
        current text. This also tests by e.isShrunkOnTextHeight()

        >>> from pagebot.contexts import getContext
        >>> from pagebot.conditions import *
        >>> from pagebot.document import Document
        >>> context = getContext('DrawBot')
        >>> doc = Document(context=context)
        >>> e = Element(padding=pt(30), w=1000, h=1000, parent=doc[1])
        >>> bs = BabelString('Test' * 30, dict(fontSize=pt(50)))
        >>> t = Text(bs, parent=e, w=200, h=500, conditions=[Shrink2TextHeight()])
        >>> result = t.solve()
        >>> t.w, t.h # FIXME: Right value?
        (200pt, 2100pt)
        """
        context = self.context
        assert context is not None
        if self.bs is not None:
            self.h = context.textSize(self.bs)[1]
        else:
            self.h = 0

    def isShrunkOnTextWidth(self, tolerance=0):
        context = self.context
        assert context is not None
        if self.bs is not None:
            return abs(context.textSize(self.bs)[0] - self.w) <= tolerance
        return not self.w

    def shrink2TextWidth(self, tolerance=0):
        """Shrink the box horizontal to fit the horizontal bounding box of the
        current text. This also tests by e.isShrunkOnTextWidth()

        >>> from pagebot import getContext
        >>> from pagebot.conditions import *
        >>> from pagebot.document import Document
        >>> context = getContext('DrawBot')
        >>> doc = Document(context=context)
        >>> e = Element(padding=pt(30), w=1000, h=1000, parent=doc[1])
        >>> bs = BabelString('Test', dict(fontSize=pt(100)))
        >>> t = Text(bs, parent=e, conditions=[Shrink2TextWidth()])
        >>> result = t.solve()
        >>> round(t.w)
        >>> # yields 197pt in Flat context.
        #202pt
        """
        context = self.context
        assert context is not None
        if self.bs is not None:
            self.w = context.textSize(self.bs)[0]
        else:
            self.w = 0

     # Text conditional testers and movers

    def getMatchingStyleLine(self, style, index=0):
        """Scan through the lines. Test the first textRun of each line to
        match all of the (font, fontSize, textFill) keys of the style.
        Then answer the line. Otherwise answer None.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style1 = dict(font='PageBot-Regular', fontSize=pt(12))
        >>> bs = context.newString('ABCD ' * 100, style1) 
        >>> style2 = dict(font='PageBot-Regular', fontSize=pt(12))
        >>> bs += context.newString('EFGH' * 100, style2)
        >>> t = Text(bs)
        >>> t.getMatchingStyleLine(style2)
        """
        matchingIndex = 0
        for line in self.textLines:
            for run in line.bs:
                if run.style == style:
                    return line
        return None

   # Baseline matching, conditional testers and movers

    def isBaselineOnGrid(self, tolerance, index=None, style=None):
        try:
            parent = self.parent
            if parent is None:
                return False # Cannot test, there is no parent grid
            line = self.textLines[index or 0]
            return abs(self.getDistance2Grid(self.top + line.y)) <= tolerance
        except IndexError:
            return False

    def styledBaselineDown2Grid(self, style, index=0, parent=None):
        """Move the index-th baseline that fits the style down to match the grid."""
        if parent is None:
            parent = self.parent
        if self.textLines and parent is not None:
            line = self.getMatchingStyleLine(style, index)
            if line is not None:
                self.top += parent.getDistance2Grid(line.y)

    def baseline2Grid(self, index=0, gridIndex=None, parent=None):
        """If gridIndex is defined, then position the index-th line on
        gridIndex-th baseline. If gridIndex is None, then round to
        nearest grid line position.

        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> from pagebot.conditions import *
        >>> context = getContext('DrawBot') 
        >>> doc = Document(context=context)
        >>> e = Element(padding=pt(30), w=1000, h=1000, parent=doc[1])
        >>> e.baselineGrid = pt(24)
        >>> e.baselineStart = pt(44)
        >>> bs = context.newString('Test', style=dict(fontSize=pt(150)))
        >>> t = Text(bs, parent=e)
        >>> t.baseline2Grid()
        >>> t.y # FIXME: Right value?
        -11pt
        >>> result = t.solve()
        >>> t.y # FIXME: Right value?
        -11pt
        """
        if parent is None:
            parent = self.parent
        textLines = self.textLines
        if textLines and parent is not None:
            assert index in range(len(self.textLines)), \
                ('%s.baselineDown2Grid: Index "%d" is not in range of available textLines "%d"' % \
                (self.__class__.__name__, index, len(self.textLines)))
            line = textLines[index]
            d = parent.getDistance2Grid(line.y)
            self.y += d # Round down
            if d > parent.baselineGrid/2:
                self.y += parent.baselineGrid

    def baselineUp2Grid(self, index=0, parent=None):
        """Move the text box up (decreasing line.y value, rounding in down direction) in vertical direction,
        so the baseline of self.textLines[index] matches the parent grid.
        """
        if parent is None:
            parent = self.parent
        if self.textLines and parent is not None:
            assert index in range(len(self.textLines)), \
                ('%s.baselineDown2Grid: Index "%d" is not in range of available textLines "%d"' % \
                (self.__class__.__name__, index, len(self.textLines)))
            line = self.textLines[index]
            self.top -= parent.getDistance2Grid(line.y) - parent.baselineGrid

    def baselineDown2Grid(self, index=0, parent=None):
        """Move the text box down in vertical direction, so the baseline of self.textLines[index]
        matches the parent grid.
        """
        if parent is None:
            parent = self.parent
        if self.textLines:
            assert index in range(len(self.textLines)), \
                ('%s.baselineDown2Grid: Index "%d" is not in range of available textLines "%d"' % \
                (self.__class__.__name__, index, len(self.textLines)))
            line = self.textLines[index]
            self.top -= parent.getDistance2Grid(line.y)

    def getBaselineY(self, index=0, parent=None):
        """Answer the vertical baseline position of the indexed line.

        >>> from pagebot import getContext
        >>> from pagebot.conditions import *
        >>> from pagebot.constants import *
        >>> from pagebot.document import Document
        >>> context = getContext('DrawBot')
        >>> doc = Document(context=context)
        >>> e = Element(padding=100, w=1000, h=1000, parent=doc[1])
        >>> bs = context.newString('Test', dict(fontSize=pt(150)))
        >>> t = Text(bs, parent=e, yAlign=TOP, conditions=[Shrink2TextBounds(), Top2Top()])
        >>> result = t.solve()
        """
        if parent is None:
            parent = self.parent
        textLines = self.textLines # Calculate or get as cached list.
        if textLines and index in range(len(textLines)):
            line = self.textLines[index]
            return parent.h - parent.pt + line.y
        return None

    def _get_baselineY(self):
        return self.getBaselineY(index=0)

    def _set_baselineY(self, y):
        self.y += self.baseline - y

    baselineY = property(_get_baselineY, _set_baselineY)

    def isBaselineOnTop(self, tolerance=0, index=0, parent=None):
        if parent is None:
            parent = self.parent

        baselineY = self.getBaselineY(index, parent)

        if baselineY is not None:
            return abs(self.top - baselineY) <= tolerance
        return False

    def baseline2Top(self, index=None, parent=None):
        """Move the vertical position of the indexed line to match self.top.

        """
        baselineY = self.getBaselineY(index, parent)
        if baselineY is not None:
            self.top = baselineY

    def isBaselineOnBottom(self, tolerance=0, index=0, parent=None):
        if parent is None:
            parent = self.parent
        baselineY = self.getBaselineY(index, parent)
        if baselineY is not None:
            return abs(self.bottom - baselineY) <= tolerance
        return False

    def baseline2Bottom(self, index=None, parent=None):
        """Move the vertical position of the indexed line to match the positon
        of self.parent.bottom."""
        baselineY = self.getBaselineY(index, parent)
        if baselineY is not None:
            self.bottom = baselineY

    # Cap height conditional testers and movers

    def isCapHeightOnTop(self, tolerance=0, index=0, parent=None):
        return False

    def capHeight2Top(self, index=None, parent=None):
        """Move the vertical position of the indexed line to match self.top.
        """
        if parent is None:
            parent = self.parent
        textLines = self.textLines
        if textLines and parent is not None:
            line = self.textLines[0]
            capHeight = 0
            for textRun in line.textRuns:
                capHeight = max(capHeight, textRun.capHeight) # Take the max capHeight of the first line.
            self.top = self.parent.h - self.parent.pt + line.y - capHeight

    def capHeight2Bottom(self, index=None, parent=None):
        # TODO: Implement
        pass

    def capHeightUp2Grid(self, index=None, parent=None):
        """Move the text box up (decreasing line.y value, rounding in down
        direction) in vertical direction, so the baseline of
        self.textLines[index] matches the parent grid."""
        if self.textLines and parent is not None:
            assert index in range(len(self.textLines)), \
                ('%s.capHeightUp2Grid: Index "%d" is not in range of available textLines "%d"' % \
                (self.__class__.__name__, index, len(self.textLines)))
            line = self.textLines[index]
            if line.textRuns:
                textRun = line.textRuns[0]
                self.top += parent.getDistance2Grid(line.y + textRun.capHeight) + parent.baselineGrid

    def capHeightDown2Grid(self, index=0, parent=None):
        """Move the text box down in vertical direction, so the baseline of
        self.textLines[index] matches the parent grid."""
        if parent is None:
            parent = self.parent
        if self.textLines and parent is not None:
            assert index in range(len(self.textLines)), \
                ('%s.capHeightDown2Grid: Index "%d" is not in range of available textLines "%d"' % \
                (self.__class__.__name__, index, len(self.textLines)))
            line = self.textLines[index]
            if line.textRuns:
                textRun = line.textRuns[0]
                self.top += parent.getDistance2Grid(line.y + textRun.capHeight)

    # xHeight conditional testers and movers

    def isXHeightOnTop(self, tolerance=0, index=0, parent=None):
        return False

    def xHeight2Top(self, index=None, parent=None):
        """Move the xHeight of the text at padding-top position.
        """
        if parent is None:
            parent = self.parent
        textLines = self.textLines
        if textLines and parent is not None:
            line = self.textLines[0]
            xHeight = 0
            for textRun in line.textRuns:
                xHeight = max(xHeight, textRun.xHeight) # Take the max xHeight of the first line.
            print('xHeight2Top', self.parent.h, self.parent.pt, line.y, xHeight)
            self.top = self.parent.h - self.parent.pt + line.y - xHeight

    def xHeight2Bottom(self, index=None, parent=None):
        # TODO: implement.
        pass

    def xHeightUp2Grid(self, index=0, parent=None):
        """Move the text box up, so self.textLines[index].textRuns[0].xHeight
        matches the parent grid.
        """
        if parent is None:
            parent = self.parent
        if self.textLines and parent is not None:
            assert index in range(len(self.textLines)), \
                ('%s.xHeightUp2Grid: Index "%d" is not in range of available textLines "%d"' % \
                (self.__class__.__name__, index, len(self.textLines)))
            line = self.textLines[index]
            if line.textRuns:
                textRun = line.textRuns[0]
                self.top += parent.getDistance2Grid(line.y + textRun.xHeight) + parent.baselineGrid

    def xHeightDown2Grid(self, index=0, parent=None):
        """Move the text box down, so self.textLines[index].textRuns[0].xHeight
        matches the parent grid.
        """
        if parent is None:
            parent = self.parent
        if self.textLines and parent is not None:
            assert index in range(len(self.textLines)), \
                ('%s.xHeightDown2Grid: Index "%d" is not in range of available textLines "%d"' % \
                (self.__class__.__name__, index, len(self.textLines)))
            line = self.textLines[index]
            if line.textRuns:
                textRun = line.textRuns[0]
                self.top += parent.getDistance2Grid(line.y + textRun.xHeight)

    # Ascenders conditional testers and movers

    def ascender2Grid(self, index=None, parent=None):
        # Move the element, so ascender height of index-line is at grid of parent."""
        #TODO: implement.
        pass

    def ascender2Top(self, index=None, parent=None):
        # Move the element, so ascender height of index-line is at top of parent."""
        #TODO: implement.
        pass

    def ascender2Bottom(self, index=None, parent=None):
        # Move the element, so ascender height of index-line is at bottom of parent."""
        #TODO: implement.
        pass

    # Descender conditional testers and movers

    def descender2Grid(self, index=None, parent=None):
        # Move the element, so descender of index-line is on grid of parent."""
        #TODO: implement.
        pass

    def descender2Top(self, index=None, parent=None):
        # Move the element, so descender of index-line is on top of parent."""
        #TODO: implement.
        pass

    def descender2Bottom(self, index=None, parent=None):
        # Move the element, so descender of index-line is on bottom of parent."""
        #TODO: implement.
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

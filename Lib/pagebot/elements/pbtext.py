#!/usr/bin/env python3
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
#     The Text element is the simplest version of text elements. If no width
#     e.w is defined, it handles single line of text (unless there are hard coded \n
#     newlines embedded in the text.)
#     If e.w is defined, then the element behaves as a text box, where lines are
#     hyphenated, wrapped and alignment by lines.
#
import re
from copy import deepcopy

from pagebot.constants import *
from pagebot.contexts.basecontext.babelstring import BabelString
from pagebot.style import makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset, point2D, point3D, pt, units, upt
from pagebot.toolbox.color import color
from pagebot.toolbox.hyphenation import hyphenatedWords

class Text(Element):
    """
    Since PageBot stores text by the internal BabelString format, with
    full control on the position of lines, the rendering as “Text”
    if not DrawBot.textbox. The problem with text boxes in general, is
    that they position text from “above the ascender of the top line”,
    without much control on the position of baselines. Larger type in
    the first line will push the whole content of the box down.
    Therefor Text.build uses context.textLines() as render engine,
    and implements the drawing separate text lines by context.text(bs),
    which always tenders text on baseline position.
    This way different contexts also have more similar behavior.

    >>> t = Text('ABCD')
    >>> t
    <Text $ABCD$>
    >>> t = Text('ABCD')
    >>> t
    <Text $ABCD$>
    """
    isText = True

    # Absolute minimum width of a text box. Avoid endless elastic height.
    TEXT_MIN_WIDTH = 24

    def __init__(self, bs=None, w=None, h=None, size=None, style=None,
            parent=None, padding=None, conditions=None, xTextAlign=None,
            yAlign=None, **kwargs):

        self._bs = None # Placeholder, ignoring self.w and self.h until defined.
    
        # Adjust the attributes in **kwargs, so their keys are part of the
        # rootstyle, in order to do automatic conversion with makeStyle()
        Element.__init__(self, parent=parent, padding=padding,
            conditions=conditions, **kwargs)
        """Creates a Text element, holding storage of `self.bs`.
        BabelString instance."""

        # Combine rootStyle, optional self.style and **kwargs attributes.
        # Note that the final style is stored in the BabelString instance
        # self.bs. self.style is used as template, in the content is defined
        # as plain string.
        if style is not None:
            self.style = makeStyle(style, **kwargs)

        # Set as property, to make sure there's always a generic BabelString
        # instance or None. Needs to be done before element initialize, as
        # some attributes (Text.xTextAlign) may need the string style as reference.
        self.bs = bs # BabelString source for this Text element.

        if xTextAlign is not None:
            assert xTextAlign in XALIGNS
            self.xTextAlign = xTextAlign

        # Can be one of BASELINE (default), TOP (equivalent to ascender height
        # of first text line), CAPHEIGHT, XHEIGHT, MIDDLE_CAP, MIDDLE_X,
        # MIDDLE and BOTTOM
        if yAlign is not None:
            assert yAlign in YALIGNS
            # Overwite value in self.bs.style
            self.yAlign = yAlign

        # Now there is a self._bs, set it's width and height (can be None)
        self.w = w
        self.h = h

    def _get_bs(self):
        """Answer the stored formatted BabelString. The value can be None.
        """
        return self._bs
    def _set_bs(self, bs):
        """Make sure that this is a formatted BabelString.
        Otherwise create it from string with the current style. Note that there is a potential clash
        in the duplicate usage of fill and stroke.

        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30, context=context)
        >>> page = doc[1]
        >>> t = Text(parent=page, w=125)
        >>> # String converts to DrawBotString.
        >>> t.bs = 'ABCD'
        >>> t.bs
        $ABCD$
        >>> t
        <Text $ABCD$ w=125pt h=12pt>
        """
        if bs is None:
            bs = ''
        if isinstance(bs, str):
            bs = BabelString(bs, self.style, w=self.w, h=self.h)
        assert isinstance(bs, BabelString)
        self._bs = bs
        bs.context = self.context
    bs = property(_get_bs, _set_bs)

    def _get_w(self): # Width
        """Property for self._w, holding the width of the textbox.

        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> t = Text('ABCD', parent=page, w=125) # Width forces “Text” behavior
        >>> page[t.eId].w
        125pt
        >>> t.w = 150
        >>> t.w, t.w == page[t.eId].w
        (150pt, True)
        """
        if self._bs is None:
            return None
        return self.bs.w
    def _set_w(self, w):
        # If None, then self.w is elastic defined by self.bs height.
        if self._bs is not None:
            if w is not None:
                w = units(w)
            self.bs.w = w
    w = property(_get_w, _set_w)

    def _get_h(self):
        """Answers the height of the textBox if defined.
        Otherwise answer the height of self.bs.textSize

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> font = findFont('Roboto-Regular')
        >>> style = dict(font=font.path, fontSize=14)
        >>> t = Text('This is content', parent=page, style=style, w=100, h=220)
        >>> page[t.eId].h
        220pt
        >>> t.h = 220
        >>> t.h, t.h == page[t.eId].h
        (220pt, True)
        >>> t.h = None
        """
        if self._bs is None:
            return None
        return self.bs.h
    def _set_h(self, h):
        # If None, then self.h is elastic defined by self.bs height.
        if self._bs is not None:
            if h is not None:
                h = units(h)
            self.bs.h = h
    h = property(_get_h, _set_h)

    def _get_firstColumnIndent(self):
        """If False or 0, then ignore first line indent of a column on text
        overflow. Otherwise set to a certain unit. This will cause text being
        indented by the amount of self.firstLineIndent, probably midsentence.

        NOTE: probably never necessary, here just in case."""
        return self.css('firstColumnIndent')
    def _set_firstColumnIndent(self, indent):
        self.style['firstColumnIndent'] = units(indent)
    firstColumnIndent = property(_get_firstColumnIndent, _set_firstColumnIndent)

    def _get_firstLineIndent(self):
        """DrawBot-compatible indent of first line of a paragraph."""
        return self.css('firstLineIndent')
    def _set_firstLineIndent(self, indent):
        self.style['firstLineIndent'] = units(indent)
    firstLineIndent = property(_get_firstLineIndent, _set_firstLineIndent)

    def _get_indent(self):
        """DrawBot-compatible indent of text.
        """
        return self.css('indent')
    def _set_indent(self, indent):
        self.style['indent'] = units(indent)
    indent = property(_get_indent, _set_indent)

    def _get_baselines(self):
        if self._baselines is None:
            #self.textLines # Initialize both self._textLines and self._baselines
            self._get_textLines()
        return self._baselines
    baselines = property(_get_baselines)

    def __getitem__(self, lineIndex):
        textLines = self.textLines
        if lineIndex in range(len(textLines)):
            return self.textLines[lineIndex]
        return None

    def __len__(self):
        return len(self.textLines)

    def __repr__(self):
        """Answers the representation string of the element.

        >>> from pagebot.document import Document
        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.color import blackColor, noColor
        >>> style = dict(textFill=blackColor, textStroke=noColor)
        >>> context = getContext('DrawBot')
        >>> doc = Document(context=context)
        >>> bs = context.newString('ABCD', style)
        >>> e = Text(bs, parent=doc[1])
        >>> e
        <Text $ABCD$ w=30.11pt h=12pt>
        >>> e = Text(bs, x=100, y=100, w=200, parent=doc[1])
        >>> e
        <Text $ABCD$ x=100pt y=100pt w=200pt h=12pt>

        """
        """
        >>> from pagebot.document import Document
        >>> from pagebot.contexts.flatcontext.flatcontext import FlatContext
        >>> from pagebot.toolbox.color import blackColor, noColor
        >>> style = dict(textFill=blackColor, textStroke=noColor)
        >>> context = FlatContext()
        >>> doc = Document(context=context)
        >>> bs = context.newString('ABCD', style)
        >>> e = Text(bs, parent=doc[1])
        >>> e
        <Text $ABCD$>
        >>> e = Text(bs, x=100, y=100, w=200, parent=doc[1])
        >>> e
        <Text $ABCD$ x=100pt y=100pt w=200pt>
        """
        s = '<%s' % self.__class__.__name__
        if self.bs is not None and len(self.bs):
            s += ' %s' % self.bs
        if self.x:
            s += ' x=%s' % self.x
        if self.y:
            s += ' y=%s' % self.y
        if self.w is not None: # Behave a text box with defined width
            s += ' w=%s' % self.w
        if self.h is not None: # Behave as text box with defined height
            s += ' h=%s' % self.h
        return s+'>'

    def copy(self, parent=None):
        """Answers a full copy of `self`, where the "unique" fields are set to
        default. Also performs a deep copy on all child elements.

        >>> from pagebot.toolbox.color import blackColor, noColor
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(textFill=blackColor, textStroke=noColor)
        >>> bs = context.newString('Hello world', style)
        >>> t = Text(bs, name='Child', w=100)
        >>> copyE = t.copy() # Copy the element attribute, including the string of self.
        >>> copyE.bs
        $Hello worl...$
        """
        e = Element.copy(self, parent=parent)
        e.bs = deepcopy(self.bs) # Copy the string separately.
        return e

    def append(self, bs, style=None):
        """Appends to the current BabelString instance self.bs.
        """
        if not isinstance(bs, BabelString):
            bs = BabelString(str(bs), style, context=self.context)
        if self.bs is None:
            self.bs = bs
        else:
            self.bs += bs
            self._textLines = None # Force new rendering on self.textLines call.

    def appendMarker(self, markerId, arg=None):
        """Append a marker at the end of the last BabelString.runs[-1].
        This can be used by page composers to see what the status of a certain
        text has become, after rendering textLines.
        """
        self.bs.appendMarker(markerId, arg)

    def getTextSize(self, bs=None, w=None):
        """Figure out what the width and height of the text self.bs is, with or
        given width or the styled width of this text box. If `fs` is defined as
        external attribute, then the size of the string is answers, as if it
        was already inside the text box.


        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> context = getContext('DrawBot')
        >>> doc = Document(context=context)
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = BabelString('ABC', style)
        >>> t = Text(bs, parent=doc[1], w=500)
        >>> t.bs
        $ABC$
        >>> t.bs == bs
        True
        >>> t.context
        <DrawBotContext>
        >>> tw, th = t.getTextSize(bs) # FIXME: Right value?
        >>> tw.rounded, th.rounded
        (182pt, 100pt)
        """
        if bs is None: # If defined, test with other string than inside.
            bs = self.bs
        if bs is None: # Still None? Don't know what to do.
            return 0, 0
        if w is None:
            w = self.w
        return self.context.textSize(bs.cs, w=self.w)

    def getOverflow(self, w=None, h=None):
        """Figures out what the overflow of the text is, with the given (w, h)
        or styled (self.w, self.h) of this text box. If h is None and self.h is
        None then by definintion overflow will allways be empty, as the box is
        elastic."""
        # In case height is undefined, box will always fit the content.
        if self.h is None and h is None:
            return ''

        # Otherwise test if there is overflow of text in the given element
        # size.
        if w is None:
            w = self.pw # Padded width

        if h is None:
            h = self.ph # Padded height

        box = (0, 0, w, h)

        return self.context.textOverflow(self.bs, box, LEFT)

    def _findStyle(self, run):
        """Answers the name and style that desctibes this run best. If there is
        a doc style, then answer that one with its name. Otherwise answer a new
        unique style name and the style dict with its parameters."""
        return self.bs.getStyleAtIndex(0)

    def _get_styledLines(self):
        """Answers the list with (styleName, style, textRun) tuples, reverse
        engineered from the FormattedString `self.bs`. This list can be used to
        query the style parameters used in the textBox, or to create CSS styles
        from its content."""
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
    styledLines = property(_get_styledLines)

    def _get_xTextAlign(self):
        """Answer the type of x-alignment. 
        
        Note that self.xAlign defines the position of the box. If the BabelString is
        used in plain text mode (bs.hasWidth == False), then the behavior of self.xAlign
        and self.xTextAlign is equivalnent.
        If the BabelString has a width defined (bs.hasWidth == True), then the self.xAlign
        defines the alignment of the box and self.xTextAlign defines the alignment of
        the text inside the box.

        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = context.newString('ABCD', dict(xTextAlign=CENTER))
        >>> bs.xTextAlign
        'center'
        >>> bs.xTextAlign = RIGHT
        >>> bs.xTextAlign
        'right'
        >>> bs.xTextAlign == bs.runs[-1].style['xTextAlign']
        True
        """
        return self._validateXAlign(self.bs.xTextAlign)
    def _set_xTextAlign(self, xTextAlign):
        if self._bs is not None:
            self.bs.xTextAlign = self._validateXAlign(xTextAlign) 
    xTextAlign = property(_get_xTextAlign, _set_xTextAlign)

    def _get_yTextAlign(self):
        """Answer the type of y-alignment. 

        Note that self.yAlign defines the position of the box. If the BabelString is
        used in plain text mode (bs.hasHeight == False), then the behavior of self.yAlign
        and self.yTextAlign is equivalnent.
        If the BabelString has a height defined (bs.hasHeight == True), then the self.yAlign
        defines the alignment of the box and self.yTextAlign defines the alignment of
        the text inside the box.

        >>> from pagebot.constants import MIDDLE
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = context.newString('ABCD') # No height defined.
        >>> bs.yTextAlign
        'top'
        >>> bs.yTextAlign = MIDDLE
        >>> bs.yTextAlign
        'middle'
        >>> bs.yTextAlign == bs.runs[-1].style['yTextAlign']
        True
        >>> t = Text(bs)
        >>> t.yTextAlign, t.yAlign
        ('middle', 'bottom')
        """
        return self._validateYAlign(self.bs.yTextAlign)
    def _set_yTextAlign(self, yTextAlign):
        if self._bs is not None:
            self.bs.yTextAlign = self._validateYAlign(yTextAlign) # Save locally, blocking CSS parent scope for this param.
    yTextAlign = property(_get_yTextAlign, _set_yTextAlign)

    #   S P E L L  C H E C K

    WORDS = re.compile('([A-Za-z]*)')

    def _spellCheckWords(self, languages, unknown, minLength):
        """Spellcheck the words of self for the defined list of languages.
        Unknown words are appended to the unknown list.

        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> doc = Document(context=context)
        >>> e = Text('This is an English text', w=1000, h=1000, parent=doc[1])
        >>> e.spellCheck() # All words are default English, no wrong words answered
        []
        >>> e = Text('Thisx is an english textxxx', w=1000, h=1000, parent=doc[1])
        >>> e.spellCheck() # Note that the spell checking is case-sensitive, e.g. English names.
        ['Thisx', 'english', 'textxxx']
        >>> e = Text('This is an English text', parent=doc[1])
        >>> e.spellCheck(languages=['nl'])
        ['This', 'text']
        """
        for word in self.WORDS.findall(self.bs.s):
            for language in languages:
                languageWords = hyphenatedWords(language)
                assert languageWords is not None
                if word and len(word) >= minLength and word not in languageWords and word.lower() not in languageWords:
                    unknown.append(word)
        return unknown

    #   F L O W

    def isOverflow(self, tolerance=0):
        """Answers if this element needs overflow to be solved. This method is
        typically called by conditions such as Overflow2Next or during drawing
        if the overflow marker needs to be drawn.

        NOTE: There is currently not a test if text actually went into the next
        element. It's just checking if there is a name defined, not if it
        exists or is already filled by another flow."""
        return self.nextElement is None and self.getOverflow()

    def overflow2Next(self, processed=None):
        """Try to fix if there is overflow. If there is overflow outside the
        page, then find the page.next with it's target element to continue,
        until all text fits or the element has not nextElement defined.
        Answer the page and result, as the page may have been altered.
        Overflow is solved by element condition Overflow2Next().

        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> doc = Document(w=1000, h=1000)
        >>> page1 = doc[1]
        >>> page1
        <Page #1 default (1000pt, 1000pt)>
        >>> bs = BabelString('AAA ' * 1000, style=dict(font='Roboto', fontSize=pt(20), leading=pt(12)))
        >>> # Fix h to lock elastic height. Overflow is now defined.
        >>> t1 = Text(bs, name="T1", w=100, h=200, nextElement='T2', parent=page1)
        >>> #t1.isOverflow()
        # Overflow shows here
        >>> t1.bs.getStyleAtIndex(0)['font']
        'Roboto'
        >>> t1.bs.getStyleAtIndex(0)['fontSize']
        20pt
        >>> t2 = Text(name="T2", w=100, h=200, nextElement='T1', nextPage=page1.next, parent=page1)
        >>> #len(str(t2.bs))
        #4000
        >>> #len(t1.isOverflow())
        #3744 # FIXME: Flat yields larger overflow
        """
        result = True
        overflow = self.getOverflow()
        page = self.getElementPage()
        nextElement = None
        if processed is None:
            # Keep track of what we did, to avoid circular references.
            processed = set()

        # If there is text overflow and there is a next element?
        if overflow and self.nextElement:

            if self.nextPage: # Try to use element on another page?
                # Try on several types in which the next page can be defined.
                if page is not None and self.nextPage == 'next': # Force to next page, relative to current
                    page = page.next
                elif isinstance(self.nextPage, Element):
                    page = self.nextPage
                elif page is not None and isinstance(self.nextPage, (int, float)): # Offset to next page
                    page = page.parent.pageNumber(page) + self.nextPage
                else: # Try by name
                    page = self.doc.getPage(self.nextPage)
                if page is not None:
                    nextElement =  page.getElementByName(self.nextElement)

            nextElement = page.getElementByName(self.nextElement) # Find element on this page.
            if page is not None and nextElement is None: # Not found any in the regular way?
                # Now try with deepFind
                nextElement = page.parent.deepFind(self.nextElement)

            if nextElement is not None:
                if nextElement.eId in processed:
                    print('### Text.overflow2Next: Element %s already processed' % nextElement)
                else:
                    # Finally found one empty box on this page or next page?
                    processed.add(nextElement.eId)
                    # Prevent indenting of first overflow text in next column,
                    # using a tiny-small space to define the new line style,
                    # with rest of style copied from first character of the overflow string.
                    overflow = overflow.columnStart(self.firstColumnIndent)

                    nextElement.bs = overflow
                    nextElement.prevPage = page # Remember the page we came from, link in both directions.
                    nextElement.prevElement = self.name # Remember the back link
                    page = nextElement.overflow2Next(processed) # Solve any overflow on the next element.
        return overflow

    #   B U I L D

    def build(self, view, origin, drawElements=True, **kwargs):
        """Draws the text on position (x, y). Draw background rectangle and /
        or frame if fill and / or stroke are defined.

        >>> from pagebot.document import Document
        >>> from pagebot.elements import *
        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.units import pt, em
        >>> context = getContext('DrawBot')
        >>> W, H = 500, 400
        >>> doc = Document(w=W, h=H, context=context)
        >>> page = doc[1]
        >>> fontSize = pt(100)
        >>> style = dict(font='PageBot-Regular', fontSize=fontSize, leading=fontSize, textFill=(1, 0, 0), xAlign=CENTER)
        >>> bs = context.newString('Hkpx\\nHkpx', style)
        >>> t = Text(bs, x=W/2, y=H/2, parent=page, showOrigin=True, fill=0.9, yAlign=MIDDLE)
        >>> l = Line(x=t.x-t.w/2, y=t.y, w=t.w, h=0, stroke=(0, 0, 0.5), parent=page)
        >>> l = Line(x=t.x-t.w/2, y=t.y+t.bs.capHeight, w=t.w, h=0, stroke=(0, 0, 0.5), parent=page)
        >>> l = Line(x=t.x-t.w/2, y=t.y+t.bs.ascender, w=t.w, h=0, stroke=(0, 0, 0.5), parent=page)
        >>> l = Line(x=t.x-t.w/2, y=t.y+t.bs.xHeight, w=t.w, h=0, stroke=(0, 0, 0.5), parent=page)
        >>> l = Line(x=t.x-t.w/2, y=t.y+t.bs.descender, w=t.w, h=0, stroke=(0, 0, 0.5), parent=page)
        >>> doc.export('_export/Text-build1.pdf')

        >>> W, H = 700, 100
        >>> doc = Document(w=W, h=H, context=context)
        >>> view = doc.view
        >>> view.showOrigin = True
        >>> view.padding = pt(30)
        >>> view.showCropMarks = True
        >>> view.showFrame = True
        >>> style = dict(font='PageBot-Regular', leading=em(1), fontSize=pt(18), textFill=(0, 0, 0.5), xAlign=CENTER)
        >>> txt = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit valim mecto trambor.'
        >>> bs = context.newString(txt, style) # Creates a BabelString with context reference.
        >>> bs.context is context
        True
        >>> t = Text(bs, x=W/2, y=H/2, parent=doc[1], yAlign=MIDDLE_X)
        >>> t.context is context
        True
        >>> doc.export('_export/Text-build2.pdf')
        """
        context = self.context
        p = pointOffset(self.origin, origin)
        tx, _, _, = p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        context = view.context # Get current context
        self._applyRotation(view, p)

        # TODO: Add Element clipping stuff here

        # Let the view draw frame info for debugging, in case view.showFrame == True.
        view.drawElementFrame(self, p, **kwargs)
        #print('-;f;f;f', self.bs, self.bs.w, self.bs.h, self.bs.tw, self.bs.th)

        if self.bs.hasWidth or self.bs.hasHeight:
            # Forced width and/or height set, behave as a textbox.
            # Draw optional background, frame or borders.
            # Width is padded width of self.
            self.buildFrame(view, (px, py-self.h+self.bs.lines[0].y, self.pw or self.bs.tw, self.bs.th))
            # No size defined, just draw the string with it's own (bs.tw, bs.th)
            # Note that there still can be multiple lines in the the string if
            # it contains '\n' characters.
            context.drawText(self.bs, (tx, py-self.h + self.bs.lines[0].y, self.w or self.bs.w, self.h or self.bs.h))

        else: # No width or height defined.
            # Draw as string using its own width (there may be embedded newlines)
            # Draw optional background, frame or borders.
            #print('......', (px, py-self.bs.th, self.bs.tw, self.bs.th))
            self.buildFrame(view, (px, py+self.bs.th-self.bs.topLineAscender, self.bs.tw, self.bs.th+self.bs.topLineAscender))
            context.drawString(self.bs, (px, py))

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'
        view.drawElementOrigin(self, origin)

    def _drawOverflowMarker_drawBot(self, view, px, py):
        """Draws the optional overflow marker, if text doesn't fit in the box."""
        b = self.b # Get current builder from self.doc.context.b
        bs = self.newString('[+]', style=dict(textFill=color(r=1, g=0, b=0), font='PageBot-Bold', fontSize=10))
        tw, _ = bs.size
        # FIX: Should work work self.bottom
        #b.text(bs.s, upt(self.right - 3 - tw, self.bottom + 3))
        b.text(bs.s, upt(self.right - 3 - tw, self.y + 6))

    def _applyAlignment(self, p):
        """Answers point `p` according to the alignment status in the css
        and alignment of the text."""
        px, py, pz = point3D(p)
        return self._applyHorizontalAlignment(px), self._applyVerticalAlignment(py), pz

    def _applyHorizontalAlignment(self, x):
        # Horizontal alignment is done by the text itself. This is just for other elements,
        # such as the frame.
        xAlign = self.xAlign
        if xAlign == CENTER:
            x -= self.w/2/self.scaleX
        elif xAlign == RIGHT:
            x -= self.w/self.scaleX
        return x

    def _applyVerticalAlignment(self, y):
        # Adjust vertical alignments for the text,
        # assuming that the default origin of drawing in on text baseline.
        yAlign = self.yAlign
        if yAlign == MIDDLE:
            y += self.h/2 - self.bs.topLineAscender

        elif yAlign == CAPHEIGHT:
            y -= self.bs.topLineCapHeight
        elif yAlign == XHEIGHT:
            y -= self.bs.topLineXHeight
        elif yAlign == MIDDLE_CAP:
            y -= self.bs.topLineCapHeight/2
        elif yAlign == MIDDLE_X:
            y -= self.bs.topLineXHeight/2

        elif yAlign == TOP:
            y -= self.bs.topLineAscender
        elif yAlign == ASCENDER: # Position of /h ascender
            y -= self.bs.topLineAscender_h

        elif yAlign == DESCENDER: # Position of /p descender
            y += self.h - self.bs.topLineAscender - self.bs.bottomLineDescender_p + self.bs.bottomLineDescender
        elif yAlign == BOTTOM:
            y += self.h - self.bs.topLineAscender
        elif yAlign == BASE_BOTTOM:
            y += self.h + self.bs.bottomLineDescender - self.bs.topLineAscender

        #else BASELINE, None is default
        return y

    def _get_bottom(self):
        """Bottom position of bounding box, not including margins.

        >>> from pagebot.document import Document
        >>> from pagebot.constants import BOTTOM
        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> doc = Document(size=A4, context=context)
        >>> bs = context.newString('ABCD', dict(fontSize=pt(100)))
        >>> t = Text(bs, x=pt(100), y=pt(500), yTextAlign=BOTTOM, fill=0.8, parent=doc[1])
        >>> t.bottom, t.y
        (500pt, 500pt)
        >>> t.bottom = 300
        >>> t.bottom, t.y # Identical, as aligned on bottom
        (300pt, 300pt)
        """
        if self._bs is None:
            return None
        return self.top - (self.bs.h or self.bs.th)
    def _set_bottom(self, y):
        if self._bs is not None:
            self.top = y + (self.bs.h or self.bs.th)
    bottom = property(_get_bottom, _set_bottom)

    def _get_top(self):
        """Bottom position of bounding box, not including margins.
        This must be different from the regular Element top property,
        as the default origin is at the baseline of the top text line.

        >>> from pagebot.constants import A4, MIDDLE_CAP, TOP
        >>> from pagebot.elements import newLine
        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> doc = Document(size=A4, context=context)
        >>> page = doc[1]
        >>> bs = context.newString('ABCD', dict(fontSize=pt(100)))
        >>> t = Text(bs, parent=page, x=pt(100), y=pt(500), yAlign=TOP, fill=0.8)
        >>> l = newLine(x=0, y=500, w=page.w, h=0, parent=page, stroke=(0, 0, 0.5), strokeWidth=0.5)
        >>> t.top
        500pt
        >>> doc.export('_export/Text-top-500.pdf')
        >>> t.top = 300
        >>> t.top, t.y # Same value, as aligned on top
        (300pt, 300pt)
        >>> l = newLine(x=0, y=300, w=page.w, h=0, parent=page, stroke=(0, 0, 0.5), strokeWidth=0.5)
        >>> doc.export('_export/Text-top-300.pdf')
        >>> t.yTextAlign = MIDDLE_CAP # For Text this is quivalent to t.yAlign
        >>> t.y -= 100
        >>> t.top, t.y # Different now, with other alignment.
        (241.9pt, 200pt)
        >>> l = newLine(x=0, y=200, w=page.w, h=0, parent=page, stroke=(0, 0, 0.5), strokeWidth=0.5)
        >>> doc.export('_export/Text-top-200.pdf')
        """
        return self._applyVerticalAlignment(self.y) + self.bs.topLineAscender
    def _set_top(self, y):
        self.y += y - self.top # Trick to reverse vertical alignment.
    top = property(_get_top, _set_top)

    #   B U I L D  I N D E S I G N

    def build_inds(self, view, origin=None, drawElements=True, **kwargs):
        """It is better to have a separate InDesignContext build tree, because
        we need more information down there than just drawing instructions.
        This way the InDesignContext just gets passed the PageBot Element,
        using it's own API."""
        context = view.context
        p = pointOffset(self.origin, origin)
        p2D = point2D(self._applyAlignment(p)) # Ignore z-axis for now.
        context.textBox(self.bs, p2D, e=self)
        if drawElements:
            for e in self.elements:
                e.build_inds(view, p2D)

    #   B U I L D  H T M L

    def build_html(self, view, origin=None, drawElements=True, **kwargs):
        """Build the HTML code through WebBuilder (or equivalent) that is
        the closest representation of self. If there are any child elements,
        then also included their code, using the level recursive indent."""

        context = view.context # Get current context.
        b = context.b

        if self.bs is not None:
            html = context.fromBabelString(self.bs)
            hasContent = html and html.strip() # Check if there is content, besides white space
        else:
            hasContent = False

        # Use self.cssClass if defined, otherwise self class. #id is ignored if None
        if hasContent:
            b.div(cssClass=self.cssClass or self.__class__.__name__.lower(), cssId=self.cssId)
            b.addHtml(html) # Get HTML from BabelString in HtmlString context.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view)

        if drawElements:
            for e in self.elements:
                e.build_html(view, origin, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view)

        if hasContent:
            b._div() # self.cssClass or self.__class__.__name__



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

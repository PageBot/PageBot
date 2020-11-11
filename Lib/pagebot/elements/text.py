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
#     e.w is defined, it handles a single line of text, unless there are hard
#     coded \n newlines embedded in the string.
#
#     If e.w is defined, the element behaves as a text box; the lines are
#     hyphenated, wrapped and aligned.

import re
from copy import deepcopy

from pagebot.constants import *
from pagebot.contexts.basecontext.babelstring import BabelString
from pagebot.style import makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset, point2D, pt, units, upt
from pagebot.toolbox.color import color
from pagebot.toolbox.hyphenation import hyphenatedWords
from pagebot.elements.textalignments import TextAlignments
from pagebot.elements.textconditions import TextConditions
from pagebot.toolbox.color import noColor

class Text(Element, TextConditions, TextAlignments):
    """PageBot stores text based on the internal BabelString format.

    TODO: reimplement various top baseline alignments.
    TODO: placed upside down compared to other elements, reverse.

    >>> from pagebot.contexts import getContext
    >>> from pagebot.document import Document
    >>> context = getContext()
    >>> doc = Document(w=300, h=400, context=context)
    >>> page = doc[1]
    >>> t = Text('ABCD', parent=page)
    >>> t
    <Text $ABCD$ w=100pt h=400pt>
    """
    isText = True

    # Absolute minimum width of a text box. Avoid endless elastic height.
    TEXT_MIN_WIDTH = 24

    def __init__(self, bs=None, w=None, h=None, size=None, style=None,
            padding=None, xTextAlign=None, xAlign=None, yAlign=None,
            margin=None, top=None, bottom=None, **kwargs):

        # Placeholder, ignoring self.w and self.h until defined.
        self._bs = None

        # Adjust the attributes in **kwargs, so their keys are part of the
        # rootstyle, in order to do automatic conversion with makeStyle()
        Element.__init__(self, **kwargs)
        assert self.context
        """Creates a Text element, holding storage of `self.bs`.
        BabelString instance."""

        # Combines rootStyle, optional self.style and **kwargs attributes. Note
        # that the final style is stored in the BabelString instance self.bs.
        # self.style is used as template, in the content is defined as plain
        # string.
        if style is not None:
            #self.style = makeStyle(style, **kwargs)
            self.style = makeStyle(style)

        # Set as property, to make sure there's always a generic BabelString
        # instance or None. Needs to be done before element initialisation,
        # because some attributes (Text.xTextAlign) may need the string style
        # as reference.
        self.bs = bs # BabelString source for this Text element.

        # TODO: shouldn't BabelString be required?
        #assert self.bs

        # These need the self.bs to be defined.
        if xTextAlign is not None:
            self.xTextAlign = xTextAlign

        if xAlign is not None:
            self.xAlign = xAlign
        if yAlign is not None:
            self.yAlign = yAlign
        else:
            self.yAlign = BOTTOM

        if padding is not None:
            self.padding = padding
        if margin is not None:
            self.margin = margin
        if top is not None:
            self.top = top
        if bottom is not None:
            self.bottom = bottom

        self.w = w
        self.h = h

    def _get_bs(self):
        """Answers the stored formatted BabelString. The value can be None."""
        return self._bs

    def _set_bs(self, bs):
        """Makes sure that this is a formatted BabelString. Otherwise creates
        it from string with the current style.

        FIXME: there is a potential clash in the duplicate usage of fill and
        stroke.

        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30, context=context)
        >>> page = doc[1]
        >>> t = Text(parent=page, w=125, h=12)
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
            # FIXME: take font size if w or h are None?
            bs = BabelString(bs, self.style, w=self.w, h=self.h, context=self.context)
        assert isinstance(bs, BabelString)
        self._bs = bs

    bs = property(_get_bs, _set_bs)

    def _get_firstColumnIndent(self):
        """If False or 0, ignores first line indent of a column on text
        overflow. Otherwise sets it to a certain unit. The text will then be
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
        """DrawBot-compatible indent of text. Equivalent to padding-left `pl`.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, context=context)
        >>> page = doc[1]
        >>> t = Text('ABCD', parent=page)
        >>> t.indent, t.pl, t.bs.indent
        (0pt, 0pt, 0pt)
        >>> t.indent = mm(5)
        >>> t.indent, t.pl, t.bs.indent
        (5mm, 5mm, 5mm)
        >>> t.pl = pt(16)
        >>> t.indent, t.pl, t.bs.indent
        (16pt, 16pt, 16pt)
        """
        if self._bs is not None:
            return self.bs.indent
        return self.css('indent')

    def _set_indent(self, indent):
        indent = units(indent)
        if self._bs:
            self.bs.indent = indent
        self.style['indent'] = indent

    indent = pl = property(_get_indent, _set_indent)

    def _get_tailIndent(self):
        """DrawBot-compatible indent of text. Equivalent to padding-right `pr`.

        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> context = getContext()
        >>> doc = Document(w=300, h=400, context=context)
        >>> page = doc[1]
        >>> t = Text('ABCD', parent=page)
        >>> t.tailIndent, t.pr, t.bs.tailIndent
        (0pt, 0pt, 0pt)
        >>> t.tailIndent = mm(5)
        >>> t.tailIndent, t.pr, t.bs.tailIndent
        (5mm, 5mm, 5mm)
        >>> t.pr = pt(16)
        >>> t.tailIndent, t.pr, t.bs.tailIndent
        (16pt, 16pt, 16pt)
        """
        if self._bs is not None:
            return self.bs.tailIndent
        return self.css('tailIndent')

    def _set_tailIndent(self, tailIndent):
        tailIndent = units(tailIndent)
        if self._bs:
            self.bs.tailIndent = tailIndent
        self.style['tailIndent'] = tailIndent

    tailIndent = pr = property(_get_tailIndent, _set_tailIndent)

    def _get_baselines(self):
        return self.context.getBaselines(self.bs)

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
        >>> context = getContext()
        >>> doc = Document(context=context)
        >>> bs = context.newString('ABCD', style)
        >>> e = Text(bs, parent=doc[1])
        >>> e
        <Text $ABCD$ w=100pt h=1000pt>
        >>> e = Text(bs, x=100, y=100, w=200, parent=doc[1])
        >>> e
        <Text $ABCD$ x=100pt y=100pt w=200pt h=1000pt>

        """
        # FIXME: restore tests.
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

        if self.bs is not None:
            s += ' %s' % self.bs

        if self.x:
            s += ' x=%s' % self.x

        if self.y:
            s += ' y=%s' % self.y

        # Always show width and height if defined.
        if self.w:#bs.hasWidth:
            s += ' w=%s' % self.w

        if self.h:#bs.hasHeight:
            s += ' h=%s' % self.h

        return s+'>'

    def build(self, view, origin=ORIGIN, **kwargs):
        """Draws the text on position (x, y). Draws a background rectangle and
        / or frame if fill and / or stroke are defined.

        >>> from pagebot.document import Document
        >>> from pagebot.elements import *
        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.units import pt, em
        >>> context = getContext()
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
        if not self.bs:
            return

        context = view.context # Get current context

        # Stores scaled x-value first; text is already aligned.
        p = pointOffset(self.origin, origin)
        x, _, _, = self._applyScale(view, p)

        # Determines frame position.
        p = self.getPosition(view, origin)
        px, py, _ = p

        # TODO: Add Element clipping stuff here.
        # FIXME: needs some restructuring, text box width and BabelString width
        # can be different now.

        # Let the view draw frame info for debugging, in case view.showFrame ==
        # True.
        view.drawElementFrame(self, p, **kwargs)
        assert self.w, self.h
        context.fill(self.css('fill', noColor))
        context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        context.rect(px, py, self.w, self.h)
        px1 = px + self.pl
        py1 = py - self.pt
        pw1 = self.w - self.pr
        ph1 = self.h - self.pb
        context.drawText(self.bs, (px1, py1, pw1, ph1))
        self.buildFrame(view, (px, py, self.w, self.h))

        if self.showMargin:
            view.drawMargin(self, (px, py))

        if self.showPadding:
            view.drawPadding(self, (px, py))

        self._restoreRotation(view, p)
        self._restoreScale(view)
        self.drawMeta(view, origin)

    def copy(self, parent=None):
        """Answers a full copy of `self`, where the "unique" fields are set to
        default. Also performs a deep copy on all child elements.

        >>> from pagebot.toolbox.color import blackColor, noColor
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> context = getContext()
        >>> doc = Document(w=300, h=400, context=context)
        >>> page = doc[1]
        >>> style = dict(textFill=blackColor, textStroke=noColor)
        >>> bs = context.newString('Hello world', style)
        >>> t = Text(bs, name='Child', w=100, parent=page)
        >>> copyE = t.copy() # Copy the element attribute, including the string of self.
        >>> copyE.bs
        $Hello worl...$
        """
        e = Element.copy(self, parent=parent)
        e.bs = deepcopy(self.bs) # Copy the string separately.
        return e

    def append(self, bs, style=None):
        """Appends to the current BabelString instance self.bs."""
        if not isinstance(bs, BabelString):
            bs = BabelString(str(bs), style, context=self.context)
        if self.bs is None:
            self.bs = bs
        else:
            self.bs += bs
            self._textLines = None # Force new rendering on self.textLines call.

    def appendMarker(self, markerId, arg=None):
        """Appends a marker at the end of the last BabelString.runs[-1].
        This can be used by page composers to see what the status of a certain
        text has become, after rendering textLines.
        """
        self.bs.appendMarker(markerId, arg)

    def getTextSize(self, bs=None, w=None):
        """Figures out what the width and height of the text self.bs is, with
        a given width or the styled width of this text box. If `fs` is defined
        as external attribute, then the size of the string is answered, as if
        it was already inside the text box.


        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> context = getContext()
        >>> doc = Document(context=context)
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = BabelString('ABC', style, context=context)
        >>> t = Text(bs, parent=doc[1], w=500)
        >>> t.bs
        $ABC$
        >>> t.bs == bs
        True
        >>> tw, th = t.getTextSize(bs) # FIXME: Right value?
        >>> tw.rounded, th.rounded
        (182pt, 100pt)
        """
        if bs is None: # If defined, test with other string than contained self.bs.
            bs = self.bs
        if bs is None: # Still None? Don't know what to do.
            return 0, 0
        if w is None:
            w = self.w # Can still be None
        return self.context.textSize(bs, w=self.w) # Context gets full BabelString bs

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
        """Answers the type of x-alignment for the string.

        NOTE: self.xAlign defines the position of the box. If the BabelString
        is used in plain text mode (bs.hasWidth == False), then the behavior of
        self.xAlign and self.xTextAlign is equivalent.

        If the BabelString has a width defined (bs.hasWidth == True), then the
        self.xAlign defines the alignment of the box and self.xTextAlign
        defines the alignment of the text inside the box.

        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = context.newString('ABCD', dict(xTextAlign=CENTER))
        >>> bs.xAlign, bs.hasWidth
        ('center', False)
        >>> t = Text(bs, context=context)
        >>> # If no width defined, these are identical.
        >>> t.xTextAlign, t.xAlign, t.bs.xAlign
        ('center', 'center', 'center')
        >>> t.xTextAlign = RIGHT
        >>>  # If no width defined, these are identical.
        >>> t.style['xTextAlign'], t.xTextAlign, t.xAlign, t.bs.xAlign
        ('right', 'right', 'right', 'right')
        """
        if self._bs is None:
            self.bs.xAlign = self.css('xTextAlign') or self.css('xAlign', LEFT)
        return self.bs.xAlign

    def _set_xTextAlign(self, xTextAlign):
        self.style['xTextAlign'] = xTextAlign = self._validateXTextAlign(xTextAlign)
        if self._bs is not None:
            self.bs.xAlign = xTextAlign
    xTextAlign = property(_get_xTextAlign, _set_xTextAlign)

    def _get_xAlign(self):
        """Answers the type of x-alignment of the box.

        NOTE: self.xAlign defines the position of the box. If the BabelString
        is used in plain text mode (bs.hasWidth == False), then the behavior of
        self.xAlign and self.xTextAlign is equivalent.

        If the BabelString has a width defined (bs.hasWidth == True), then the
        self.xAlign defines the alignment of the box and self.xTextAlign
        defines the alignment of the text inside the box.

        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> context = getContext()
        >>> doc = Document(w=300, h=400, context=context)
        >>> page = doc[1]
        >>> bs = context.newString('ABCD', dict(xAlign=CENTER))
        >>> t = Text(bs, parent=page)
        >>> bs.xAlign
        'center'
        >>> bs.xAlign = RIGHT
        >>> bs.xAlign
        'right'
        >>> bs.xAlign == bs.runs[-1].style['xAlign']
        True
        """
        if self._bs is not None and not self.bs.hasWidth:
            return self.bs.xAlign
        return self.css('xAlign', LEFT)

    def _set_xAlign(self, xAlign):
        self.style['xAlign'] = xAlign = self._validateXTextAlign(xAlign)
        if self._bs is not None and not self.bs.hasWidth:
            self.style['xTextAlign'] = self.bs.xAlign = xAlign

    xAlign = property(_get_xAlign, _set_xAlign)


    def _get_yAlign(self):
        """Answers the type of y-alignment.

        NOTE: self.yAlign defines the position of the box. If the BabelString
        is used in plain text mode (bs.hasHeight == False), then the behavior
        of self.yAlign and self.yTextAlign is equivalnent.

        If the BabelString has a height defined (bs.hasHeight == True), then
        the self.yAlign defines the alignment of the box and self.yTextAlign
        defines the alignment of the text inside the box.

        >>> from pagebot.constants import MIDDLE
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, context=context)
        >>> page = doc[1]
        >>> bs = context.newString('ABCD') # No height defined.
        >>> bs.yAlign
        'baseline'
        >>> t = Text(bs, yAlign=BOTTOM, parent=page)
        >>> t.yAlign
        'bottom'
        """
        # Behave as string, then yAlign and bs.yTextAlign are equivalent.
        if self._bs is not None and not self.bs.hasHeight:
            return self.bs.yAlign
        return self.css('yAlign', BOTTOM)

    def _set_yAlign(self, yAlign):
        # Save locally, blocking CSS parent scope for this param.
        self.style['yAlign'] = yAlign = self._validateYTextAlign(yAlign)
        if self._bs is not None:
            self.bs.yAlign = yAlign

    yAlign = property(_get_yAlign, _set_yAlign)

    #   S P E L L  C H E C K

    WORDS = re.compile('([A-Za-z]*)')

    def _spellCheckWords(self, languages, unknown, minLength):
        """Spellcheck the words of self for the defined list of languages.
        Unknown words are appended to the unknown list.

        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> context = getContext()
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
        until all text fits or the element has not nextElement defined. Answers
        the page and result, as the page may have been altered.  Overflow is
        solved by element condition Overflow2Next().

        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> doc = Document(w=1000, h=1000, context=context)
        >>> page1 = doc[1]
        >>> page1
        <Page #1 default (1000pt, 1000pt)>
        >>> bs = BabelString('AAA ' * 1000, style=dict(font='Roboto', fontSize=pt(20), leading=pt(12)), context=context)
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
                # Force to next page, relative to current.
                if page is not None and self.nextPage == 'next':
                    page = page.next
                elif isinstance(self.nextPage, Element):
                    page = self.nextPage
                elif page is not None and isinstance(self.nextPage, (int, float)):
                    # Offset to next page.
                    page = page.parent.pageNumber(page) + self.nextPage
                else:
                    # Try by name.
                    page = self.doc.getPage(self.nextPage)
                if page is not None:
                    nextElement =  page.getElementByName(self.nextElement)

            # Find element on this page.
            nextElement = page.getElementByName(self.nextElement)
            # Not found any in the regular way?
            if page is not None and nextElement is None:
                # Now try with deepFind
                nextElement = page.parent.deepFind(self.nextElement)

            if nextElement is not None:
                if nextElement.eId in processed:
                    print('### Text.overflow2Next: Element %s already processed' % nextElement)
                else:
                    # Finally found one empty box on this page or next page?
                    processed.add(nextElement.eId)
                    # Prevent indenting of first overflow text in next column,
                    # using a small space to define the new line style,
                    # with rest of style copied from first character of the
                    # overflow string.
                    overflow = overflow.columnStart(self.firstColumnIndent)

                    nextElement.bs = overflow
                    # Remember the page we came from, link in both directions.
                    nextElement.prevPage = page
                    # Remember the back link.
                    nextElement.prevElement = self.name
                    # Solve any overflow on the next element.
                    page = nextElement.overflow2Next(processed)
        return overflow

    def _drawOverflowMarker_drawBot(self, view, px, py):
        """Draws the optional overflow marker, if text doesn't fit in the box."""
        # Get current builder from self.doc.context.b
        bs = self.newString('[+]', style=dict(textFill=color(r=1, g=0, b=0), font='PageBot-Bold', fontSize=10))
        tw, _ = bs.textSize
        # FIX: Should work work self.bottom
        #self.b.text(bs.s, upt(self.right - 3 - tw, self.bottom + 3))
        self.b.text(bs.s, upt(self.right - 3 - tw, self.y + 6))


    # Disabling these temporarily, needs some testing at element level first.
    '''
    def _applyAlignment(self, p):
        """Answers point `p` according to the alignment status in the css and
        alignment of the text."""
        px, py, pz = point3D(p)
        return self._applyHorizontalAlignment(px), self._applyVerticalAlignment(py), pz

    def _applyHorizontalAlignment(self, x):
        """Horizontal alignment is done by the text itself. This is just for
        other elements, such as the frame."""
        # Horizontal align defined in self.bs should be handled by the context.
        xAlign = self.xAlign
        if xAlign == CENTER:
            x -= self.w/2/self.scaleX
        elif xAlign == RIGHT:
            x -= self.w/self.scaleX
        return x

    def _applyVerticalAlignment(self, y):
        """Adjust vertical alignments for the text, assuming that the default
        origin of drawing is on text baseline."""
        # Vertical alignment if handled by the text element, where the type comes
        # either from self.yAlign or self.bs.yTextAlign
        yAlign = self.yAlign or self.bs.yTextAlign

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
            pass
            #y += self.h - self.bs.topLineAscender
        elif yAlign == BASE_BOTTOM:
            y += self.h + self.bs.bottomLineDescender - self.bs.topLineAscender

        #else BASELINE, None is default
        return y
    '''

    # NOTE: Changed babelstring text() implementation, (mostly) behaves like a
    # regular rectangle.
    '''
    def _get_bottom(self):
        """Bottom position of bounding box, not including margins.

        >>> from pagebot.document import Document
        >>> from pagebot.constants import BOTTOM
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> doc = Document(size=A4, context=context)
        >>> bs = context.newString('ABCD', dict(fontSize=pt(100)))
        >>> t = Text(bs, x=pt(100), y=pt(500), yAlign=BOTTOM, fill=0.8, parent=doc[1])
        >>> #t.bottom, t.y
        #(500pt, 500pt)
        >>> #t.bottom = 300
        >>> #t.bottom, t.y # Identical, as aligned on bottom
        #(300pt, 300pt)
        """

        if self._bs is None:
            return None
        return self.y#self.top - self.h

    def _set_bottom(self, y):
        self.top = y + self.h

    bottom = property(_get_bottom, _set_bottom)

    def _get_top(self):
        """Bottom position of bounding box, not including margins. This has to
        be different from the regular Element top property, because the default
        origin is at the baseline of the top text line.

        """
        return self._applyVerticalAlignment(self.y) + self.bs.topLineAscender
    def _set_top(self, y):
        self.y += y - self.top # Trick to reverse vertical alignment.
    top = property(_get_top, _set_top)

    '''

    '''
    def _set_top(self, y):
        """Shift the element so `self.top == y`. Where the "top" is, depends on
        the setting of `self.yAlign`. If `self.isText`, then vertical position
        can also be defined by the top or bottom position of the baseline.

        TODO: placed upside down compared to other elements, reverse.
        """
        if self.yAlign == MIDDLE:
            self.y = units(y) - self.h/2
        elif self.yAlign == BOTTOM:
            self.y = y
        else: # yAlign must be TOP or None
            self.y = units(y) - self.h

    def _get_top(self):
        """Answers the top position (relative to self.parent) of self.
        >>> e = Element(y=100, h=248, yAlign=TOP)
        >>> e.top
        100pt
        >>> e.yAlign = BOTTOM
        >>> e.top
        348pt
        >>> e.yAlign = MIDDLE
        >>> e.top
        224pt
        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> doc = Document(size=A4, context=context)
        >>> page = doc[1]
        >>> bs = context.newString('ABCD', dict(fontSize=pt(100)))
        >>> t = Text(bs, parent=page, x=pt(100), y=pt(500), yAlign=TOP, fill=0.8)
        >>> t.top
        500pt
        >>> t.y
        500pt
        >>> t.y -= 100
        >>> t.y
        400pt
        """
        if self.yAlign == MIDDLE:
            return self.y + self.h/2
        if self.yAlign == BOTTOM:
            return self.y + self.h

        # yAlign must be TOP or None
        return self.y

    top = property(_get_top, _set_top)
    '''


    #   B U I L D  I N D E S I G N

    def build_inds(self, view, origin=None, **kwargs):
        """It is better to have a separate InDesignContext build tree, because
        we need more information down there than just drawing instructions.
        This way the InDesignContext just gets passed the PageBot Element,
        using it's own API."""
        context = view.context
        p = pointOffset(self.origin, origin)
        p2D = point2D(self._applyAlignment(p)) # Ignore z-axis for now.
        context.textBox(self.bs, p2D, e=self)
        for e in self.elements:
            e.build_inds(view, p2D)

    #   B U I L D  H T M L

    def build_html(self, view, origin=None, **kwargs):
        """Build the HTML code through WebBuilder (or equivalent) that is
        the closest representation of self. If there are any child elements,
        then also included their code, using the level recursive indent."""

        context = view.context # Get current context.
        b = context.b

        if self.bs is not None:
            html = context.fromBabelString(self.bs)
            # Check if there is any content, besides white space.
            hasContent = bool(html and html.strip())
        else:
            hasContent = False

        # Use self.cssClass if defined, otherwise self class. #id is ignored if None
        if hasContent:
            b.div(cssClass=self.cssClass or self.__class__.__name__.lower(), cssId=self.cssId)
            # Get HTML from BabelString in HtmlString context.
            b.addHtml(html)

        for e in self.elements:
            e.build_html(view, origin, **kwargs)

        if hasContent:
            b._div() # self.cssClass or self.__class__.__name__

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

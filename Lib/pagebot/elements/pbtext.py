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
#     text.py
#
#     The Text element is the simplest version of text elements. If no width
#     e.w is defined, it handles single line of text (unless there are hard coded \n
#     newlines embedded in the text.)
#     If e.w is defined, then the element behaves as a text box, where lines are
#     hyphenated, wrapped and alignment by lines.
#
import re
from copy import deepcopy

from pagebot.constants import (LEFT, RIGHT, CENTER, MIDDLE, BOTTOM,
    DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_BASELINE_COLOR,
    DEFAULT_BASELINE_WIDTH, BASE_LINE_BG, BASE_LINE, BASE_INDEX_LEFT,
    BASE_Y_LEFT, BASE_INDEX_RIGHT, BASE_Y_RIGHT)
from pagebot.contexts.basecontext.babelstring import BabelString
from pagebot.style import makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset, point2D, pt, units, uRound, upt
from pagebot.toolbox.color import color, noColor
from pagebot.toolbox.hyphenation import hyphenatedWords

class Text(Element):
    """
    Since PageBot stores text by the internal BabelString format, with
    full control on the position of lines, the rendering as “TextBox”
    if not DrawBot.textbox. The problem with text boxes in general, is
    that they position text from “above the ascender of the top line”,
    without much control on the position of baselines. Larger type in
    the first line will push the whole content of the box down.
    Therefor TextBox.build uses context.textLines() as render engine, 
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
    isTextBox = True

    # Absolute minimum width of a text box. Avoid endless elastic height.
    TEXT_MIN_WIDTH = 24

    def __init__(self, bs=None, w=None, h=None, size=None, style=None, 
            parent=None, padding=None, **kwargs):
        self._bs = None

        Element.__init__(self, parent=parent, padding=padding, **kwargs)
        """Creates a Text element, holding storage of `self.bs`.
        BabelString instance."""

        self._textLines = None # Cache storage of self.textLined property

        # Combine rootStyle, optional self.style and **kwargs attributes.
        # Note that the final style is stored in the BabelString instance
        # self.bs. self.style is used as template, in the content is defined
        # as plain string.
        self.style = makeStyle(style, **kwargs)

        # If self._w is None, behave as Text. Otherwise behave as “TextBox”.
        # This change in behavior makes that we don’t have a separate TextBox class.
        # If self._h is defined, the overflow is detected.
        self._w = self._h = None
        if size is not None:
            w, h = size
        if w is not None:
            self._w = units(w)
        if h is not None:
            self._h = units(h)

        # Set as property, to make sure there's always a generic BabelString
        # instance or None. Needs to be done before element initialize, as
        # some attributes (Text.xAlign) may need the string style as reference.
        self.bs = bs

    def _get_bs(self):
        """Answer the stored formatted BabelString. The value can be None.
        """
        return self._bs
    def _set_bs(self, bs):
        """If not None, make sure that this is a formatted BabelString. 
        Otherwise create it with the current style. Note that there is a potential clash
        in the duplicate usage of fill and stroke.

        >>> from pagebot.document import Document
        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30, context=context)
        >>> page = doc[1]
        >>> t = Text(parent=page, w=125)
        >>> # String converts to DrawBotString.
        >>> t.bs = 'AAA'
        >>> t.bs
        $AAA$
        >>> len(t.textLines) # Make new self._textLines render with context
        1
        >>> t._textLines is not None
        True
        >>> t.bs = context.newString('ABCD')
        >>> t._textLines is None # Setting of BabelString clears textLines cache
        True
        >>> t
        <Text $ABCD$ w=125pt>
        """
        # Source can be None, a string or a BabelString.
        if bs is None:
            bs = ''
        if isinstance(bs, str):
            if self.context is not None:
                bs = self.context.newString(bs, self.style)
            else:
                bs = BabelString(bs, self.style) # Otherwise without context, for now.
        #assert isinstance(bs, BabelString)
        self._textLines = None # Force re-render on self.textLines property call.
        self._bs = bs
    bs = property(_get_bs, _set_bs)

    def clear(self):
        """Clear the current content of the element. Make a new formatted
        string with self.style.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> context = getContext('DrawBot')
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30, context=context)
        >>> style = dict(font='PageBot-Regular', fontSize=pt(12))
        >>> page = doc[1]
        >>> bs = context.newString('ABCD', style)
        >>> tb = Text(bs, parent=page, w=125)
        >>> tb.bs
        $ABCD$
        >>> tb.clear()
        >>> not tb.bs.s
        True
        """
        self.bs = None # Also clear the cached self._textLines

    def _get_w(self): # Width
        """Property for self._w, holding the width of the textbox.

        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> t = Text(parent=page, w=125) # Width forces “TextBox” behavior
        >>> page[t.eId].w
        125pt
        >>> t.w = 150
        >>> t.w, t.w == page[t.eId].w
        (150pt, True)
        """
        # In case of relative units, use this as base.
        if self._w is not None:
            base = dict(base=self.parentW, em=self.em) # In case relative units, use parent as base.
            return units(self._w, base=base)
        if self.bs is not None:
            return self.bs.textSize[0]
        return None
    def _set_w(self, w):
        # If None, then self.w is elastic defined by self.bs height.
        if w is not None:
            w = units(w)
        self._w = w
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
        if self._h is not None:
            base = dict(base=self.parentH, em=self.em) # In case relative units, use parent as base.
            return units(self._h, base=base)
        if self.bs is not None:
            return self.bs.textSize[1]
        return None
    def _set_h(self, h):
        # If None, then self.h is elastic defined by self.bs height.
        if h is not None:
            h = units(h)
        self._h = h
    h = property(_get_h, _set_h)

    def _get_y(self):
        """Answers the `y`-position of self.

        >>> e = Element(y=100, h=400)
        >>> e.x, e.y, e.z
        (0pt, 100pt, 0pt)
        >>> e.y = 200
        >>> e.x, e.y, e.z
        (0pt, 200pt, 0pt)
        >>> child = Element(y='40%', parent=e)
        >>> child.y, child.y.pt # 40% of 400
        (40%, 160)
        >>> e.h = 500
        >>> child.y, child.y.pt # 40% of 500 dynamic calculation
        (40%, 200)
        """
        # Retrieve as Unit instance and adjust attributes to current settings.
        base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
        return units(self.style.get('y'), base=base)
    def _set_y(self, y):
        """Convert to units, if y is not already a Unit instance."""
        self.style['y'] = units(y)
        #self._textLines = None # Force recalculation of y values.
    y = property(_get_y, _set_y)

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

    def _get_textLines(self):
        context = self.context
        assert context is not None
        self._textLines = context.textLines(self.bs)
        return self._textLines
    textLines = property(_get_textLines)

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
        if self._w is not None: # Behave a text box with defined width
            s += ' w=%s' % self._w
        if self._h is not None: # Behave as text box with defined height
            s += ' h=%s' % self._h
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
        if not isintance(bs, BabelString):
            bs = BabelString(str(bs), style, context=self.context)
        if self.bs is None:
            self.bs = bs
        else:
            self.bs += bs   
            self._textLines = None # Force new rendering on self.textLines call. 

    def appendMarker(self, markerId, arg=None):
        """Append a marker at the end of the last BabelString.runs[-1]
        """
        self.bs.appendMarker(markerId, arg)

    def getTextSize(self, bs=None, w=None):
        """Figure out what the width and height of the text self.bs is, with or
        given width or the styled width of this text box. If `fs` is defined as
        external attribute, then the size of the string is answers, as if it
        was already inside the text box.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> context = getContext('DrawBot')
        >>> doc = Document(context=context)
        >>> font = findFont('Roboto-Regular')
        >>> bs = BabelString('ABC', dict(font=font, fontSize=pt(124)))
        >>> t = Text(bs, parent=doc[1], w=100, h=None)
        >>> t.bs
        $ABC$
        >>> t.bs == bs
        True
        >>> t.context
        <DrawBotContext>
        >>> tw, th = t.context.textSize(bs) # FIXME: Right value?
        >>> tw.rounded, th.rounded
        (239pt, 174pt)
        """
        context = self.context
        assert context is not None
        if bs is None: # If defined, test with other string than inside.
            bs = self.bs
        if bs is None: # Still None? Don't know what to do.
            return 0, 0
        if w is None:
            return context.textSize(bs, w=w)
        return context.textSize(bs, w=self.w)

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

    def _get_xAlign(self): 
        """Answer the type of x-alignment. Since the orienation of the box is equivalent to the
        on the alignment of the text, it is stored as self.style, referring to the current run.
        That is why we redefine the default element.xAlign propety.

        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = context.newString('ABCD', dict(xAlign=CENTER))
        >>> bs.xAlign
        'center'
        >>> bs.xAlign = RIGHT
        >>> bs.xAlign
        'right'
        >>> bs.xAlign == bs.runs[-1].style['xAlign']
        True

        """
        return self._validateXAlign(self.bs.xAlign)
    def _set_xAlign(self, xAlign):
        if self._bs is not None:
            self.bs.xAlign = self._validateXAlign(xAlign) # Save locally, blocking CSS parent scope for this param.
    xAlign = property(_get_xAlign, _set_xAlign)

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


    def _drawOverflowMarker_drawBot(self, view, px, py):
        """Draws the optional overflow marker, if text doesn't fit in the box."""
        b = self.b # Get current builder from self.doc.context.b
        bs = self.newString('[+]', style=dict(textFill=color(r=1, g=0, b=0), font='PageBot-Bold', fontSize=10))
        tw, _ = bs.size
        # FIX: Should work work self.bottom
        #b.text(bs.s, upt(self.right - 3 - tw, self.bottom + 3))
        b.text(bs.s, upt(self.right - 3 - tw, self.y + 6))

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

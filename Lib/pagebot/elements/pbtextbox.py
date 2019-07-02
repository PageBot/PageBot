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
#     textbox.py
#
import re
from pagebot.constants import (LEFT, RIGHT, CENTER, MIDDLE,
                            BOTTOM, DEFAULT_WIDTH, DEFAULT_HEIGHT,
                            DEFAULT_BASELINE_COLOR, DEFAULT_BASELINE_WIDTH,
                            BASE_LINE_BG, BASE_LINE, BASE_INDEX_LEFT, BASE_Y_LEFT,
                            BASE_INDEX_RIGHT, BASE_Y_RIGHT)
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset, pt, units, uRound, upt
from pagebot.toolbox.color import color, noColor

class TextBox(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.
    isTextBox = True

    TEXT_MIN_WIDTH = 24 # Absolute minumum with of a text box. Avoid endless elastic height.

    def __init__(self, bs=None, w=None, h=None, size=None, **kwargs):
        Element.__init__(self,  **kwargs)
        """Creates a TextBox element. Default is the storage of `self.s`.
        (DrawBot FormattedString or Flat equivalent), but optional it can also
        be ts (tagged str) if output is mainly through build and HTML/CSS.
        Since both strings cannot be converted lossless one into the other, it
        is safer to keep them both if they are available."""

        self._textLines = None
        self._baselines = None # Force initiaize upon first usage.

        if size is not None:
            w, h = size
        self.w, self.h = w or DEFAULT_WIDTH, h # If h is None, height is elastic size

        self.bs = bs # Set as property, to make sure there's always a context based Babelstring or None

    def _get_bs(self):
        """Answer the stored formatted string. The value can be None.
        """
        return self._bs
    def _set_bs(self, bs):
        """If not None, make sure that this is a formatted string. Otherwise create it with
        the current style. Note that in case there is potential clash in the
        double usage of fill and stroke.

        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> tb = TextBox(parent=page, w=125)
        >>> tb.bs = 'AAA' # String converts to DrawBotString.
        >>> tb.bs, tb.bs.s, tb.bs.__class__.__name__
        (AAA, AAA, 'DrawBotString')
        >>> tb = TextBox('BBB')
        >>> tb.bs

        """
        if bs is not None:
            # Source can be any type: BabelString instance or plain unicode string.
            bs = self.newString(bs, style=self.style)
            #assert bs is not None
        self._bs = bs
    bs = property(_get_bs, _set_bs)

    def clear(self):
        """Clear the current content of the element. Make a new formatted string with self.style.

        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> tb = TextBox('AAA', parent=page, w=125)
        >>> tb.bs
        AAA
        >>> tb.clear()
        >>> tb.bs is None
        True
        """
        self.bs = None

    def _get_w(self): # Width
        """Property for self.w, holding the width of the textbox.

        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> tb = TextBox(parent=page, w=125)
        >>> page[tb.eId].w
        125pt
        >>> tb.w = 150
        >>> tb.w, tb.w == page[tb.eId].w
        (150pt, True)
        """
        base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base.
        return units(self.css('w'), base=base)
    def _set_w(self, w):
        self.style['w'] = units(w or DEFAULT_WIDTH)
        # Note choice for difference in camelCase
        #self._textLines = self._baselines = None # Force reset if being called
    w = property(_get_w, _set_w)

    def _get_h(self):
        """Answers the height of the textBox. If self.style['h'] is None, then answer the
        vertical space that the text needs.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> font = findFont('Roboto-Regular')
        >>> style = dict(font=font.path, fontSize=14)
        >>> tb = TextBox('This is content', parent=page, style=style, w=100, h=220)
        >>> page[tb.eId].h
        220pt
        >>> tb.h = 220
        >>> tb.h, tb.h == page[tb.eId].h
        (220pt, True)
        >>> tb.h = None
        >>> tb.h, tb.style['h'] is None
        (20pt, True)
        """
        if self.style['h'] is None: # Elastic height
            h = units(self.getTextSize(w=self.w)[1])
        else:
            base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
            h = units(self.css('h', 0), base=base)
        return h

    def _set_h(self, h):
        # Overwrite style from here, unless self.style['elasticH'] is True
        if h is not None: # If None, then self.h is elastic defined by content
            h = units(h or DEFAULT_HEIGHT) # Overwrite element local style from here, parent css becomes inaccessable.
        self.style['h'] = h

    h = property(_get_h, _set_h)

    def _get_y(self):
        """Answers the y position of self.

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
        """If False or 0, then ignore first line indent of a column on text overflow.
        Otherwise set to a certain unit. This will cause text being indented by the amount of
        self.firstLineIndent, probably in mid-sentence. This option is likely never necessary,
        implemented just in case.
        """
        return self.css('firstColumnIndent')
    def _set_firstColumnIndent(self, indent):
        self.style['firstColumnIndent'] = units(indent)
    firstColumnIndent = property(_get_firstColumnIndent, _set_firstColumnIndent)

    def _get_firstLineIndent(self):
        """DrawBot-compatible indent of first line of a paragraph.
        """
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
        if self._textLines is None:
            self._textLines = []
            self._baselines = {}

            if self.bs:
                for textLine in self.bs.getTextLines(self.pw, self.ph):
                    #print('---', textLine.y, self.h - textLine.y)
                    textLine.y = units(self.h - textLine.y) # Make postion relative to text box self.
                    self._textLines.append(textLine)
                    self._baselines[upt(textLine.y)] = textLine

        return self._textLines
    textLines = property(_get_textLines)

    def _get_baselines(self):
        if self._baselines is None:
            self.textLines # Initialize both self._textLines and self._baselines
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

        >>> from pagebot.toolbox.color import blackColor, noColor
        >>> style = dict(textFill=blackColor, textStroke=noColor)
        >>> e = TextBox('ABC', style=style)
        >>> e.eId in str(e) # TextBox:236DE32AAC108A45490 (0, 0) ABC'
        True
        >>> e = TextBox('ABC', x=100, y=100, w=200, style=style)
        >>> e.eId in str(e)
        True
        """
        if self.title:
            name = ':'+self.title
        elif self.name:
            name = ':'+self.name
        else: # No naming, show unique self.eId:
            name = ':'+self.eId

        if self.bs is not None and self.bs.s:
            s = ' S(%d)' % len(self.bs)
        else:
            s = ''

        if self.elements:
            elements = ' E(%d)' % len(self.elements)
        else:
            elements = ''
        return '%s%s (%s, %s)%s%s' % (self.__class__.__name__, name, uRound(self.xy), uRound(self.size), s, elements)

    def copy(self, parent=None):
        """Answers a full copy of `self`, where the "unique" fields are set to
        default. Also performs a deep copy on all child elements.

        >>> from pagebot.toolbox.color import blackColor, noColor
        >>> style = dict(textFill=blackColor, textStroke=noColor)
        >>> e = TextBox('Hello world', name='Child', w=100, style=style)
        >>> copyE = e.copy() # Copy the element attribute, including the string of self.
        >>> #copyE.bs # TODO: Needs development and testing
        Hello world
        """
        e = Element.copy(self, parent=parent)
        e.bs = self.bs # Copy the string separately.
        return e

    # BabelString support, answering the structure that holds strings for all
    # builder types.

    def setText(self, bs, style=None):
        """Set the formatted string to `s`, using `style` or `self.style`. The
        `bs` as also be a number, in which case is gets converted into a
        string."""
        if isinstance(bs, (int, float)):
            bs = str(bs)
        if isinstance(bs, str):
            bs = self.newString(bs, e=self, style=style)
        self.bs = bs

    def _get_text(self):
        """Answers the plain text of the current self.bs"""
        return u'%s' % self.bs
    text = property(_get_text)

    def append(self, bs, style=None):
        """Appends to the string type that is defined by the current view /
        builder type. Note that the string is already assumed to be styled or
        can be added as plain string. Don't calculate the overflow here, as
        this is a slow / expensive operation. Also we don't want to calculate
        the textLines / runs for every string appended, as we don't know how
        much more the caller will add. bs._textLines is set to None to force
        recalculation as soon as bs.textLines is called again. If bs is not a
        BabelString instance, then create one, defined by the self.context, and
        based on the style of self."""
        #assert isinstance(bs, (str, self.context.STRING_CLASS))
        #self.bs += self.newString(bs, e=self, style=style)
        if self.bs is None:
            self.bs = bs
        else:
            self.bs += bs
        #self.bs = self.newString(bs, e=self, style=style)

    def appendMarker(self, markerId, arg=None):
        self.bs.appendMarker(markerId, arg)

    def getTextSize(self, bs=None, w=None):
        """Figure out what the width/height of the text self.bs is, with or
        given width or the styled width of this text box. If `fs` is defined as
        external attribute, then the size of the string is answers, as if it
        was already inside the text box.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.name in ('DrawBotContext', 'FlatContext', 'SvgContext')
        True
        """
        """
        TODO: Get these tests or similar to work.
        >>> font = findFont('Roboto-Regular')
        >>> bs = context.newString('ABC', style=dict(font=font.path, fontSize=pt(124)))
        >>> tb = TextBox(bs, w=100, h=None)
        >>> tb.bs
        ABC
        >>> tb.getTextSize()[1]
        436.0
        >>> bs = context.newString('ABC', style=dict(font=font.path, fontSize=pt(24)))
        >>> tb = TextBox(bs, w=100, h=None)
        >>> tb.getTextSize()[1]
        28.0
        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> c = FlatContext()
        >>> bs = c.newString('ABC', style=dict(font=font.path, fontSize=pt(124)))
        >>> tb = TextBox(bs, w=100, h=None)
        >>> tb.getTextSize()[1] # ???
        73.0
        """
        if bs is None:
            bs = self.bs
        if bs is None: # Still None?
            return 0, 0
        if w is None:
            return self.bs.size
        return bs.textSize(w=self.w)

    def getOverflow(self, w=None, h=None):
        """Figure out what the overflow of the text is, with the given (w, h)
        or styled (self.w, self.h) of this text box. If h is None and self.h is
        None then by definintion overflow will allways be empty, as the box is
        elastic."""
        if self.h is None and h is None: # In case height is undefined, box will always fit the content.
            return ''

        # Otherwise test if there is overflow of text in the given element size.
        if w is None:
            w = self.pw # Padded width

        if h is None:
            h = self.ph # Padded height

        return self.bs.textOverflow(w, h, LEFT)

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

    #   S P E L L  C H E C K

    WORDS = re.compile('([A-Za-z]*)')

    def _spellCheckWords(self, languages, unknown, minLength):
        """Spellcheck the words of self for the defined list of languages.
        Unknown words are appended to the unknown list.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> e = TextBox('This is an English text', context=context)
        >>> e.spellCheck()
        []
        >>> e = TextBox('Thisx is an english textxxx', context=context)
        >>> e.spellCheck() # Note that the spell checking is case-sensitive, e.g. English names.
        ['Thisx', 'english', 'textxxx']
        >>> e = TextBox('This is an English text', context=context)
        >>> e.spellCheck(languages=['nl'])
        ['This', 'text']
        """
        from pagebot.toolbox.hyphenation import hyphenatedWords
        for word in self.WORDS.findall(str(self.bs)):
            for language in languages:
                languageWords = hyphenatedWords(language)
                assert languageWords is not None
                if word and len(word) >= minLength and word not in languageWords and word.lower() not in languageWords:
                    unknown.append(word)

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
        Overflow is solved by element condition Overflow2Next()

        >>> from pagebot.document import Document
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> doc = Document(w=1000, h=1000, context=context)
        >>> page1 = doc[1]
        >>> s = context.newString('AAA ' * 1000, style=dict(font='Verdana', fontSize=10, leading=12))
        >>> # Fix h to lock elastic height. Overflow now is defined.
        >>> t1 = TextBox(s, name="T1", w=100, h=200, nextElement='T2', parent=page1)
        >>> t1.bs.getStyleAtIndex(0)['fontSize']
        10pt
        >>> t2 = TextBox(name="T2", w=100, h=200, nextElement='T1', nextPage=page1.next, parent=page1)
        >>> len(str(t1.bs.s))
        4000
        >>> len(t1.getOverflow())
        3744
        """
        result = True
        overflow = self.getOverflow()
        page = self.getElementPage()
        nextElement = None
        if processed is None:
            processed = set() # Keep track of what we did, to avoid circular references.

        if overflow and self.nextElement: # If there is text overflow and there is a next element?

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
                    print('### TextBox.overflow2Next: Element %s already processed' % nextElement)
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
        """Draw the text on position (x, y). Draw background rectangle and/or
        frame if fill and/or stroke are defined."""
        context = view.context # Get current context
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
        self._applyRotation(view, p)

        # Let the view draw frame info for debugging, in case view.showFrame ==
        # True.
        view.drawElementFrame(self, p, **kwargs)

        self.buildFrame(view, p) # Draw optional background, frame or borders.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # self has its own baseline drawing, derived from the text, instance of
        # self.baselineGrid.
        self.drawBaselines(view, px, py, background=True) # In case there is baseline at the back

        # Draw the text with horizontal and vertical alignment.
        if self.bs:
            tw, th = self.bs.size
        else:
            tw, th = 100, 12 # Some value, otherwise fitting will loop.

        xOffset = yOffset = 0
        if self.css('yTextAlign') == MIDDLE:
            yOffset = units(self.h - self.pb - self.pt - th)/2
        elif self.css('yTextAlign') == BOTTOM:
            yOffset = units(self.h - self.pb - self.pt - th)
        if self.css('xTextAlign') == CENTER:
            xOffset = units(self.w - self.pl - self.pr - tw)/2
        elif self.css('xTextAlign') == RIGHT:
            xOffset = units(self.w - self.pl - self.pr - tw)

        textShadow = self.textShadow
        if textShadow:
            context.saveGraphicState()
            context.setShadow(textShadow)

        box = clipPath = None

        # DrawBotContext wants the language and hyphenation set per block when drawing.
        context.language(self.bs.language or 'en')
        context.hyphenation(self.bs.hyphenation or True)
        #print('Set language and hyphenation', self.bs.language, self.bs.hyphenation, self.page.pageNumber)

        if self.clipPath is not None: # Use the elements as clip path:
            clipPath = self.clipPath
            clipPath.translate((px, py))
            context.textBox(self.bs, clipPath=clipPath, align=self.css('xTextAlign'))

        elif clipPath is None:
            if 0 and self.elements: # If there are child elements, then these are used as layout for the clipping path.
                clipPath = self.childClipPath # Construct the clip path, so we don't need to restore translate.
                if clipPath is not None:
                    clipPath.translate((self.pl, self.pb))
                clipPath.translate((self.pl, self.pb))
                context.textBox(self.bs, clipPath=clipPath, align=self.css('xTextAlign'))
            else:
                box = px + self.pl, py + self.pb, self.pw, self.ph
                # One of box or clipPath are now defined.
                context.textBox(self.bs, r=box, align=self.css('xTextAlign'))

        if textShadow:
            context.restoreGraphicState()

        if drawElements:
            # If there are child elements, recursively draw them over the pixel
            # image.
            self.buildChildElements(view, p)

        # self has its own baseline drawing, derived from the text, instace of
        # self.baselineGrid.
        self.drawBaselines(view, px, py, background=False) # In case there is baseline at the front

        if view.showTextOverflowMarker and self.isOverflow():
            # TODO: Make this work for FlatContext too
            self._drawOverflowMarker_drawBot(view, px, py)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'

    def drawBaselines(self, view, px, py, background=False):
        # Let's see if we can draw over them in exactly the same position.

        show = self.showBaselineGrid or view.showBaselineGrid

        c = self.context # Get current context and builder

        # Take baseline color and width if defined in local self. Otherwise use view.css
        baselineColor = self.style.get('baselineColor', view.css('baselineColor', DEFAULT_BASELINE_COLOR))
        baselineWidth = self.style.get('baselineWidth', view.css('baselineWidth', DEFAULT_BASELINE_WIDTH))

        font = self.css('viewMarkerFont')
        fontSize = self.css('baseLineMarkerSize')
        leadingStyle = dict(font=self.css('viewMarkerFont'), fontSize=fontSize, textFill=color(r=1, g=0, b=0))

        c.stroke(baselineColor, baselineWidth)
        prevY = 0
        for textLine in self.textLines:
            y = self.h - textLine.y

            # Line drawing depends on used flag and if we are in background/foreground mode.
            if (background and BASE_LINE_BG in show) or (not background and BASE_LINE in show):
                c.line((px, py+y), (px + self.w, py+y))

            # Only text drawing in foreground mode. Text is exclusive, because of limited
            # available space, only one type of label can be shown at either side.
            if not background:
                if BASE_Y_LEFT in show:
                    yStyleL = dict(font=font, fontSize=fontSize, textFill=baselineColor, xTextAlign=RIGHT)
                    bs = self.newString('%d' % round(self.h - y), style=yStyleL)
                    tw, th = bs.size
                    c.textBox(bs, (px - tw*2 - 3, py + y - th/5, tw*2, th))
                elif BASE_INDEX_LEFT in show:
                    indexStyleL = dict(font=font, fontSize=pt(8), textFill=baselineColor, xTextAlign=RIGHT)
                    bs = self.newString(str(textLine.lineIndex), style=indexStyleL)
                    tw, th = bs.size
                    c.textBox(bs, (px - tw*2 - 3, py + y - th/5, tw*2, th))

                if BASE_Y_RIGHT in show:
                    yStyleR = dict(font=font, fontSize=fontSize, textFill=baselineColor, xTextAlign=LEFT)
                    bs = self.newString('%d' % round(self.h - y), style=yStyleR)
                    tw, th = bs.size
                    c.textBox(bs, (px + self.w + 3, py + y - th/5, tw*2, th))
                elif BASE_INDEX_RIGHT in show:
                    indexStyleR = dict(font=font, fontSize=pt(8), textFill=baselineColor, xTextAlign=LEFT)
                    bs = self.newString(str(textLine.lineIndex), style=indexStyleR)
                    tw, th = bs.size
                    c.textBox(bs, (px + self.w + 3, py + y - th/5, tw*2, th))

                if 0: #view.showTextLeading:
                    leading = round(abs(y - prevY))
                    bs = self.newString('%d' % leading, style=leadingStyle)
                    _, th = bs.size
                    c.textBox(bs, (px + self.w + 3, py + prevY - leading/2 - th/5))
            prevY = y

    def _drawOverflowMarker_drawBot(self, view, px, py):
        """Draw the optional overflow marker, if text doesn't fit in the box."""
        b = self.b # Get current builder from self.doc.context.b
        bs = self.newString('[+]', style=dict(textFill=color(r=1, g=0, b=0), font='Verdana-Bold', fontSize=10))
        tw, _ = bs.size
        # FIX: Should work work self.bottom
        #b.text(bs.s, upt(self.right - 3 - tw, self.bottom + 3))
        b.text(bs.s, upt(self.right - 3 - tw, self.y + 6))


    #   B U I L D  H T M L

    def build_html(self, view, origin=None, drowElements=True, **kwargs):
        """Build the HTML code through WebBuilder (or equivalent) that is
        the closest representation of self. If there are any child elements,
        then also included their code, using the level recursive indent."""

        context = view.context # Get current context.
        b = context.b

        if self.bs is not None:
            html = str(self.bs.s)
            hasContent = html and html.strip() # Check if there is content, besides white space
        else:
            hasContent = False

        # Use self.cssClass if defined, otherwise self class. #id is ignored if None
        if hasContent:
            b.div(cssClass=self.cssClass or self.__class__.__name__.lower(), cssId=self.cssId)
            b.addHtml(html) # Get HTML from BabelString in HtmlString context.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view)

        if drowElements:
            for e in self.elements:
                e.build_html(view, origin, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view)

        if hasContent:
            b._div() # self.cssClass or self.__class__.__name__


    #   C O N D I T I O N S

    def fitFontSize2Right(self):
        """Make the right padding of the parent, without
        moving the left position. Overwriting the default behavior of Element, as we want
        text to be fiting too.

        >>> from pagebot.contexts import getContext
        >>> from pagebot.conditions import *
        >>> context = getContext()
        >>> e = Element(padding=pt(30), w=1000, h=1000, context=context)
        >>> bs = context.newString('Test', style=dict(font='Verdana', fontSize=pt(20)))
        >>> tb = TextBox(bs, parent=e, conditions=(Left2Left(), Fit2Width()))
        >>> result = e.solve()
        >>> tb.w
        940pt
        """
        self.w = self.parent.w - self.parent.pr - self.x
        self.bs = self.context.newString(self.bs.s, style=self.style, w=self.pw)
        return True

    # Shrinking box sizes, conditional testers and movers

    def isShrunkOnTextHeight(self, tolerance=0):
        if self.bs is not None:
            return abs(self.bs.size[1] - self.h) <= tolerance
        return not self.h

    def shrink2TextHeight(self, tolerance=0):
        """Shrink the box vertical to fit the vertical bounding box of the current text.
        This also tests by e.isShrunkOnTextHeight()

        >>> from pagebot.contexts import getContext
        >>> from pagebot.conditions import *
        >>> context = getContext()
        >>> e = Element(padding=pt(30), w=1000, h=1000, context=context)
        >>> bs = context.newString('Test', style=dict(font='Verdana', fontSize=pt(50)))
        >>> tb = TextBox(bs, parent=e, conditions=[Shrink2TextHeight()])
        >>> result = e.solve()
        >>> tb.h
        70pt
        """
        if self.bs is not None:
            self.h = self.bs.size[1]
        else:
            self.h = 0

    def isShrunkOnTextWidth(self, tolerance=0):
        if self.bs is not None:
            return abs(self.bs.size[0] - self.w) <= tolerance
        return not self.w

    def shrink2TextWidth(self, tolerance=0):
        """Shrink the box horizontal to fit the horizontal bounding box of the current text.
        This also tests by e.isShrunkOnTextWidth()

        >>> from pagebot.contexts import getContext
        >>> from pagebot.conditions import *
        >>> context = getContext()
        >>> e = Element(padding=pt(30), w=1000, h=1000, context=context)
        >>> bs = context.newString('Test', style=dict(font='Verdana', fontSize=pt(100)))
        >>> tb = TextBox(bs, parent=e, conditions=[Shrink2TextWidth()])
        >>> result = e.solve()
        >>> round(tb.w)
        202pt
        """
        if self.bs is not None:
            self.w = self.bs.size[0]
        else:
            self.w = 0

     # Text conditional testers and movers

    def getMatchingStyleLine(self, style, index=0):
        """Scan through the lines. Test the first textRun of each line to
        match all of the (font, fontSize, textFill) keys of the style.
        Then answer the line. Otherwise answer None.

        Note that this should be extended to scanning all textRuns,
        as by conicidence there van be a "Bold" style inside main text
        at the start of a line.
        Also it should be testing on cascading values (what is defined
        in the style?) instead of testing on all 3 parameters.
        Also testing on line parameters, such as leading.
        """
        matchingIndex = 0
        for line in self.textLines:
            if not line.textRuns:
                continue
            textRun = line.textRuns[0]
            # If this textRun is matching style, then increment the matchIndex.
            # Answer the line if the index matches.
            if  textRun.font == style.get('font', None) and\
                upt(textRun.fontSize) == upt(style.get('fontSize', 0)) and\
                textRun.textFill == style.get('textFill', noColor):
                # Here there was a match.
                if matchingIndex == index:
                    return line
                matchingIndex += 1
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

        >>> from pagebot.contexts import getContext
        >>> from pagebot.conditions import *
        >>> context = getContext()
        >>> e = Element(padding=pt(30), w=1000, h=1000, context=context)
        >>> e.baselineGrid = pt(24)
        >>> e.baselineStart = pt(44)
        >>> bs = context.newString('Test', style=dict(font='Verdana', fontSize=pt(150)))
        >>> tb = TextBox(bs, parent=e)
        >>> tb.baseline2Grid()
        >>> #tb.y

        >>> result = tb.solve()
        >>> #tb.y

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

        >>> from pagebot.contexts import getContext
        >>> from pagebot.conditions import *
        >>> from pagebot.constants import *
        >>> context = getContext()
        >>> e = Element(padding=100, w=1000, h=1000, context=context)
        >>> bs = context.newString('Test', style=dict(font='Verdana', fontSize=pt(150)))
        >>> tb = TextBox(bs, parent=e, yAlign=TOP, conditions=[Shrink2TextBounds(), Top2Top()])
        >>> result = tb.solve()
        """
        """
        TODO: fix doctest; py3.6 / py3.7 rounding difference?
        >>> tb.y, tb.baselineY
        (900pt, 1079pt)

        Travis
        (900pt, 1065pt)
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
        """Move the vertical position of the indexed line to match the positon of self.parent.bottom.
        """
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
        """Move the text box up (decreasing line.y value, rounding in down direction) in vertical direction,
        so the baseline of self.textLines[index] matches the parent grid.
        """
        if self.textLines and parent is not None:
            assert index in range(len(self.textLines)), \
                ('%s.capHeightUp2Grid: Index "%d" is not in range of available textLines "%d"' % \
                (self.__class__.__name__, index, len(self.textLines)))
            line = self.textLines[index]
            if line.textRuns:
                textRun = line.textRuns[0]
                self.top += parent.getDistance2Grid(line.y + textRun.capHeight) + parent.baselineGrid

    def capHeightDown2Grid(self, index=0, parent=None):
        """Move the text box down in vertical direction, so the baseline of self.textLines[index]
        matches the parent grid.
        """
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
        # TODO:Implement
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
        #TODO:Implement
        pass

    def ascender2Top(self, index=None, parent=None):
        # Move the element, so ascender height of index-line is at top of parent."""
        #TODO:Implement
        pass

    def ascender2Bottom(self, index=None, parent=None):
        # Move the element, so ascender height of index-line is at bottom of parent."""
        #TODO:Implement
        pass

    # Descender conditional testers and movers

    def descender2Grid(self, index=None, parent=None):
        # Move the element, so descender of index-line is on grid of parent."""
        #TODO:Implement
        pass

    def descender2Top(self, index=None, parent=None):
        # Move the element, so descender of index-line is on top of parent."""
        #TODO:Implement
        pass

    def descender2Bottom(self, index=None, parent=None):
        # Move the element, so descender of index-line is on bottom of parent."""
        #TODO:Implement
        pass


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

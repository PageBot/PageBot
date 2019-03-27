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
#     htmlstring.py
#
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css
from pagebot.constants import LEFT, DEFAULT_LANGUAGE
from pagebot.toolbox.units import upt
from pagebot.constants import XXXL

class HtmlString(BabelString):

    BABEL_STRING_TYPE = 'html'

    """HtmlString is a wrapper around an HTML tagged string."""
    def __init__(self, s, context, language=None, style=None):
        self.context = context # Store the context, in case we need it.
        self.s = s # Enclose the HTML string
        if style is None:
            style = {}
        self.style = style
        self.language = language or DEFAULT_LANGUAGE
        super().__init__(s, context, style=style)

    def _get_font(self):
        """Answers the current state of fontName."""
        return self.style.get('font') or self.context.getFont()
    def _set_font(self, fontName):
        if fontName is not None:
            self.context.font(fontName)
        self.style['font'] = fontName
    font = property(_get_font, _set_font)

    def _get_fontSize(self):
        """Answers the current state of the fontSize."""
        return self.style.get('fontSize') or self.context.getFontSize()
    def _set_fontSize(self, fontSize):
        if fontSize is not None:
            self.context.fontSize(fontSize)
        self.style['fontSize'] = fontSize
    fontSize = property(_get_fontSize, _set_fontSize)

    def _get_s(self):
        """Answers the embedded HTML string by property, to enforce checking type of the string."""
        return self._s
    def _set_s(self, html):
        # TODO: Test later if html is the right type
        #assert isinstance(html, str)
        self._s = html
    s = property(_get_s, _set_s)

    def asText(self):
        return self.s # TODO: Use re to find non-tagged text to return.

    def textSize(self, w=None, h=None):
        """Answers the (w, h) size for a given width, with the current text.
        For html this probably won't be an accurate guess. Let's think about something else."""
        return len(self.s)*10, 12

    def textOverflow(self, w, h, align=LEFT):
        """How to decide if there is HTML text overflow? Useful to do?"""
        # TODO: Some stuff needs to get here.
        return ''

    def getTextLines(self, w, h=None, align=LEFT):
        u"""Answers the dictionary of TextLine instances. Key is y position of the line.

        >>> from pagebot.toolbox.units import mm, uRound, pt
        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> context = HtmlContext()
        >>> style = dict(font='Verdana', fontSize=pt(12))
        >>> bs = context.newString('Example Text ' * 10, style=style)
        >>> lines = bs.getTextLines(w=200)
        >>> #FIX en(lines)
        0
        >>> #FIX line = lines[0]
        >>> #FIX line.maximumLineHeight
        1.4em
        >>>
        """
        assert w
        if not h:
            h = XXXL
        wpt, hpt = upt(w, h)
        textLines = []
        return textLines

    def append(self, sOrBs):
        if hasattr(sOrBs, 's'):
            sOrBs = sOrBs.s
        self.s += sOrBs

    def getStyleAtIndex(self, index):
        """Answer the constructed style of the string a position index of chars.
        TODO: Try to find CSS status?
        """
        return {}

    MARKER_PATTERN = '<!-- ==%s@%s== -->'

    def appendMarker(self, markerId, arg):
        """Append a comment string with markerId that can be used as non-display marker.
        This way the Composer can find the position of markers in text boxes.

        """
        marker = self.MARKER_PATTERN % (markerId, arg or '')
        self.append(marker)

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, fontSize=None, styleName=None,
            pixelFit=None, tagName=None):
        """Answers a FlatString instance from valid attributes in *style*. Set all values after testing
        their existence, so they can inherit from previous style formats.
        If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*."""

        sUpperCase = css('uppercase', e, style)
        sLowercase = css('lowercase', e, style)
        sCapitalized = css('capitalized', e, style)
        if sUpperCase:
            s = s.upper()
        elif sLowercase:
            s = s.lower()
        elif sCapitalized:
            s = s.capitalize()

        return cls(s, context)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])


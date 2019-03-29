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
#     stacked.py
#
from random import choice
from pagebot.elements.variablefonts.basefontshow import BaseFontShow
from pagebot.constants import JUSTIFIED, LEFT
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.toolbox.units import pointOffset

class Stacked(BaseFontShow):
    """Showing the specified (variable) font as full page with a matrix
    of all glyphs in the font.

    Usage of standard style parameters
    fill        Fill color for the background of the element
    stroke      Draw frame around the element
    textFill    Color of the text. Default is black.
    padding     Use in case of background color or frame. Default is 0

    """
    def __init__(self, f, words=None, labelFontSize=None, **kwargs):
        """
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> from pagebot.toolbox.units import em
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> conditions = [Fit()]
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF')
        >>> style = dict(gh=16, fill=0.95, leading=em(1.4))
        >>> gs = Stacked(font1, parent=page, conditions=conditions, padding=40, style=style, context=c)
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> #font2 = findFont('Upgrade-Regular')
        >>> #font2 = findFont('Escrow-Bold')
        >>> style = dict(stroke=0, strokeWidth=0.25, gh=8, leading=em(1.4))
        >>> gs = Stacked(font2, parent=page, conditions=conditions, style=style, padding=40, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sStacked.pdf' % font1.info.familyName)
        """
        BaseFontShow.__init__(self, **kwargs)
        self.f = f # Font instance
        self.words = words or {} # Optional dictionary for headline words. Keys is frame index number.
        self.usedText = set() # Avoid double use of headline words.
        # Add semi-random generated content, styles of fitting.
        self.blurb = Blurb() # Random content creator, in case there is no content supplied.
        self.lineTag = 'design_headline' # Default label where to find random word choices.
        self.headlineTag = 'design_headline' # Default label where to find (or create) random headline text.
        self.textTag = 'da_text' # Default label where to find (or create) random body text.

    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        c = self.context
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional background fill, frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        view.drawElementFrame(self, p)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # Draw that actual content of the element by stacked specimen rectangles.
        self.drawStacked(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def getText(self, tag, cnt=None, charCnt=None):
        """If the tag type of text is in self.words, then take a random choice from there.
        Otherwise use the tag to create a blurb with the specified length."""
        if tag in self.words:
            text = choice(self.words[tag])
            if text in self.usedText: # Already used, try once more.
                text = choice(self.words[tag])
        else:
            text = self.blurb.getBlurb(tag, cnt=cnt, charCnt=charCnt)
        self.usedText.add(text)
        return text

    def drawStacked(self, view, origin, **kwargs):
        """Draw the content of the element, responding to size, styles, font and content."""

        c = self.context

        # Start on top left, with respect to optional padding value.
        x = self.pl
        y = self.h-self.pt

        # Top headline. (x,y) is top-left of the box, passed on for the position of the next box.
        s = self.getText(self.lineTag, charCnt=10).upper()
        x, y = self.buildStackedLine(s, origin, x, y, self.pw, wght=0.7, wdth=-0.4)

        # Second headline
        s = self.getText(self.lineTag, 4, 18)
        x, y = self.buildStackedLine(s, origin, x, y, self.pw, wght=-0.7)

        # Some large headline thing
        s = self.getText(self.lineTag, 5, 24)
        x, y = self.buildStackedLine(s, origin, x, y, self.pw, wght=0.3, wdth=-0.4)

        # Body text 16/24
        s = self.getText(self.textTag, 20)
        x, y = self.buildTextBox(None, s, origin, x, y, self.pw, None, 16, JUSTIFIED)

        # Body text 12/18
        s = self.getText(self.textTag, 30)
        x, y = self.buildTextBox(None, s, origin, x, y, self.pw, None, 12, JUSTIFIED)

        # Body text 10/15
        s1 = self.getText(self.headlineTag)
        s2 = self.getText(self.textTag, cnt=20)
        x, y = self.buildTextBox(s1, s2, origin, x, y, self.pw, None, 10, JUSTIFIED, Bwght=0.7, Bwdth=-0.1)

        # Body text 9/13.5
        # Don't update to the new y, next colomn needs to be on the right, starting at the same y.
        s1 = self.getText(self.headlineTag)
        s2 = self.getText(self.textTag) + ' ' + self.getText(self.textTag)
        x, _ = self.buildTextBox(s1, s2, origin, x, y, (self.pw-self.gw)/2, y-self.pb,
            9, LEFT, labelSize=7, Bwght=0.6, Bwdth=-0.1)

        # Body text 8/12
        s1 = self.getText(self.headlineTag)
        s2 = self.getText(self.textTag) + ' ' + self.getText(self.textTag)
        x, y = self.buildTextBox(s1, s2, origin, x+(self.pw+self.gw)/2, y, (self.pw-self.gw)/2, y-self.pb,
            8, LEFT, labelSize=7, Bwght=0.6, Bwdth=-0.1)



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

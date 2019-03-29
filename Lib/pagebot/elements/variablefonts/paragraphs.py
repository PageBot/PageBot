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
#     paragraphs.py
#
from random import choice
from pagebot.elements.variablefonts.basefontshow import BaseFontShow
from pagebot.constants import LEFT
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.toolbox.units import pointOffset

class Paragraphs(BaseFontShow): 
    """Showing the specified (variable) font as full page with a matrix
    of all glyphs in the font.

    Usage of standard style parameters
    fill        Fill color for the background of the element
    stroke      Draw frame around the element
    textFill    Color of the text. Default is black.
    padding     Use in case of background color or frame. Default is 0

    """
    def __init__(self, f, words=None, labelSize=None, **kwargs):
        """   
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> from pagebot.toolbox.color import color
        >>> from pagebot.toolbox.units import em
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> style = dict(gh=16, fill=color(0.95), leading=em(1.4))
        >>> conditions = [Fit()]
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF')
        >>> gs = Paragraphs(font1, parent=page, conditions=conditions, padding=40, style=style, context=c)
        >>> style = dict(stroke=0, strokeWidth=0.25, gh=8, leading=em(1.4))
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> #font2 = findFont('Upgrade-Regular')
        >>> #font2 = findFont('Escrow-Bold')
        >>> gs = Paragraphs(font2, parent=page, conditions=conditions, style=style, padding=40, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sParagraphs.pdf' % font1.info.familyName)
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
        self.labelSize = labelSize # If undefined, then don't draw labels.

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
        """Draw the content of the element, responding to size, styles, font and content.
        Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
        if the axis exists.

        TODO: If the axis does not exist, do something else with the right column
        """

        c = self.context

        # Start on top left, with respect to optional padding value.
        x = self.pl
        y = self.h-self.pt

        fontSizes = (7, 8, 9, 10, 11)
        for fontSize in fontSizes:
            # Don't update to the new y, next colomn needs to be on the right, starting at the same y.
            s1 = self.getText(self.headlineTag, cnt=6)
            if not s1[-1] in ',.!?':
                s1 += '.'
            s2 = self.getText(self.textTag) + ' ' + self.getText(self.textTag)
            x, _ = self.buildTextBox(s1, s2, origin, x, y, 
                w=(self.pw-self.gw)/2, h=self.ph/len(fontSizes)-self.gh, 
                fontSize=fontSize, alignment=LEFT, labelSize=self.labelSize or self.DEFAULT_LABEL_SIZE, 
                Bwght=0.4, Bwdth=-0.1)       

            # Same text in same fontSize, without optical size axis used
            _, y = self.buildTextBox(s1, s2, origin, x+(self.pw+self.gw)/2, y, 
                w=(self.pw-self.gw)/2, h=self.ph/len(fontSizes)-self.gh, 
                fontSize=fontSize, alignment=LEFT, labelSize=self.labelSize or self.DEFAULT_LABEL_SIZE, 
                label='No optical size axis used.\n\n', Bwght=0.6, Bwdth=-0.1, useOpsz=False)        



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

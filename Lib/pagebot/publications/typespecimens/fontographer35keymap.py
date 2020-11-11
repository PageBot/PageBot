#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     Build a type specimen similar as, and tribute to, the good old
#     Fontographer 3.5 KeyMap page.
#
#     TODO
#     Make number of GlyphSquares on a page (8x8) dependent on page size.
#     Make font size options (also needs resonsive layout)
#     Optional other layout, use of color and adaption to foundry identity.
#     Optional placement of foundry logo instead of the "Key map"
#     Extending functions for showing additional information per glyph, such
#     as Variable axis location in design space, changed from latest git,
#     Option using this layout with UFO.
#

from pagebot.toolbox.units import pointOffset, inch, pt, em
from pagebot.constants import A4, ONLINE, CENTER, XXXL, ORIGIN
from pagebot.toolbox.color import color, whiteColor, blackColor,  noColor
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.dating import now

from pagebot.publications.typespecimens.basetypespecimen import BaseTypeSpecimen
from pagebot.elements import *
from pagebot.conditions import *

W, H = A4
SQUARES = 8*8
PADDING = 36, 42, 60, 56 # Padding page "margins"
SQSIZE = pt(36) # Standard size of the Fontographer grid glyph squares
SQMR = 14 # Margins to position element identical to origina layout.
SQMB = 46
SQML = 12
MAX_PAGES = XXXL # For debugging, set to the amount of pages to export
SHADOW = pt(2) # Thicknes of "shadow" lines in header.

class GlyphSquare(Element):
    """The GlyphSquare element is the self-contained infographic showing each
    glyph in the original Fontographer 3.5 style. Element float towards a
    position on the page, defined by conditions. When page.solve() is executed,
    the elements find their positions, comparable to the CSS float
    parameters."""

    def __init__(self, glyph, uCode, **kwargs):
        Element.__init__(self,  **kwargs)
        assert glyph, glyph.font
        self.glyph = glyph # Glyph object. Can be used for additional information later.
        self.uCode = uCode # Unicode from cmap

    def build(self, view, origin=ORIGIN, **kwargs):
        """Draw the text on position (x, y). Draw background rectangle and/or
        frame if fill and/or stroke are defined."""
        f = findFont('PageBot-Regular')
        labelFont = findFont('Roboto-Regular') # Keep this as label font (or change it)
        # Make the styles for the strings on the page.
        labelStyle = dict(font=labelFont, fontSize=pt(6), textFill=0, xTextAlign=CENTER)
        glyphStyle = dict(font=f, fontSize=SQSIZE, textFill=0)
        # Get the page position, depending on the floated origin of the element.
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
        # Use the standard frame drawing of Element, using the border settings of self.
        self.buildFrame(view, p) # Draw optional frame or borders.
        # Calculate the scaled width for self.glyph, depending on the em-square
        # of fonts.

        #print(self.glyph.font)
        #w = self.glyph.width
        # FIXME
        return
        width = w /f.info.unitsPerEm * SQSIZE
        # Draw the vertical width line. Not dashed for now.
        self.context.fill(None)
        self.context.stroke(color(1, 0, 0), w=0.5)
        self.context.line((px+width, py), (px+width, py+SQSIZE))
        # Calculate the position of the baseline of the glyph in the square,
        # using font.info.descender from bottom of the square.
        baseline = py - f.info.descender/f.info.unitsPerEm * SQSIZE
        # Create the string in size SQSIZE showing the glyph.
        t = self.context.newString(chr(self.uCode), style=glyphStyle)
        # Set stroke color and stroke width for baseline and draw it.
        self.context.stroke(color(0, 0, 0.5), w=0.5)
        self.context.line((px, baseline), (px+SQSIZE, baseline))
        # Draw the glyph.
        self.context.text(t, (px, baseline))
        # Construct the label from the original glyph, unicode and glyph name
        # (if available)
        label = self.context.newString('%s (%d) %s' % (chr(self.uCode),
            self.uCode, self.glyph.name), style=labelStyle)
        # Get the size of the generated formatted string to center it.
        # Draw the label.
        tw,th = label.size
        self.context.text(label, (px + SQSIZE/2 - tw/2, py-pt(7)))
        # Construct the rotated width string on left and right side.
        widthLabel = self.context.newString('Width: %d' % self.glyph.width,
            style=labelStyle)
        leftLabel = self.context.newString('Offset: %d' % self.glyph.leftMargin,
            style=labelStyle)
        self.context.save() # Save the graphics state
        # Translate the origin to the current position of self, so we can rotate.
        self.context.translate(px, py)
        self.context.rotate(90) # Rotate clockwise vertical
        self.context.text(widthLabel, (0, -SQSIZE-pt(7))) # Draw labels on these positions
        self.context.text(leftLabel, (0, pt(3)))
        self.context.restore() # Restore the graphics state
        self._restoreScale(view)

class Fontographer35KeyMap(BaseTypeSpecimen):
    """

    >>> specimen = Fontographer35KeyMap(w=500, h=1000, autoPages=1)
    >>> doc = specimen.newSampleDocument(name='fontographer 35 keymap')
    >>> page = doc[1]
    >>> score = page.solve()
    >>> doc.export('_export/fontographer35keymap.pdf')

    """
    # Standard page size for now.
    # Substitute the name or file name of the font to show if locally installed.
    # In this example we use the font that come with PageBot.

    def newSampleDocument(self, autoPages=None, **kwargs):
        f = findFont('PageBot-Regular')
        doc = self.newDocument(autoPages=autoPages or 1, **kwargs)
        context = doc.context
        self.makePages(doc, f)
        return doc

    def makeHeader(self, doc, page, font):
        labelFont = findFont('Roboto-Regular') # Keep this as label font (or change it)
        page.padding = PADDING
        header = newRect(h=inch(1), padding=pt(8), mb=inch(0.6), parent=page,
            fill=0.4, conditions=[Fit2Width(), Top2Top()])
        titleStyle = dict(font=labelFont, fontSize=pt(20), textFill=0, xTextAlign=CENTER)
        title = doc.context.newString('Key map', style=titleStyle)
        mr = pt(8)
        newText(title, w=page.pw*0.35, fill=0.5, parent=header,
            pt=pt(12), # Padding top
            mr=mr, # Margin right of the "Key map" text box element
            borderTop=dict(stroke=whiteColor, strokeWidth=SHADOW),
            borderLeft=dict(stroke=whiteColor, strokeWidth=SHADOW),
            borderRight=dict(stroke=blackColor, strokeWidth=SHADOW),
            borderBottom=dict(stroke=blackColor, strokeWidth=SHADOW),
            conditions=[Left2Left(), Fit2Height()])
        t = 'Size: %s  Font: %s\nNotice: © %s\nPrinted by PageBot on %s' % \
            (pt(SQSIZE), font.path.split('/')[-1], font.info.copyright, now().datetime)

        fontInfoStyle = dict(font=labelFont, fontSize=pt(10), leading=em(1.2),
            textFill=blackColor)
        fontInfo = doc.context.newString(t, style=fontInfoStyle)
        newText(fontInfo, fill=1, parent=header, margin=0, w=page.pw*0.65-3*mr,
            padding=pt(4),
            borderTop=dict(stroke=blackColor, strokeWidth=SHADOW),
            borderLeft=dict(stroke=blackColor, strokeWidth=SHADOW),
            conditions=[Right2Right(), Top2Top(), Fit2Height()]
        )
        page.solve()

    def addGlyphSquare(self, doc, page, font, uCode, glyphName):
        squareIndex = 0

        if uCode < 32: # Skip control characters
            return
        if squareIndex >= SQUARES:
            if len(doc) >= (MAX_PAGES or XXXL):
                return
            squareIndex = 0
            page = doc.newPage()
            self.makeHeader(doc, page, font)

        squareIndex += 1
        glyph = font[glyphName]

        if glyph is None or not glyph:
            return

        # Creates an element for this glyph. Note the conditions that will
        # later be checked for the position status by
        # doc.solve()-->page.solve()
        GlyphSquare(glyph, uCode, name='square-%s' % glyphName, w=SQSIZE, h=SQSIZE,
            ml=SQML, mr=SQMR, mb=SQMB,
            borders=dict(strokeWidth=pt(0.5), line=ONLINE, stroke=0, dash=(1,1)),
            parent=page, fill=color(0.95, a=0.8), stroke=noColor,
            conditions=[Right2Right(), Float2Top(), Float2Left()],
        )

    def makePages(self, doc, font):
        u"""Create the elements (header and a grid of GlyphSquares) for each page.
        Add as many pages as needed to accommodate all glyphs in the font.
        """
        page = doc[1]
        self.makeHeader(doc, page, font)

        # Keep track on the amount of squares on the page, checking currently
        # agains the fixed value of SQUARES (8x8 in the original Fontographer
        # layout) TODO: Make this responsive to the size of the page.
        squareIndex = 0
        for uCode, glyphName in sorted(font.cmap.items()):
            self.addGlyphSquare(doc, page, font, uCode, glyphName)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

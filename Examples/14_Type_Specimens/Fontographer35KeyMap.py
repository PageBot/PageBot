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

from pagebot.toolbox.units import pointOffset, inch, pt, upt, em
from pagebot.elements import *
from pagebot.constants import A4, ONLINE, CENTER, XXXL
from pagebot.document import Document
from pagebot.conditions import *
from pagebot.toolbox.color import color, whiteColor, blackColor,  noColor
from pagebot.fonttoolbox.objects.font import findFont, findFonts
from pagebot.toolbox.dating import now
from pagebot import getContext
context = getContext()

# Standard page size for now.
W, H = A4
SQUARES = 8*8
PADDING = 36, 42, 60, 56 # Padding page "margins"
SQSIZE = pt(36) # Standard size of the Fontographer grid glyph squares
SQMR = 14 # Margins to position element identical to origina layout.
SQMB = 46
SQML = 12
MAX_PAGES = XXXL # For debugging, set to the amount of pages to export
SHADOW = pt(2) # Thicknes of "shadow" lines in header.

# Substitute the name or file name of the font to show if locally installed.
# In this example we use the font that come with PageBot.
f = findFont('Bungee-Regular')
labelFont = findFont('Roboto-Regular') # Keep this as label font (or change it)
# Make the styles for the strings on the page.
labelStyle = dict(font=labelFont, fontSize=pt(6), textFill=0, xTextAlign=CENTER)
glyphStyle = dict(font=f, fontSize=SQSIZE, textFill=0)
titleStyle = dict(font=labelFont, fontSize=pt(20), textFill=0, xTextAlign=CENTER) 
fontInfoStyle = dict(font=labelFont, fontSize=pt(10), leading=em(1.2), 
    textFill=blackColor)

# The GlyphSquare element is the self-contained "info-graphic" showing each glyph
# in the original Fontographer 3.5 style.
# Element float towards a position on the page, defined by conditions.
# When page.solve() is executed, the elements find their positions,
# comparable to the CSS float parameters.
class GlyphSquare(Element):
    def __init__(self, glyph, uCode, **kwargs):
        Element.__init__(self,  **kwargs)
        self.glyph = glyph # Glyph object. Can be used for additional information later.
        self.uCode = uCode # Unicode from cmap
         
    def build(self, view, origin, drawElements=True, **kwargs):
        """Draw the text on position (x, y). Draw background rectangle and/or
        frame if fill and/or stroke are defined."""
        context = view.context # Get current context
        b = context.b
        # Get the page position, depending on the floated origin of the element.
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
        # Use the standard frame drawing of Element, using the border settings of self.
        self.buildFrame(view, p) # Draw optional frame or borders.
        # Calculate the scaled width for self.glyph, depending on the em-square 
        # of fonts.
        width = self.glyph.width/f.info.unitsPerEm * SQSIZE
        # Draw the vertical width line. Not dashed for now.
        context.fill(None)
        context.stroke(color(1, 0, 0), w=0.5)
        context.line((px+width, py), (px+width, py+SQSIZE))
        # Calculate the position of the baseline of the glyph in the square, 
        # using font.info.descender from bottom of the square.
        baseline = py - f.info.descender/f.info.unitsPerEm * SQSIZE
        # Create the string in size SQSIZE showing the glyph.
        t = context.newString(chr(self.uCode), style=glyphStyle)
        # Set stroke color and stroke width for baseline and draw it.
        context.stroke(color(0, 0, 0.5), w=0.5)
        context.line((px, baseline), (px+SQSIZE, baseline))
        # Draw the glyph. 
        context.text(t, (px, baseline))
        # Construct the label from the original glyph, unicode and glyph name 
        # (if available)
        label = context.newString('%s (%d) %s' % (chr(self.uCode), 
            self.uCode, self.glyph.name), style=labelStyle)
        # Get the size of the generated formatted string to center it. 
        # Draw the label.
        tw,th = label.size
        context.text(label, (px + SQSIZE/2 - tw/2, py-pt(7)))
        # Construct the rotated width string on left and right side.
        widthLabel = context.newString('Width: %d' % self.glyph.width, 
            style=labelStyle)
        leftLabel = context.newString('Offset: %d' % self.glyph.leftMargin, 
            style=labelStyle)
        context.save() # Save the graphics state
        # Translate the origin to the current position of self, so we can rotate.
        context.translate(px, py) 
        context.rotate(90) # Rotate clockwise vertical
        context.text(widthLabel, (0, -SQSIZE-pt(7))) # Draw labels on these positions
        context.text(leftLabel, (0, pt(3)))
        context.restore() # Restore the graphics state

        self._restoreScale(view)

def makeHeader(page, font):
    page.padding = PADDING
    header = newRect(h=inch(1), padding=pt(8), mb=inch(0.6), parent=page, 
        fill=0.4, conditions=[Fit2Width(), Top2Top()])
    title = context.newString('Key map', style=titleStyle)
    mr = pt(8)
    newTextBox(title, w=page.pw*0.35, fill=0.5, parent=header, 
        pt=pt(12), # Padding top
        mr=mr, # Margin right of the "Key map" text box element   
        borderTop=dict(stroke=whiteColor, strokeWidth=SHADOW),
        borderLeft=dict(stroke=whiteColor, strokeWidth=SHADOW),
        borderRight=dict(stroke=blackColor, strokeWidth=SHADOW),
        borderBottom=dict(stroke=blackColor, strokeWidth=SHADOW),
        conditions=[Left2Left(), Fit2Height()])
    t = 'Size: %s  Font: %s\nNotice: © %s\nPrinted by PageBot on %s' % \
        (pt(SQSIZE), font.path.split('/')[-1], font.info.copyright, now().datetime)
    fontInfo = context.newString(t, style=fontInfoStyle)
    newTextBox(fontInfo, fill=1, parent=header, margin=0, w=page.pw*0.65-3*mr,
        padding=pt(4),
        borderTop=dict(stroke=blackColor, strokeWidth=SHADOW),
        borderLeft=dict(stroke=blackColor, strokeWidth=SHADOW),
        conditions=[Right2Right(), Top2Top(), Fit2Height()]
    )
    page.solve()
    
def makePages(doc, font):
    u"""Create the elements (header and a grid of GlyphSquares) for each page.
    Add as many pages as needed to accommodate all glyphs in the font.
    """
    page = doc[1] # Get the first (automatic) generated page from the document,
    makeHeader(page, font) # Make the heading block for this page.
    # Keep track on the amount of squares on the page, checking currently agains
    # the fixed value of SQUARES (8x8 in the original Fontographer layout)
    # TODO: Make this responsive to the size of the page.
    squareIndex = 0 
    for uCode, glyphName in sorted(font.cmap.items()):
        if uCode < 32: # Skip control characters
            continue
        if squareIndex >= SQUARES: 
            if len(doc) >= (MAX_PAGES or XXXL):
                return
            squareIndex = 0
            page = doc.newPage()
            makeHeader(page, font)

        squareIndex += 1
        glyph = f[glyphName]
        # Create an element for this glyph. Note the conditions that will
        # later be checked for the position status by doc.solve()-->page.solve()
        GlyphSquare(glyph, uCode, name='square-%s' % glyphName, w=SQSIZE, h=SQSIZE,
            ml=SQML, mr=SQMR, mb=SQMB,
            borders=dict(strokeWidth=pt(0.5), line=ONLINE, stroke=0, dash=(1,1)),
            parent=page, fill=color(0.95, a=0.8), stroke=noColor,
            conditions=[Right2Right(), Float2Top(), Float2Left()],
        )
# Actual building of the proof pages. 
# Create a new doc, with the right amount of frames/pages.
doc = Document(w=W, h=H, originTop=False, context=context)
# Get the current default view (maker of PDF page documents) and set 
# the flag to show padding.
view = doc.view
view.showPadding = True
# Make all specimen pages for this font.
makePages(doc, f)
# Solve the layout conditions recursively for all elements. 
# This will make the fit on the grid of the page.
# In this case it would not be too complex to position directly by
# (x, y) grid cells. But using conditions it more sustainable, as it
# adapts naturally to a changing page size.
doc.solve()
# Export the generated pages to the PDF document.
# The changed content of the _export folder is committed into Git.
doc.export('_export/%s_Fog35-KeyMap.pdf' % f.info.fullName)
doc.export('_export/%s_Fog35-KeyMap.png' % f.info.fullName)

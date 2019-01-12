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
#     UseThemes.py
#
from pagebot.themes.palette import PALETTES
from pagebot.constants import A4, CENTER
from pagebot.toolbox.units import upt, point2D, pt, units
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.document import Document
from pagebot.conditions import *
from pagebot.elements import Rect, TextBox
from pagebot.gradient import Shadow

context = DrawBotContext()

W, H = A4[0], pt(700)

PADDING = pt(50)

doc = Document(w=W, h=H, context=context, originTop=False)

class  ColorPalette(Rect):
    """Draw a palette as matrix of spot color samples.

    >>> from pagebot.contexts.drawbotcontent import DrawBotContext
    >>> from pagebot.conditions import *
    >>> context = DrawBotContext()
    >>> doc = Document(w=500, h=500, context=context)
    >>> page = doc[1]
    >>> page.padding = pt(30)
    >>> ps = PaletteColors(parent=page, conditions=[Fit2Width(), Top2Top()])
    """
    def __init__(self, palette, colorWidth=None, **kwargs):
        Rect.__init__(self, **kwargs)
        self.palette = palette
        self.colorWidth = colorWidth or 100 # Width of color samples (needs to fit text)

    def buildFrame(self, view, p):
        pass # Ignore frame and shadow drawing for the whole element.

    def buildColor(self, x, y, cw, ch, clr):

        c = self.context

        eShadow = self.shadow

        if eShadow:
            c.saveGraphicState()
            c.setShadow(eShadow)
            c.fill(eShadow.color)
            c.rect(x, y, cw, ch)
            c.restoreGraphicState()

        c.stroke(None)
        c.fill(1)
        c.rect(x, y, cw, ch) # All background

        c.fill(clr)
        c.rect(x, y+(ch-cw), cw, cw) # Color square

        c.stroke(0)
        c.strokeWidth(1)
        c.fill(None)
        c.rect(x, y, cw, ch) # Frame

        bs = context.newString('SPOT\n%s' % clr.spot, 
            style=dict(font='Upgrade-Regular', fontSize=15, leading=18, xTextAlign=CENTER, textFill=0))
        tw, th = bs.size
        c.text(bs, (x+cw/2-tw/2, y+30))


    def buildElement(self, view, p, drawElements=True):
        c = self.context
        px, py = point2D(p)        

        cw = units(self.colorWidth) # Fixed color sample widht
        ch = cw*1.5 # w/h ratio of a color sample
        cols = 4 # Color columns
        rows = int(len(self.palette)/cols) + 1 # Color rows (palette has currently )
        gutter = (self.w - cw*cols)/(cols - 1) # Calculate the gutter to fill up fixed color-sample widths

        cIndex = 0
        for iy in range(rows):
            for ix in range(cols):
                if cIndex < len(self.palette): # Check on "incomplete" last row
                    if self.palette[cIndex] is not None: # Check if there is a valid color at this attribute index
                        self.buildColor(px + ix*(cw+gutter), py + self.h - iy*(ch+gutter)-ch, cw, ch, self.palette[cIndex])
                cIndex += 1 # Color/attribute index

page = doc[1]
for _, palette in sorted(PALETTES.items()):
    page.padding = PADDING
    page.pb = 0
    bs = context.newString('Theme: %s' % palette.name, style=dict(font='Upgrade-Medium', fontSize=24, textFill=0))
    Rect(parent=page, z=-10, w=W, h=H, fill=0.8)
    TextBox(bs, parent=page, h=48, w=W-2*PADDING, conditions=[Left2Left(), Top2Top()])
    ColorPalette(palette, parent=page, conditions=[Fit2Width(), Float2Top()], 
        shadow=Shadow(blur=pt(10), color=0.4))
    page.solve()

    page = page.next


doc.export('_export/ThemeColorsByDocument.pdf')
doc.export('_export/ThemeColorsByDocument.png')



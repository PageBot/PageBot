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
#     DrawVariableFont3AxisAnimation.py
#
#     Note: the type of animation used in this example is self-contained:
#     all code for for FontIcon class and KeyFrame class is here.
#     In the future these classes will be part of the main PageBot library,
#     which may make them incompatible with this particular example.
#
#     TODO: Instance location does not seem to work right.
#
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.constants import CENTER
from pagebot.toolbox.color import blackColor
from pagebot.toolbox.units import pt, em, upt

context = getContext()

W = H = pt(500)

f = findFont('Amstelvar-Roman-VF') # Get PageBot Font instance of Variable font.

LIGHT72 = getVarFontInstance(f, dict(wght=0.5, wdth=0.6, opsz=72), styleName='Light72')
BOOK_LIGHT = getVarFontInstance(f, dict(wght=0.5, wdth=0.7), styleName='Book Light')
BOOK_CONDENSED = getVarFontInstance(f, dict(wght=0.6, wdth=0.7), styleName='Book Condensed')
BOOK = getVarFontInstance(f, dict(wght=0.6, wdth=0), styleName='Book')
LIGHT_CONDENSED = getVarFontInstance(f, dict(wght=0.9, wdth=0.7), styleName='Light Condensed')
LIGHT = getVarFontInstance(f, dict(wght=0.9, wdth=0), styleName='Light')
BOOK_ITALIC = getVarFontInstance(f, dict(wght=0.25, wdth=1), styleName='Book Italic')
MEDIUM = getVarFontInstance(f, dict(wght=0.40, wdth=0), styleName='Medium')
SEMIBOLD = getVarFontInstance(f, dict(wght=0.40, wdth=1), styleName='Semibold')
SEMIBOLD_CONDENSED = getVarFontInstance(f, dict(wght=0.40, wdth=0.5), styleName='Semibold Condensed')
BOLD = getVarFontInstance(f, dict(wght=0.0, wdth=0), styleName='Bold')
BOLD_CONDENSED = getVarFontInstance(f, dict(wght=0.0, wdth=0.7), styleName='Bold Condensed')
BOLD_ITALIC = getVarFontInstance(f, dict(wght=0.7, wdth=0), styleName='Bold Italic')

LABEL_FONT = BOOK

class FontIcon:
    W = pt(30)
    H = pt(40)
    L = pt(2)
    E = pt(8)
    LABEL_RTRACKING = em(0.02)
    LABEL_RLEADING = em(1.3)

    def __init__(self, f, name=None, label=None, title=None, eId=None, c='F', s=1, line=None,
            labelFont=None, titleFont=None, x=0, y=0, show=True):
        self.f = f # Font instance
        self.labelFont = labelFont or f
        self.titleFont = titleFont, labelFont or f
        self.title = title
        self.name = name # Name below the icon
        self.label = label # Optiona second label line
        self.c = c # Character(s) in the icon.
        self.scale = s
        self.line = line or self.L
        self.x = x
        self.y = y
        self.show = show
        self.eId = eId

    def _get_w(self):
        return self.W*self.scale
    w = property(_get_w)

    def _get_ih(self):
        """Answer scaled height of the plain icon without name label."""
        return self.H*self.scale
    ih = property(_get_ih)

    def _get_h(self):
        h = self.ih
        if self.name:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        if self.label:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        if self.title:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        return h
    h = property(_get_h)

    def draw(self, orgX, orgY):
        if not self.show:
            return
        w = self.w # Width of the icon
        h = self.ih # Height of the icon
        e = self.E*self.scale # Ear size
        l = self.L*self.scale # Line
        x = self.x + orgX
        y = self.y + orgY

        context.newPath()
        context.moveTo((0, 0))
        context.lineTo((0, h))
        context.lineTo((w-e, h))
        context.lineTo((w, h-e))
        context.lineTo((w, 0))
        context.lineTo((0, 0))
        context.closePath()
        context.moveTo((w-e, h))
        context.lineTo((w-e, h-e))
        context.lineTo((w, h-e))

        context.save()
        context.fill(1)
        context.stroke(0)
        context.strokeWidth(self.line)
        context.translate(x, y)
        context.drawPath()

        labelSize = e
        bs = context.newString(self.c,
                               style=dict(font=self.f.path,
                                          textFill=blackColor,
                                          fontSize=h*2/3))
        tw, th = bs.size
        context.text(bs, (w/2-tw/2, h/2-th/3.2))

        if self.title:
            bs = context.newString(self.title,
                                   style=dict(font=self.labelFont.path,
                                              textFill=blackColor,
                                              tracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.size
            context.text(bs, (w/2-tw/2, self.ih+th/2))

        y -= upt(self.LABEL_RLEADING, base=labelSize)
        if self.name:
            bs = context.newString(self.name,
                                   style=dict(font=self.labelFont.path,
                                              textFill=blackColor,
                                              tracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.size
            context.text(bs, (w/2-tw/2, y))
            y -= upt(self.LABEL_RLEADING, base=labelSize)

        if self.label:
            bs = context.newString(self.label,
                                   style=dict(font=self.labelFont.path,
                                              textFill=blackColor,
                                              tracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.size
            context.text(bs, (w/2-tw/2, y))
        context.restore()

class KeyFrame:
    def __init__(self, objects, positions, steps=None, drawBackground=None):
        self.objects = objects
        self.positions = positions
        self.steps = steps or 1
        if drawBackground is not None:
            self.drawBacktround = drawBackground

    def drawBackground(self):
        context.fill(1)
        context.rect(0, 0, W, H)

    def draw(self):
        for n in range(self.steps):
            context.newPage(W, H)
            self.drawBackground()
            for o in self.objects:
                offsetX = 0
                offsetY = 0
                if o.eId in self.positions: # Changed target, then calculate new offset
                    tx, ty = self.positions[o.eId]
                    offsetX = (tx-o.x)*1.0*n/self.steps
                    offsetY = (ty-o.y)*1.0*n/self.steps
                o.draw(offsetX, offsetY)
        # Set the new target positions
        for o in self.objects:
            if o.eId in self.positions:
                tx, ty = self.positions[o.eId]
                o.x = tx
                o.y = ty
S = 1.5

lightIcon = FontIcon(LIGHT, 'Light', eId='Light', s=S, label='50K', labelFont=LABEL_FONT)
lightCondensedIcon = FontIcon(LIGHT_CONDENSED, 'Light Condensed', eId='LightCondensed', s=S, label='50K', labelFont=LABEL_FONT)
boldIcon = FontIcon(BOLD, 'Bold', eId='Bold', s=S, label='50K', labelFont=LABEL_FONT)
boldCondensedIcon = FontIcon(BOLD_CONDENSED, 'Bold Condensed', eId='BoldCondensed', s=S, label='50K', labelFont=LABEL_FONT)
varFontIcon = FontIcon(BOOK, 'Variable Font', eId='VarFont', s=S, label='0K', labelFont=LABEL_FONT, title='No axes')

fontIcons = [varFontIcon, lightIcon, boldIcon, lightCondensedIcon, boldCondensedIcon]
id2FontIcon = {}
for fontIcon in fontIcons:
    id2FontIcon[fontIcon.eId] = fontIcon

def positionFontIcons():
    y = H - 110
    for iconId in ('Light', 'LightCondensed', 'Bold', 'BoldCondensed'):
        fontIcon = id2FontIcon[iconId]
        fontIcon.x = 50
        fontIcon.y = y
        y -= fontIcon.h*1.1

    varFontIcon = id2FontIcon['VarFont']
    varFontIcon.x = W/2-varFontIcon.w/2
    varFontIcon.y = H/2-varFontIcon.ih/2

def drawBackground(keyFrame, frame):
    context.fill(1)
    context.rect(0, 0, W, H)

def drawAnimation():
    positionFontIcons()
    varFontIcon = id2FontIcon['VarFont']

    KeyFrame(fontIcons, {}, 8,
        drawBackground=drawBackground
    ).draw()

    KeyFrame(fontIcons,
        {'Light': (varFontIcon.x, varFontIcon.y), 'Bold': (varFontIcon.x, varFontIcon.y)}, 14,
        drawBackground=drawBackground
    ).draw()
    id2FontIcon['Light'].show = False
    id2FontIcon['Bold'].show = False
    varFontIcon.title = '1 axis [Weight]'
    varFontIcon.label = '75K'

    KeyFrame(fontIcons,
        {'LightCondensed': (varFontIcon.x, varFontIcon.y), 'BoldCondensed': (varFontIcon.x, varFontIcon.y)}, 14,
        drawBackground=drawBackground
    ).draw()
    id2FontIcon['LightCondensed'].show = False
    id2FontIcon['BoldCondensed'].show = False
    varFontIcon.title = '2 axis [Weight, Width]'
    varFontIcon.label = '90K'

    KeyFrame(fontIcons, {}, 14,
        drawBackground=drawBackground
    ).draw()

    context.saveImage('_export/VarFont3Axes.gif')

drawAnimation()

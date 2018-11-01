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
#     DrawVariableFontManyWeightsAnimation.py
#
#     Note: the type of animation used in this example is self-contained:
#     all code for for FontIcon class and KeyFrame class is here.
#     In the future these classes will be part of the main PageBot library,
#     which may make them incompatible with this particular example.
#
#     TODO: Positions of icons and var-instances don't seem to work.
#
from pagebot import getRootPath
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.constants import CENTER
from pagebot.toolbox.units import pt, em, upt
from pagebot.toolbox.color import color, blackColor

c = getContext()
W = H = pt(500)

# Get PageBot Font instances of Variable font.
f = findFont('Amstelvar-Roman-VF')
ULTRALIGHT_CONDENSED = getVarFontInstance(f, dict(wght=0.9, wdth=0.7), styleName='Ultra Light Condensed')
ULTRALIGHT = getVarFontInstance(f, dict(wght=1, wdth=0), styleName='Ultra Light')
LIGHT_CONDENSED = getVarFontInstance(f, dict(wght=0.9, wdth=0.7), styleName='Light Condensed')
LIGHT = getVarFontInstance(f, dict(wght=0.9, wdth=0), styleName='Light')
THIN_CONDENSED = getVarFontInstance(f, dict(wght=0.8, wdth=0.7), styleName='Thin Condensed')
THIN = getVarFontInstance(f, dict(wght=0.8, wdth=0), styleName='Thin')
BOOK_CONDENSED = getVarFontInstance(f, dict(wght=0.7, wdth=0.7), styleName='Book Condensed')
BOOK = getVarFontInstance(f, dict(wght=0.7, wdth=0), styleName='Book')
REGULAR_CONDENSED = getVarFontInstance(f, dict(wght=0.6, wdth=0.7), styleName='Regular Condensed')
REGULAR = getVarFontInstance(f, dict(wght=0.6, wdth=0), styleName='Regular')
MEDIUM_CONDENSED = getVarFontInstance(f, dict(wght=0.5, wdth=0.7), styleName='Medium Condensed')
MEDIUM = getVarFontInstance(f, dict(wght=0.5, wdth=0), styleName='Medium')
SEMIBOLD_CONDENSED = getVarFontInstance(f, dict(wght=0.30, wdth=0.7), styleName='Semibold Condensed')
SEMIBOLD = getVarFontInstance(f, dict(wght=0.30, wdth=0), styleName='Semibold')
BOLD_CONDENSED = getVarFontInstance(f, dict(wght=0.0, wdth=0.7), styleName='Bold Condensed')
BOLD = getVarFontInstance(f, dict(wght=0.0, wdth=0), styleName='Bold')

LABEL_FONT = BOOK

class FontIcon:
    """
    """

    W = pt(30)
    H = pt(40)
    L = pt(2)
    E = pt(8)
    LABEL_RTRACKING = em(0.02)
    LABEL_RLEADING = em(1.3)

    def __init__(self, f, name=None, label=None, title=None, eId=None, char='F', s=1, line=None,
            labelFont=None, titleFont=None, x=0, y=0, show=True):
        self.f = f # Font instance
        self.labelFont = labelFont or f
        self.titleFont = titleFont, labelFont or f
        self.title = title
        self.name = name # Name below the icon.
        self.label = label # Optional second label line.
        self.char = char # Character(s) in the icon.
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
        """Answers scaled height of the plain icon without name label."""
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
        """Draws a font icon"""

        bs = c.newString('Book Cover', style=dict(font='Georgia', fontSize=pt(50), fill=blackColor))
        c.text(bs, (100, 100))
        return

        if not self.show:
            return

        w = self.w # Width of the icon
        h = self.ih # Height of the icon
        e = self.E*self.scale # Ear size
        l = self.L*self.scale # Line
        x = self.x + orgX
        y = self.y + orgY

        # Doc icon.
        path = c.newPath()
        c.moveTo((pt(0), pt(0)))
        c.lineTo((pt(0), pt(h)))
        c.lineTo((pt(w-e), pt(h)))
        c.lineTo((pt(w), pt(h-e)))
        c.lineTo((pt(w), pt(0)))
        c.lineTo((pt(0), pt(0)))
        c.closePath()
        c.moveTo((pt(w-e), pt(h)))
        c.lineTo((pt(w-e), pt(h-e)))
        c.lineTo((pt(w), pt(h-e)))
        c.fill(whiteColor)
        c.stroke(blackColor)
        c.strokeWidth = self.line
        c.moveTo((pt(x), pt(y)))
        c.drawPath(path)
        c.saveGraphicState()

        labelSize = e
        bs = c.newString(self.char,
                         style=dict(font=self.f.path,
                                    textFill=blackColor,
                                    fontSize=h*2/3))
        tw, th = bs.size
        c.text(bs, (w/2-tw/2, h/2-th/3.2))
        fill(0)
        stroke(0)
        print(type(bs.s))
        text(bs.s, (w/2-tw/2, h/2-th/3.2))


        if self.title:
            bs = c.newString(self.title,
                             style=dict(font=self.labelFont.path,
                             textFill=blackColor,
                             tracking=self.LABEL_RTRACKING,
                             fontSize=labelSize))
            tw, th = bs.size
            c.textFill=blackColor,
            c.text(bs, ((w/2-tw/2), pt(self.ih+th/2)))
            text(bs.s, (w/2-tw/2, self.ih+th/2))

        y -= upt(self.LABEL_RLEADING, base=labelSize)

        if self.name:
            bs = c.newString(self.name,
                             style=dict(font=self.labelFont.path,
                                        textFill=blackColor,
                                        tracking=self.LABEL_RTRACKING,
                                        fontSize=labelSize))
            tw, th = bs.size
            c.text(bs, (w/2-tw/2, y))
            #text(self.name, (w/2-tw/2, y))

            y -= upt(self.LABEL_RLEADING, base=labelSize)
        if self.label:
            bs = c.newString(self.label,
                             style=dict(font=self.labelFont.path,
                                        textFill=blackColor,
                                        tracking=self.LABEL_RTRACKING,
                                        fontSize=labelSize))
            tw, th = bs.size
            c.text(bs, (w/2-tw/2, y))
            #text(self.label, (w/2-tw/2, y))
        c.restoreGraphicState()

class KeyFrame:
    """
    """

    def __init__(self, objects, positions, steps=None, drawBackground=None):
        print('this is a new keyframe')
        self.objects = objects
        self.positions = positions
        self.steps = steps or 1
        self.drawBackgroundHook = drawBackground

    def drawBackground(self):
        c.fill(Color(0, 1, 1))
        c.rect(pt(0), pt(0), pt(W), pt(H))

    def draw(self):
        for n in range(self.steps):
            c.newPage(pt(W), pt(H))

            # Formattted string using append.
            print(' * Testing with append')
            bs = c.newString('')
            # Contains a DrawBot FormattedString.
            aa = bs.s
            aa.append("123", font="Helvetica", fontSize=100, fill=(1, 0, 1))
            print(aa._font)
            print(aa._fontSize)
            print(aa._fill)
            c.text(bs, (pt(100), pt(100)))

            # Formatted string without append.
            print(' * Testing without append')
            bs = c.newString('bla', style=dict(font='Helvetica', fontSize=pt(100), fill=0))
            print('style: %s' % bs.style)
            aa = bs.s
            print(aa._font)
            print(aa._fontSize)
            #c.setTextFillColor(aa, blackColor)
            print(aa._fill)
            c.b.text(aa, (100, 200))

            c.text(bs, (100, 200))

            """
            self.drawBackground()
            if self.drawBackgroundHook is not None:
                self.drawBackgroundHook(self, n)
            """

            for o in self.objects:
                offsetX = 0
                offsetY = 0
                if o.eId in self.positions: # Changed target, then calculate new offset
                    tx, ty = self.positions[o.eId]
                    offsetX = (tx-o.x)*1.0*n/self.steps
                    offsetY = (ty-o.y)*1.0*n/self.steps

                o.draw(offsetX, offsetY)

        # Set the new target positions.
        for o in self.objects:
            if o.eId in self.positions:
                tx, ty = self.positions[o.eId]
                o.x = tx
                o.y = ty
S = 1.5
FSIZE = '50k'
ultraLightIcon = FontIcon(ULTRALIGHT, 'Ultra Light', eId='UltraLight', s=S, label=FSIZE, labelFont=LABEL_FONT)
ultraLightCondensedIcon = FontIcon(ULTRALIGHT_CONDENSED, 'UltraLight Condensed', eId='UltraLightCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
lightIcon = FontIcon(LIGHT, 'Light', eId='Light', s=S, label=FSIZE, labelFont=LABEL_FONT)
lightCondensedIcon = FontIcon(LIGHT_CONDENSED, 'Light Condensed', eId='LightCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
thinIcon = FontIcon(THIN, 'Thin', eId='Thin', s=S, label=FSIZE, labelFont=LABEL_FONT)
thinCondensedIcon = FontIcon(THIN_CONDENSED, 'Thin Condensed', eId='ThinCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
bookIcon = FontIcon(BOOK, 'Book', eId='Book', s=S, label=FSIZE, labelFont=LABEL_FONT)
bookCondensedIcon = FontIcon(BOOK_CONDENSED, 'Book Condensed', eId='BookCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
regularIcon = FontIcon(REGULAR, 'Regular', eId='Regular', s=S, label=FSIZE, labelFont=LABEL_FONT)
regularCondensedIcon = FontIcon(REGULAR_CONDENSED, 'Regular Condensed', eId='BookCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
mediumIcon = FontIcon(MEDIUM, 'Medium', eId='Medium', s=S, label=FSIZE, labelFont=LABEL_FONT)
mediumCondensedIcon = FontIcon(MEDIUM_CONDENSED, 'Medium Condensed', eId='MediumCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
semibolIcon = FontIcon(SEMIBOLD, 'Semibold', eId='Semibold', s=S, label=FSIZE, labelFont=LABEL_FONT)
semiboldCondensedIcon = FontIcon(SEMIBOLD_CONDENSED, 'Semibold Condensed', eId='SemiboldCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
boldIcon = FontIcon(BOLD, 'Bold', eId='Bold', s=S, label=FSIZE, labelFont=LABEL_FONT)
boldCondensedIcon = FontIcon(BOLD_CONDENSED, 'Bold Condensed', eId='BoldCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
varFontIcon = FontIcon(BOOK, 'Variable Font', eId='VarFont', s=S, char='', label='0k', labelFont=LABEL_FONT, title='No axes')

fontIcons = [varFontIcon, ultraLightIcon, lightIcon, thinIcon, bookIcon, regularIcon, mediumIcon, semibolIcon, boldIcon]
id2FontIcon = {}

for fontIcon in fontIcons:
    id2FontIcon[fontIcon.eId] = fontIcon

def positionFontIcons():
    y = Y = H - 130
    for iconId in ('UltraLight', 'Thin', 'Regular', 'Semibold'):
        fontIcon = id2FontIcon[iconId]
        fontIcon.x = 50
        fontIcon.y = y
        y -= fontIcon.h*1.1

    y = Y

    for iconId in ('Light', 'Book', 'Medium', 'Bold'):
        fontIcon = id2FontIcon[iconId]
        fontIcon.x = 150
        fontIcon.y = y
        y -= fontIcon.h*1.1

    varFontIcon = id2FontIcon['VarFont']
    varFontIcon.x = W/2-varFontIcon.w/2+40
    varFontIcon.y = H/2-varFontIcon.ih/2

def drawBackground1(keyFrame, frame):
    bs = c.newString('8 weight fonts\nTotal 400k',
                     style=dict(font=LABEL_FONT.path,
                                leading=em(1.2),
                                fontSize=18,
                                fill=color(1, 0, 0)))
    c.textBox(bs, (50, H-60, 200, 50))

def drawBackground2(keyFrame, frame):
    drawBackground1(keyFrame, frame)
    varFontIcon = id2FontIcon['VarFont']
    bs = c.newString('1 axis\nTotal 100k',
                     style=dict(font=LABEL_FONT.path,
                                leading=em(1.2),
                                fontSize=18,
                                fill=color(1, 0, 0)))
    c.textBox(bs, (varFontIcon.x, H-60, 200, 50))

def drawBackground3(keyFrame, frame):
    drawBackground1(keyFrame, frame)
    varFontIcon = id2FontIcon['VarFont']
    bs = c.newString('%d weights\nTotal 100k' % ((2**15)+1),
                     style=dict(font=LABEL_FONT.path,
                                leading=em(1.2),
                                fontSize=18,
                                textFill=color(1, 0, 0)))
    c.textBox(bs, (varFontIcon.x, H-60, 200, 50))

def drawAnimation():
    """
    Main function, draws a variation font infographic animation.
    """

    positionFontIcons()
    varFontIcon = id2FontIcon['VarFont']

    '''
    #
    KeyFrame(fontIcons, {}, 15,
        drawBackground=drawBackground1
    ).draw()
    '''

    #
    KeyFrame(fontIcons,
        {'Regular': (varFontIcon.x, varFontIcon.y)}, 10,
        #drawBackground=None
    ).draw()

    id2FontIcon['Regular'].show = False
    varFontIcon.title = '0 axis'
    varFontIcon.label = FSIZE
    varFontIcon.c = 'F'

    '''
    #
    KeyFrame(fontIcons,
        {'Bold': (varFontIcon.x, varFontIcon.y)}, 10,
        drawBackground=drawBackground1
    ).draw()
    id2FontIcon['Bold'].show = False
    varFontIcon.title = '1 axis [Weight]'
    varFontIcon.label = '100k'

    KeyFrame(fontIcons, {}, 10,
        drawBackground=drawBackground2
    ).draw()

    #
    KeyFrame(fontIcons,
        {'UltraLight': (varFontIcon.x, varFontIcon.y), 'Light': (varFontIcon.x, varFontIcon.y),
         'Thin': (varFontIcon.x, varFontIcon.y), 'Book': (varFontIcon.x, varFontIcon.y),
         'Medium': (varFontIcon.x, varFontIcon.y), 'Semibold': (varFontIcon.x, varFontIcon.y),
         'Bold': (varFontIcon.x, varFontIcon.y)}, 10,
        drawBackground=drawBackground2
    ).draw()

    id2FontIcon['UltraLight'].show = False
    id2FontIcon['Light'].show = False
    id2FontIcon['Thin'].show = False
    id2FontIcon['Book'].show = False
    id2FontIcon['Medium'].show = False
    id2FontIcon['Semibold'].show = False
    varFontIcon.label = '100K'

    #
    KeyFrame(fontIcons, {}, 40,
        drawBackground=drawBackground3
    ).draw()
    '''

    c.saveImage('_export/VarFontManyWeights.gif')

drawAnimation()

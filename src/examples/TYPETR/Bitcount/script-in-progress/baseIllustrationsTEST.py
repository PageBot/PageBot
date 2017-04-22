#
#    Typetr logo animation
#

bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName and not 'Italic' in fontName and not 'Prop' in fontName:
        bitcountNames.append(fontName)

PIX = 10

"""
Feature | Description | Grid Single | Grid Double | Mono Single | Mono Double | Prop Single | Prop Double
--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- | --- |
**c2sc** | lc->sc 			| X | X | X | X | X | X
**smcp** | Cap->sc 		| X | X | X | X | X | X
**frac** | Fractions 		| - | - | - | - | X | X
**liga** | Ligatures 		| X | X | X | X | X | X
**ss01** | Ascenders+ 		| - | - | X | X | X | X
**ss02** | Capitals+ 		| - | - | X | X | X | X
**ss03** | Descenders+ 		| - | - | X | X | X | X
**ss04** | Contrast px 		| X | - | X | - | X | -
**ss05** | No-Contrast px 	| - | X | - | X | - | X
**ss06** | Forced xHght 	| X | - | - | - | - | -
**ss07** | Condensed 		| X | - | X | - | X | -
**ss08** | Italic 			| X | X | X | X | X | X
**ss09** | Alternative g 	| - | - | X | X | X | X
**onum** | Lowercase figs 	| X | X | X | X | X | X
**zero** | Slash zero 		| X | X | X | X | X | X
"""
    
GRID_COLOR = 0.4, 0.7, 1 
FONTS = {
    'Double': 'BitcountMonoDouble-RegularCircle',
    'DoubleIt': 'BitcountMonoDouble-RegularCircleItalic',
    'DoubleBold': 'BitcountMonoDouble-BoldCircle',
    'DoubleBold': 'BitcountMonoDouble-BoldCircle',
    'DoubleBoldSquare': 'BitcountMonoDouble-BoldSquare',
    'DoubleBook': 'BitcountMonoDouble-BookCircle',
    'DoubleBookOpenCircle': 'BitcountMonoDouble-BookOpenCircle',
    'DoubleBookOpenSquare': 'BitcountMonoDouble-BookOpenSquare',
    'DoubleBookSquare': 'BitcountMonoDouble-BookSquare',
    'DoubleItalic': 'BitcountMonoDouble-RegularCircleItalic',
    'DoubleMedium': 'BitcountMonoDouble-MediumCircle',
    'DoubleMediumSquare': 'BitcountMonoDouble-MediumSquare',
    'GridDouble': 'BitcountGridDouble-RegularCircle',
    'GridDoubleIt': 'BitcountGridDouble-RegularCircleItalic',
    'GridSingle': 'BitcountGridSingle-RegularCircle',
    'GridSingleIt': 'BitcountGridSingle-RegularCircleItalic',
    'PropDouble': 'BitcountPropDouble-RegularCircle',
    'PropDoubleIt': 'BitcountPropDouble-RegularCircleItalic',
    'PropSingle': 'BitcountPropSingle-RegularCircle',
    'PropSingleIt': 'BitcountPropSingle-RegularCircleItalic',
    'Single': 'BitcountMonoSingle-RegularCircle',
    'SingleIt': 'BitcountMonoSingle-RegularCircleItalic',
    'SingleBold': 'BitcountMonoSingle-BoldCircle',
    'SingleBold': 'BitcountMonoSingle-BoldCircle',
    'SingleBoldSquare': 'BitcountMonoSingle-BoldSquare',
    'SingleBoldLineSquare': 'BitcountMonoSingle-BoldLineSquare',
    'SingleBook': 'BitcountMonoSingle-BookCircle',
    'SingleBookOpenCircle': 'BitcountMonoSingle-BookOpenCircle',
    'SingleBookOpenSquare': 'BitcountMonoSingle-BookOpenSquare',
    'SingleBookSquare': 'BitcountMonoSingle-BookSquare',
    'SingleBookLineSquare': 'BitcountMonoSingle-BookLineSquare',
    'SingleItalic': 'BitcountMonoSingle-RegularCircleItalic',
    'SingleMedium': 'BitcountMonoSingle-MediumCircle',
    'SingleMediumSquare': 'BitcountMonoSingle-MediumSquare',
    'SingleMediumLineSquare': 'BitcountMonoSingle-MediumLineSquare',
    'SingleSquare': 'BitcountMonoSingle-RegularSquare',
    'SingleSquareIt': 'BitcountMonoSingle-RegularSquareItalic',
    'SingleLineSquare': 'BitcountMonoSingle-RegularLineSquare',
    'DoubleSquare': 'BitcountMonoDouble-RegularSquare',
}
H = 9*PIX
W = 32*PIX
X = Y = PIX
FS = PIX*10

size(W, H)

def resetFeatures():
    openTypeFeatures(c2sc=False, smcp=False, frac=False, liga=False, ss01=False, ss02=False,
        ss03=False, ss04=False, ss05=False, ss06=False, ss07=False, ss08=False, ss09=False,
        onum=False, zero=False)
        
def drawString(s, px, py, fontName, color=None):
    font(FONTS[fontName])
    fontSize(FS)
    stroke(None)
    if color is not None:
        r, g, b = color
        fill(r, g, b)
    else:
        fill(color or 0)
    text(s, (X+px*PIX, Y+(1+py)*PIX))

def drawGrid(w, h, offsetX=0, offsetY=0, color=None):
    newPath()
    for x in range(PIX, w, PIX):
        moveTo((x+offsetX, Y+offsetY))
        lineTo((x+offsetX, Y+h-PIX*2+offsetY))
    for y in range(PIX, h, PIX):
        moveTo((X+offsetX, y+offsetY))
        lineTo((X+w-PIX*2+offsetX, y+offsetY))
    fill(None)
    r, g, b = color or GRID_COLOR
    stroke(r, g, b)
    strokeWidth(0.5)
    drawPath()
     
def make_singleFigures():
    s0 = 'ABC0123456789'
    s1 = 'abc0123456789'
    s2 = 'Fraction 01234/56789'
    w = (len(s0)*6+2)*PIX
    h = 10*PIX
    newPage(w, h-PIX)
    drawGrid(w, h-PIX)
    drawString(s0, 0, 0, 'Single')
    resetFeatures()

    newPage(w, h-PIX)
    drawGrid(w, h-PIX)
    openTypeFeatures(ss07=True) #  Condensed
    drawString(s0, 0, 0, 'Single')
    resetFeatures()

    newPage(w, h)
    drawGrid(w, h)
    openTypeFeatures(ss01=True, ss02=True) #  Extended ascender
    drawString(s0, 0, 0, 'Single')
    resetFeatures()

    newPage(w, h)
    drawGrid(w, h)
    openTypeFeatures(ss01=True, ss02=True, ss07=True) #  Condensed, Extended ascender
    drawString(s0, 0, 0, 'Single')
    resetFeatures()

    newPage(w, h-PIX)
    drawGrid(w, h-PIX)
    openTypeFeatures(onum=True, lnum=True)
    drawString(s1, 0, 0, 'Single')
    resetFeatures()

    newPage(w, h-PIX)
    drawGrid(w, h-PIX)
    openTypeFeatures(onum=True, lnum=True, ss07=True) # Condensed, lower case
    drawString(s1, 0, 0, 'Single')
    resetFeatures()

    newPage(w, h-PIX)
    drawGrid(w, h-PIX)
    openTypeFeatures(smcp=True, c2sc=False) # smallcaps
    fsSingleSC = FormattedString(s1, font=FONTS['Single'], fontSize=FS)
    drawString(fsSingleSC, 0, 0, 'Single')
    resetFeatures()

    newPage(w, h-PIX)
    drawGrid(w, h-PIX)
    openTypeFeatures(smcp=True, c2sc=False, ss07=True) # Condensed, smallcaps
    fsSingleSC = FormattedString(s1, font=FONTS['Single'], fontSize=FS)
    drawString(fsSingleSC, 0, 0, 'Single')
    resetFeatures()

    newPage(w, h)
    openTypeFeatures(onum=True, ss07=False, frac=True) # Fraction
    drawGrid(w, h)
    drawString(s2, 0, 0, 'PropSingle')
    resetFeatures()

def make_doubleFigures():
    s0 = 'ABC0123456789'
    s1 = 'abc0123456789'
    s2 = 'Fraction 01234/56789'
    w = (len(s0)*6+2)*PIX
    newPage(w, H)
    drawGrid(w, H)
    drawString(s0, 0, 0, 'Double')
    resetFeatures()
    newPage(w, H)
    drawGrid(w, H)
    drawString(s1, 0, 0, 'PropDouble')
    # Condensed
    resetFeatures()
    openTypeFeatures(onum=True, ss07=False, frac=True)
    newPage(w, H)
    drawGrid(w, H)
    drawString(s2, 0, 0, 'PropDouble')
    resetFeatures()
        

def make_zeros():
    variants = (
        (False, False, True, False),
        (True, False, True, False),
        (False, True, True, False),
        (True, True, True, False),
         
        (False, False, False, False),
        (True, False, False, False),
        (False, True, False, False),
        (True, True, False, False),
         
        (False, False, False, True),
        (True, False, False, True),
        (False, True, False, True),
        (True, True, False, True),
         
        )
    s = 'Aa012'
    w = (len(s)*6+2)*PIX
    for cond, slashed, lc, caps in variants:
        newPage(w, H)
        drawGrid(w, H)
        #openTypeFeatures(onum=True, lnum=True, hwid=True, ss01=True, ss02=True, 
        #    ss04=False, ss05=False, ss06=False, pcap=False, smcp=False, c2sc=False)
        openTypeFeatures(zero=slashed, smcp=caps, c2sc=False, 
            ss07=cond, lnum=lc, onum=lc)
        drawString(s, 0, 0, 'Single')
        resetFeatures()

        
#print listOpenTypeFeatures(FONTS['Single'])
     
make_singleFigures()
make_doubleFigures()
#make_zeros()
saveImage('../images/referenceImagesFigures.png', 1)
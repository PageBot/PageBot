#
#    Typetr logo animation
#

bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName:
        print fontName
        bitcountNames.append(fontName)

PIX = 10

"""
Feature | Description | Grid Single | Grid Double | Mono Single | Mono Double | Prop Single | Prop Double
--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- | --- |
**c2sc** | Cap->sc 			| X | X | X | X | X | X
**smcp** | lc->sc 		| X | X | X | X | X | X
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
    'SingleLight': 'BitcountMonoSingle-LightCircle',
    'SingleBook': 'BitcountMonoSingle-BookCircle',
    'SingleBookSquare': 'BitcountMonoSingle-BookSquare',
    'SingleBookLineSquare': 'BitcountMonoSingle-BookLineSquare',
    'SingleItalic': 'BitcountMonoSingle-RegularCircleItalic',
    'SingleMedium': 'BitcountMonoSingle-MediumCircle',
    'SingleMediumSquare': 'BitcountMonoSingle-MediumSquare',
    'SingleMediumLineSquare': 'BitcountMonoSingle-MediumLineSquare',
    'SingleLightSquare': 'BitcountMonoSingle-LightSquare',
    'SingleLightLineSquare': 'BitcountMonoSingle-LightLineSquare',
    'SingleSquare': 'BitcountMonoSingle-RegularSquare',
    'SingleSquareIt': 'BitcountMonoSingle-RegularSquareItalic',
    'SingleLineSquare': 'BitcountMonoSingle-RegularLineSquare',
    'DoubleSquare': 'BitcountMonoDouble-RegularSquare',
    
    'SingleLightLineCircle': 'BitcountMonoSingle-LightLineCircle',
    'SingleBookLineCircle': 'BitcountMonoSingle-BookLineCircle',
    'SingleLineCircle': 'BitcountMonoSingle-RegularLineCircle',
    'SingleMediumLineCircle': 'BitcountMonoSingle-MediumLineCircle',
    'SingleBoldLineCircle': 'BitcountMonoSingle-BoldLineCircle',

    'SingleLightPlus': 'BitcountMonoSingle-LightPlus',
    'SingleBookPlus': 'BitcountMonoSingle-BookPlus',
    'SinglePlus': 'BitcountMonoSingle-RegularPlus',
    'SingleMediumPlus': 'BitcountMonoSingle-MediumPlus',
    'SingleBoldPlus': 'BitcountMonoSingle-BoldPlus',
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
    if fontName in FONTS:
        fontName = FONTS[fontName]
    font(fontName)
    fontSize(FS)
    stroke(None)
    if color is not None:
        r, g, b = color
        fill(r, g, b)
    else:
        fill(color or 0)
    text(s, (X+px*PIX, Y+(1+py)*PIX))

def drawGrid(w, h, offsetX=0, offsetY=0, color=None, italic=False):
    newPath()
    for x in range(PIX, w, PIX):
        if italic:
            moveTo((x+offsetX-2*PIX*14/100, Y+offsetY))
            lineTo((x+offsetX+(h-2*PIX)*14/100, Y+h-PIX*2+offsetY))
        else:
            moveTo((x+offsetX, Y+offsetY))
            lineTo((x+offsetX, Y+h-PIX*2+offsetY))
    for y in range(PIX, h, PIX):
        if italic:
            moveTo((X+offsetX+(y+PIX)*14/100, y+offsetY))
            lineTo((X+w-PIX*2+offsetX+(y+PIX)*14/100, y+offsetY))
        else:
            moveTo((X+offsetX, y+offsetY))
            lineTo((X+w-PIX*2+offsetX, y+offsetY))
    fill(None)
    r, g, b = color or GRID_COLOR
    stroke(r, g, b)
    strokeWidth(0.5)
    drawPath()
        
def make_aehg():
    s = 'aehg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    drawGrid(w, H)
    drawString(s, 0, 0, 'GridSingle')

def make_single_double_aehg():
    s = 'aehg'
    w = (len(s)*6*2+2)*PIX
    newPage(w, H)
    drawGrid(w, H)
    drawString(s, 0, 0, 'GridSingle')
    drawString(s, len(s)*6, 0, 'GridDouble')

def make_grid_accent_Aaaa():
    s = u'AÁÃaáã'
    w = (len(s)*6*2+2)*PIX
    newPage(w+PIX, H+3*PIX)
    drawGrid((len(s)*6+2)*PIX, H)
    drawGrid((len(s)*6+2)*PIX, H+3*PIX, (len(s)*6+1)*PIX)
    drawString(s, 0, 0, 'GridSingle')
    drawString(s, len(s)*6+1, 0, 'Single')

def make_mono_ascender_descender():
    s = u'Adp'
    w = (len(s)*6*2+2)*PIX
    newPage(w+PIX, H+2*PIX)
    drawGrid((len(s)*6+2)*PIX, H, offsetY=PIX)
    drawGrid((len(s)*6+2)*PIX, H+2*PIX, (len(s)*6+1)*PIX)
    drawString(s, 0, 1, 'Single')
    openTypeFeatures(ss01=True, ss02=True, ss03=True) # Ascender+ and descender+
    drawString(s, len(s)*6+1, 1, 'Single')
    resetFeatures()
    
def make_mono_capital_ascender_descender():
    s = u'Adp'
    w = (len(s)*6*3+2)*PIX
    newPage(w+PIX, H+2*PIX)
    drawGrid((len(s)*6+2)*PIX, H, offsetY=PIX)
    drawGrid((len(s)*6*2+2)*PIX, H+2*PIX, (len(s)*6+1)*PIX)
    drawString(s, 0, 1, 'Single')
    openTypeFeatures(ss01=True, ss03=True) # Ascender+ and descender+
    drawString(s, len(s)*6+1, 1, 'Single')
    resetFeatures()
    openTypeFeatures(ss01=True, ss02=True, ss03=True) # Ascender+ and descender+
    drawString(s, len(s)*6*2+1, 1, 'Single')
    resetFeatures()
    
def make_ae():
    w = (6*6+2)*PIX
    newPage(w, H)
    drawGrid(w, H)
    drawString('ae', 0, 0, 'Single')
    drawString('ae', 12, 0, 'Double')
    drawString('ae', 24, 0, 'SingleSquare')

def make_spacing():
    sGrid = 'Grid inmIMW'
    sMono = 'Mono inmIMW'
    sProp = 'Prop inmIMW'
    fsGrid = FormattedString(sGrid, font=FONTS['GridSingle'], fontSize=FS)
    fsMono = FormattedString(sMono, font=FONTS['Single'], fontSize=FS)
    fsProp = FormattedString(sProp, font=FONTS['PropSingle'], fontSize=FS)
    w = (max(len(sMono), len(fsProp))*6+2)*PIX
    newPage(w, H*3)
    drawGrid(w, H*3)
    drawString(fsGrid, 0, 18, 'Single')
    drawString(fsMono, 0, 9, 'Single')
    drawString(fsProp, 0, 0, 'Single')

def make_tracking():
    s0 = 'track=0'
    s10 = 'track=10'
    fs10 = FormattedString(s10, tracking=10, font=FONTS['Single'], fontSize=FS)
    w = (len(s10)*7+2)*PIX
    newPage(w, H*2)
    drawGrid(w, H*2)
    drawString(s0, 0, 9, 'Single')
    drawString(fs10, 0, 0, 'Single')

def make_kerning():
    s0 = 'Prop CAPITALS'
    s1 = '\\TeL’ Kernings'
    w = (12*6+2)*PIX
    newPage(w, H*2)
    drawGrid(w, H*2)
    drawString(s0, 0, 9, 'PropSingle')
    drawString(s1, 0, 0, 'PropSingle')

def make_contrastPixelSingle():
    s0 = 'Contrast ACGOco'
    w = (len(s0)*6+2)*PIX
    newPage(w, H*3)
    save()
    drawGrid(w, H*3)
    openTypeFeatures(ss04=False) # Contrast pixel
    drawString(s0, 0, 18, 'Single')
    openTypeFeatures(ss04=True)
    drawString(s0, 0, 9, 'Single', color=(1, 0, 0))
    openTypeFeatures(ss04=False)
    drawString(s0, 0, 9, 'Single', color=(0.5, 0.5, 0.5))
    openTypeFeatures(ss04=True)
    drawString(s0, 0, 0, 'Single')
    resetFeatures()
    restore()

def make_contrastPixelDouble():
    s0 = 'Contrast ACGOco'
    w = (len(s0)*6+2)*PIX
    newPage(w, H*3)
    save()
    drawGrid(w, H*3)
    openTypeFeatures(ss05=False) # No constrast pixel
    drawString(s0, 0, 18, 'Double')
    openTypeFeatures(ss05=False)
    drawString(s0, 0, 9, 'Double', color=(1, 0, 0))
    openTypeFeatures(ss05=True)
    drawString(s0, 0, 9, 'Double', color=(0.5, 0.5, 0.5))
    openTypeFeatures(ss05=True)
    drawString(s0, 0, 0, 'Double')
    resetFeatures()
    restore()

def make_singleDouble():
    s0 = 'ABCabc Single'
    s1 = 'ABCabd Double'
    w = (len(s0)*6+2)*PIX
    newPage(w, H*2)
    drawGrid(w, H*2)
    drawString(s0, 0, 9, 'Single')
    drawString(s1, 0, 0, 'Double')

def make_singleCircleWeights():
    s0 = 'Light Circle'
    s1 = 'Book Circle'
    s2 = 'Regular Circle'
    s3 = 'Medium Circle'
    s4 = 'Bold Circle'
    w = (len(s2)*6+2)*PIX
    newPage(w, H*5)
    drawGrid(w, H*5)
    drawString(s0, 0, 36, 'SingleLight')
    drawString(s1, 0, 27, 'SingleBook')
    drawString(s2, 0, 18, 'Single')
    drawString(s3, 0, 9, 'SingleMedium')
    drawString(s4, 0, 0, 'SingleBold')

def make_singleSquareWeights():
    s0 = 'Light Square'
    s1 = 'Book Square'
    s2 = 'Regular Square'
    s3 = 'Medium Square'
    s4 = 'Bold Square'
    w = (len(s2)*6+2)*PIX
    newPage(w, H*5)
    drawGrid(w, H*5)
    drawString(s0, 0, 36, 'SingleLightSquare')
    drawString(s1, 0, 27, 'SingleBookSquare')
    drawString(s2, 0, 18, 'SingleSquare')
    drawString(s3, 0, 9, 'SingleMediumSquare')
    drawString(s4, 0, 0, 'SingleBoldSquare')

def make_singleLineSquareWeights():
    s0 = 'Lt Line Square'
    s1 = 'Bk Line Square'
    s2 = 'Rg Line Square'
    s3 = 'Md Line Square'
    s4 = 'Bd Line Square'
    w = (len(s2)*6+2)*PIX
    newPage(w, H*5)
    drawGrid(w, H*5)
    drawString(s0, 0, 36, 'SingleLightLineSquare')
    drawString(s1, 0, 27, 'SingleBookLineSquare')
    drawString(s2, 0, 18, 'SingleLineSquare')
    drawString(s3, 0, 9, 'SingleMediumLineSquare')
    drawString(s4, 0, 0, 'SingleBoldLineSquare')

def make_singleLineCircleWeights():
    s0 = 'Lt Line Circle'
    s1 = 'Bk Line Circle'
    s2 = 'Rg Line Circle'
    s3 = 'Md Line Circle'
    s4 = 'Bd Line Circle'
    w = (len(s2)*6+2)*PIX
    newPage(w, H*5)
    drawGrid(w, H*5)
    drawString(s0, 0, 36, 'SingleLightLineCircle')
    drawString(s1, 0, 27, 'SingleBookLineCircle')
    drawString(s2, 0, 18, 'SingleLineCircle')
    drawString(s3, 0, 9, 'SingleMediumLineCircle')
    drawString(s4, 0, 0, 'SingleBoldLineCircle')
    
def make_singleLinePlusWeights():
    s0 = 'Light Plus'
    s1 = 'Book Plus'
    s2 = 'Regular Plus'
    s3 = 'Medium Plus'
    s4 = 'Bold Plus'
    w = (len(s2)*6+2)*PIX
    newPage(w, H*5)
    drawGrid(w, H*5)
    drawString(s0, 0, 36, 'SingleLightPlus')
    drawString(s1, 0, 27, 'SingleBookPlus')
    drawString(s2, 0, 18, 'SinglePlus')
    drawString(s3, 0, 9, 'SingleMediumPlus')
    drawString(s4, 0, 0, 'SingleBoldPlus')
    
   
def XXmake_singleFigures():
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
        
def XXmake_doubleFigures():
    s0 = 'ABC0123456789'
    s1 = 'abc0123456789'
    s2 = 'Fraction 01234/56789'
    w = (len(s0)*6+2)*PIX
    newPage(w, H*3)
    drawGrid(w, H*3)
    drawString(s0, 0, 18, 'Double')
    openTypeFeatures(onum=True, lnum=True, hwid=True, ss01=True, ss02=True, 
        ss04=False, ss05=False, ss06=False, pcap=False, smcp=False, c2sc=False)
    # @@@ drawString(s1, 0, 9, 'PropDouble')
    # Condensed
    openTypeFeatures(onum=True, ss04=False, frac=True)
    # @@@ drawString(s2, 0, 0, 'PropDouble')
    resetFeatures()
        
def make_grid_ai():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['GridSingle'], fontSize=FS)
    fsDouble = ''#FormattedString(s0, font=FONTS['GridDouble'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    drawString(fsSingle+fsDouble, 0, 0, 'Single')
        
def make_mono_ai():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['Single'], fontSize=FS)
    fsDouble = ''#FormattedString(s0, font=FONTS['Double'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, 12*PIX)
    #drawGrid(w, 12*PIX)
    drawString(fsSingle+fsDouble, 0, 1, 'Single')
        
def make_prop_ai():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['PropSingle'], fontSize=FS)
    fsDouble = ''#FormattedString(s0, font=FONTS['PropDouble'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, 12*PIX)
    #drawGrid(w, 12*PIX)
    drawString(fsSingle+fsDouble, 0, 1, 'Single')
        
def make_griddouble_ai():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['GridDouble'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    drawString(fsSingle, 0, 0, 'Single')

def make_monodouble_ai():
    s0 = u'áí'
    fsDouble = FormattedString(s0, font=FONTS['Double'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, 12*PIX)
    #drawGrid(w, 12*PIX)
    drawString(fsDouble, 0, 1, 'Single')
        
def make_propdouble_ai():
    return
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['PropDouble'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, 12*PIX)
    #drawGrid(w, 12*PIX)
    drawString(fsSingle, 0, 1, 'Single')
        
def make_grid_ai_italic():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['GridSingleIt'], fontSize=FS)
    fsDouble = ''#FormattedString(s0, font=FONTS['GridDouble'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    drawString(fsSingle+fsDouble, 0, 0, 'Single')
        
def make_mono_ai_italic():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['SingleIt'], fontSize=FS)
    fsDouble = ''#FormattedString(s0, font=FONTS['Double'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, 12*PIX)
    #drawGrid(w, 12*PIX)
    drawString(fsSingle+fsDouble, 0, 1, 'Single')
        
def make_prop_ai_italic():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['PropSingleIt'], fontSize=FS)
    fsDouble = ''#FormattedString(s0, font=FONTS['PropDouble'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, 12*PIX)
    #drawGrid(w, 12*PIX)
    drawString(fsSingle+fsDouble, 0, 1, 'Single')
        
def make_griddouble_ai_italic():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['GridDoubleIt'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    drawString(fsSingle, 0, 0, 'Single')

def make_monodouble_ai_italic():
    s0 = u'áí'
    fsSingle = FormattedString(s0, font=FONTS['DoubleIt'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, 12*PIX)
    #drawGrid(w, 12*PIX)
    drawString(fsSingle, 0, 1, 'Single')
        
def make_propdouble_ai_italic():
    return 
    s0 = u'áí'
    fsDouble = FormattedString(s0, font=FONTS['PropDoubleIt'], fontSize=FS)
    w = (len(s0)*6+2)*PIX
    newPage(w, 12*PIX)
    #drawGrid(w, 12*PIX)
    drawString(fsDouble, 0, 1, 'Single')
        
def make_smcp():
    s0 = 'Bitcount'
    w = (len(s0)*6+2)*PIX
    newPage(w, H*2)
    drawGrid(w, H*2)
    drawString(s0, 0, 9, 'Single')
    openTypeFeatures(smcp=True, c2sc=False, ss01=False, ss02=False, 
        ss04=True, ss05=True, ss06=True, )
    drawString(s0, 0, 0, 'Single')
    resetFeatures()

def make_c2sc():
    s0 = 'BITCOUNT'
    w = (len(s0)*6+2)*PIX
    fsSingle = FormattedString(s0, font=FONTS['Single'], fontSize=FS)
    openTypeFeatures(smcp=False, c2sc=True)
    fsSingleSC = FormattedString(s0, font=FONTS['Single'], fontSize=FS)
    openTypeFeatures(liga=False, zero=False, onum=False, lnum=False, hwid=False, ss01=False, ss02=False, 
        ss04=False, ss05=False, ss06=False, pcap=False, smcp=False, c2sc=False)
    newPage(w, H*2)
    drawGrid(w, H*2)
    drawString(fsSingle, 0, 9, 'Single')
    drawString(fsSingleSC, 0, 0, 'Single')

def make_condensed():
    s0 = 'Bitcount'
    w = (len(s0)*6+2)*PIX
    newPage(w, H*2)
    drawGrid(w, H*2)
    drawString(s0, 0, 9, 'Single')
    openTypeFeatures(smcp=True, c2sc=False, ss01=False, ss02=False, 
        ss04=True, ss05=False, ss06=False, )
    drawString(s0, 0, 0, 'Single')
    resetFeatures()

def make_prop_condensed():
    s0 = 'Bitcount'
    w = (7*6+2)*PIX
    newPage(w, H*2)
    drawGrid(w, H*2)
    drawString(s0, 0, 9, 'PropSingle')
    openTypeFeatures(smcp=True, c2sc=False, ss01=False, ss02=False, 
        ss04=True, ss05=False, ss06=False, )
    drawString(s0, 0, 0, 'PropSingle')
    resetFeatures()

def make_smcp_condensed(): # 31
    s0 = 'Bitcount'
    w = (len(s0)*6+2)*PIX
    newPage(w, H*2)
    drawGrid(w, H*2)
    drawString(s0, 0, 9, 'Single')
    openTypeFeatures(smcp=True, c2sc=False, ss01=False, ss02=False, 
        ss04=True, ss05=False, ss06=False, )
    drawString(s0, 0, 0, 'Single')
    resetFeatures()

def make_aehfg():
    s = 'aehfg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    drawString(s, 0, 0, 'Single')

def make_aehfg_slanted():
    s = 'aehfg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    drawString(s, 0, 0, 'SingleIt')

def make_aehfg_italic():
    s = 'aehfg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    openTypeFeatures(ss02=False, 
        ss04=False, ss05=True, ss06=False, )
    drawString(s, 0, 0, 'Single')
    resetFeatures()

def make_aehfg_slanted_italic():
    s = 'aehfg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    openTypeFeatures(ss02=False, 
        ss04=False, ss05=True, ss06=False, )
    drawString(s, 0, 0, 'SingleIt')
    resetFeatures()

def make_aehfg_square():
    s = 'aehfg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    drawString(s, 0, 0, 'SingleSquare')

def make_aehfg_square_slanted():
    s = 'aehfg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    drawString(s, 0, 0, 'SingleSquareIt')

def make_aehfg_square_italic():
    s = 'aehfg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    openTypeFeatures(ss02=False, 
        ss04=False, ss05=True, ss06=False, )
    drawString(s, 0, 0, 'SingleSquare')
    resetFeatures()

def make_aehfg_square_slanted_italic():
    s = 'aehfg'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    openTypeFeatures(ss02=False, 
        ss04=False, ss05=True, ss06=False, )
    drawString(s, 0, 0, 'SingleSquareIt')
    resetFeatures()

def make_g():
    s = 'g'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    openTypeFeatures()
    drawString(s, 0, 0, 'Single')
    resetFeatures()

def make_g_italic():
    s = 'g'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H, italic=True)
    openTypeFeatures()
    drawString(s, 0, 0, 'SingleIt')
    resetFeatures()

def make_g_alt():
    s = 'g'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H)
    openTypeFeatures(ss09=True, )
    drawString(s, 0, 0, 'Single')
    resetFeatures()

def make_g_alt_italic():
    s = 'g'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    #drawGrid(w, H, italic=True)
    openTypeFeatures(ss09=True, )
    drawString(s, 0, 0, 'SingleIt')
    resetFeatures()

#    Single
#    ss04 = Cond
#    ss05 = Alternative g

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
    s = '012'
    w = (len(s)*6+2)*PIX
    for cond, slashed, lc, caps in variants:
        newPage(w, H)
        #drawGrid(w, H)
        #openTypeFeatures(onum=True, lnum=True, hwid=True, ss01=True, ss02=True, 
        #    ss04=False, ss05=False, ss06=False, pcap=False, smcp=False, c2sc=False)
        openTypeFeatures(zero=slashed, smcp=caps, 
            ss04=cond, lnum=lc, onum=lc)
        drawString(s, 0.5, 0, 'Single')
        resetFeatures()

def make_pixel_shapes():
    s = 'e'
    w = (len(s)*6+2)*PIX
    for n2 in ('Circle', 'LineCircle', 'Square', 'LineSquare', 'Plus'):
        for n1 in ('Light', 'Book', 'Regular', 'Medium', 'Bold'):
            for it in ('', 'Italic'):
                newPage(w, H)
                #drawGrid(w, H)
                if it:
                    offset = 0.1
                else:
                    offset = 0.35
                drawString(s, offset, 0, 'BitcountMonoSingle-%s%s%s' % (n1, n2, it))
    
def make_OTF_X_ascender():
    s = u'd'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(ss01=True, ss02=True, ss03=True) # Ascender+ and descender+
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_descender():
    s = u'p'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(ss01=True, ss02=True, ss03=True) # Ascender+ and descender+
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_capital():
    s = u'A'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(ss01=True, ss02=True, ss03=True) # Ascender+ and descender+
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_ligatures():
    s = u'flfi'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    openTypeFeatures(liga=False) # Ascender+ and descender+
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(liga=True) # Ascender+ and descender+
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_fraction():
    s = u'1/2'
    w = (len(s)*6)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'PropSingle')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(frac=True) # Fraction
    drawString(s, 0, 1, 'PropSingle')
    resetFeatures()

def make_OTF_X_contrast():
    s = u'A'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(ss04=True) # Contrast pixel    
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_noContrast():
    s = u'O'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Double')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(ss05=True) # No-Contrast pixel    
    drawString(s, 0, 1, 'Double')
    resetFeatures()

def make_OTF_X_force_xheight():
    s = u'i'
    w = (len(s)*6+2)*PIX
    newPage(w, H)
    drawGrid(w, H)
    drawString(s, 0, 0, 'GridSingle')

    newPage(w, H)
    drawGrid(w, H)
    openTypeFeatures(ss06=True) # Force x-height    
    drawString(s, 0, 0, 'GridSingle')
    resetFeatures()

def make_OTF_X_condensed():
    s = u'a'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(ss07=True) # Condensed    
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_italic():
    s = u'a'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(ss08=True) # Condensed    
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_g():
    s = u'g'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(ss09=True) # Alt g    
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_number_case():
    s = u'0123'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(onum=True, lnum=True) # Number case    
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_zero():
    s = u'0'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    drawString(s, 0, 1, 'Single')

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(zero=True) # Slash zero  
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_uc2caps():
    s = u'A'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    openTypeFeatures(c2sc=False) # Small caps   
    drawString(s, 0, 1, 'Single')
    resetFeatures()

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(c2sc=True) # Small caps   
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_lc2caps():
    s = u'a'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H, offsetY=PIX)
    openTypeFeatures(smcp=False) # Small caps   
    drawString(s, 0, 1, 'Single')
    resetFeatures()

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(smcp=True) # Small caps   
    drawString(s, 0, 1, 'Single')
    resetFeatures()

def make_OTF_X_tnum():
    s = u'$123.456,18'
    w = (len(s)*6+2)*PIX
    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(tnum=False, onum=False, ss02=True) # Table figures   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(tnum=True, onum=False, ss02=True) # Small caps   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H+PIX)
    drawGrid(w, H+PIX)
    openTypeFeatures(tnum=False, onum=False, ss02=False) # Table figures   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H+PIX)
    drawGrid(w, H+PIX)
    openTypeFeatures(tnum=True, onum=False, ss02=False) # Small caps   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H)
    drawGrid(w, H)
    openTypeFeatures(tnum=False, onum=True, ss02=False) # Table figures   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H)
    drawGrid(w, H)
    openTypeFeatures(tnum=True, onum=True, ss02=False) # Small caps   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    # Condensed 
    
    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(tnum=False, onum=False, ss07=True, ss02=True) # Table figures   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H+2*PIX)
    drawGrid(w, H+2*PIX)
    openTypeFeatures(tnum=True, onum=False, ss07=True, ss02=True) # Small caps   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H+PIX)
    drawGrid(w, H+PIX)
    openTypeFeatures(tnum=False, onum=False, ss07=True, ss02=False) # Table figures   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H+PIX)
    drawGrid(w, H+PIX)
    openTypeFeatures(tnum=True, onum=False, ss07=True, ss02=False) # Small caps   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H)
    drawGrid(w, H)
    openTypeFeatures(tnum=False, onum=True, ss07=True, ss02=False) # Table figures   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

    newPage(w, H)
    drawGrid(w, H)
    openTypeFeatures(tnum=True, onum=True, ss07=True, ss02=False) # Small caps   
    drawString(s, 0, 0, 'PropSingle')
    resetFeatures()

def make_matrix():
    s = u'/matrix57 /matrix58 /matrix68 /matrix610 /typetr'
    w = ((2*len(s.split('/'))-2)*6+2)*PIX
    newPage(w, H+3*PIX)
    drawGrid(w, H+3*PIX)
    openTypeFeatures(liga=True) # Small caps   
    drawString(s, 0, 2, 'Double')
    
print listOpenTypeFeatures(FONTS['Single'])

# KEEP ORDER, NOT TO CHANGE THE INDEX NUMBER OF THE IMAGES.
make_aehg()   
make_ae()   
make_tracking()
make_spacing()
make_kerning()  
make_contrastPixelSingle() 
make_contrastPixelDouble() 
make_singleDouble()
make_singleCircleWeights()
make_singleSquareWeights()
make_singleLineSquareWeights()
#make_singleFigures()
#make_doubleFigures()
newPage(W, H) # Keep rest in sync
newPage(W, H) 

make_grid_ai()
make_mono_ai()
make_prop_ai()
make_griddouble_ai()
make_monodouble_ai()
make_propdouble_ai()
make_grid_ai_italic()
make_mono_ai_italic()
make_prop_ai_italic()
make_griddouble_ai_italic()
make_monodouble_ai_italic()
make_propdouble_ai_italic()
make_smcp()
make_c2sc()
make_condensed()
make_prop_condensed()
make_smcp_condensed()
make_aehfg()
make_aehfg_slanted()
make_aehfg_italic()
make_aehfg_slanted_italic()
make_aehfg_square()
make_aehfg_square_slanted()
make_aehfg_square_italic()
make_aehfg_square_slanted_italic()
make_g()
make_g_italic()   
make_g_alt()
make_g_alt_italic()
make_zeros()
make_pixel_shapes()

make_singleLineCircleWeights()
make_single_double_aehg()
make_grid_accent_Aaaa()
make_mono_ascender_descender()
make_mono_capital_ascender_descender()
make_singleLinePlusWeights()

make_OTF_X_ascender()
make_OTF_X_descender()
make_OTF_X_capital()
make_OTF_X_ligatures()
make_OTF_X_fraction()
make_OTF_X_contrast()
make_OTF_X_noContrast()
make_OTF_X_force_xheight()
make_OTF_X_condensed()
make_OTF_X_italic()
make_OTF_X_g()
make_OTF_X_number_case()
make_OTF_X_zero()
make_OTF_X_lc2caps()
make_OTF_X_uc2caps()
make_OTF_X_tnum()
make_matrix()

saveImage('../images/referenceImagesX.png', 1)
saveImage('../images/referenceImagesX.pdf', multipage=True)
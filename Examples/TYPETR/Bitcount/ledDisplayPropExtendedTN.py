#
#    Running led animation, example fpr TypeNetwork site.
#
from drawBot import installedFonts, openTypeFeatures, newPage, fill, rect

bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName and not 'Italic' in fontName and 'Mono' in fontName and 'Single' in fontName:
        bitcountNames.append(fontName)

# Size of a pixel in DrawBot units.
PIX = 6

#GRID_COLOR = 0.4, 0.7, 1 
FONTS = {
    # Used layers to simulate unsharp pixel leds.
    'PropSingleLight': 'BitcountPropSingle-LightCircle',
    'PropSingleLightItalic': 'BitcountPropSingle-LightCircleItalic',
    'PropSingleBook': 'BitcountPropSingle-BookCircle',
    'PropSingleBookItalic': 'BitcountPropSingle-BookCircleItalic',
    'PropSingleMediumItalic': 'BitcountPropSingle-MediumCircleItalic',
    'PropSingleMedium': 'BitcountPropSingle-MediumCircle',
    'PropSingleBold': 'BitcountPropSingle-BoldCircle',
    'PropSingleBoldItalic': 'BitcountPropSingle-BoldCircleItalic',
    'PropSingle': 'BitcountPropSingle-RegularCircle',
    'PropSingleItalic': 'BitcountPropSingle-RegularCircleItalic',
    # Other font options. Make sure that the spacing types match for layers.
    'GridSingle': 'BitcountGridSingle-RegularCircle',
    'GridDouble': 'BitcountGridDouble-RegularCircle',
    'SingleMediumItalic': 'BitcountMonoSingle-MediumCircleItalic',
    'SingleMedium': 'BitcountMonoSingle-MediumCircle',
    'SingleBold': 'BitcountMonoSingle-BoldCircle',
    'SingleBoldItalic': 'BitcountMonoSingle-BoldCircleItalic',
    'Single': 'BitcountMonoSingle-RegularCircle',
    'Double': 'BitcountMonoDouble-RegularCircle',
    'SingleItalic': 'BitcountMonoSingle-RegularCircleItalic',
    'DoubleItalic': 'BitcountMonoDouble-RegularCircleItalic',
    'SingleSquare': 'BitcountMonoSingle-RegularSquare',
    'SoubleSquare': 'BitcountMonoDouble-RegularSquare',
    'SingleBook': 'BitcountMonoSingle-BookCircle',
    'DoubleBook': 'BitcountMonoDouble-BookCircle',
    'SingleBookSquare': 'BitcountMonoSingle-BookSquare',
    'DoubleBookSquare': 'BitcountMonoDouble-BookSquare',
    'SingleBold': 'BitcountMonoSingle-BoldCircle',
    'DoubleBold': 'BitcountMonoDouble-BoldCircle',
    'SingleBookOpenSquare': 'BitcountMonoSingle-BookOpenSquare',
    'DoubleBookOpenSquare': 'BitcountMonoDouble-BookOpenSquare',
    'SingleBookOpenCircle': 'BitcountMonoSingle-BookOpenCircle',
    'DoubleBookOpenCircle': 'BitcountMonoDouble-BookOpenCircle',

}
H = 9*PIX
W = 32*PIX
X = Y = PIX
FS = PIX*10
FRAMES = 16

HIGHLIGHT = False # Leds appear to be more 3D



def drawString(s, px, py, fontName, color=None, gridColor=None):
    if fontName in FONTS:
        fontName = FONTS[fontName]
    font(fontName)
    fontSize(FS)
    stroke(None)
    if color is not None:
        r, g, b, t = color
        fill(r, g, b, t)
    else:
        fill(color or 0)
    text(s, (px, py))

def makeFlash(s, w, h, px, py, color1=None, color2=None, flashSpeed=4):
    if color1 is None:
        r1, g1, b1 = 1, 0, 0
    else:
        r1, g1, b1 = color1        
    if color2 is None:
        r2, g2, b2 = 0.2, 0, 0
    else:
        r2, g2, b2 = color2     
    for n in range(flashSpeed):
        newPage(w, h)
        fill(0)
        rect(0, 0, w, h)
        drawString(s, px, py, 'PropSingleBold', (r1, g1, b1, 0.2))
        drawString(s, px, py, 'PropSingleMedium', (r1, g1, b1, 0.5))
        if HIGHLIGHT:
            drawString(s, px, py, 'PropSingle', (r1*0.9, g1*0.9, b1*0.9, 1))
            drawString(s, px-1, py+1, 'PropSingleLight', (r1, g1, b1, 1))
        else:
            drawString(s, px, py, 'PropSingle', (r1, g1, b1, 1))

    for n in range(flashSpeed):
        newPage(w, h)
        fill(0)
        rect(0, 0, w, h)
        drawString(s, px, py, 'PropSingleBold', (r2, g2, b2, 0.2))
        drawString(s, px, py, 'PropSingleMedium', (r2, g2, b2, 0.5))
        if HIGHLIGHT:
            drawString(s, px, py, 'PropSingle', (r2*0.9, g2*0.9, b2*0.9, 1))
            drawString(s, px-1, py+1, 'PropSingleLight', (r2, g2, b2, 1))
        else:
            drawString(s, px, py, 'PropSingle', (r2, g2, b2, 1))

def makeRunningLeds(s, w, h, px, py, speed=1):
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)
    drawString(s, px, py, 'PropSingleBoldItalic', (0.3, 0, 0, 1))
    drawString(s, px, py, 'PropSingleMediumItalic', (0.6, 0.0, 0, 1))
    if HIGHLIGHT:
        drawString(s, px, py, 'PropSingleItalic', (0.8, 0, 0, 1))
        drawString(s, px-1, py+1, 'PropSingleLightItalic', (1, 0, 0, 1))
    else:
        drawString(s, px, py, 'PropSingleItalic', (1, 0, 0, 1))  

if __name__ == '__main__':
           
    openTypeFeatures(onum=True, lnum=True, hwid=True, ss01=True, ss02=True, 
        ss04=False, ss05=False, ss06=True, pcap=False, smcp=False, c2sc=False)
      
    line1 = 'Separate Bitcount fonts @ $10.10'
    line2 = u'Package of all 300 Bitcounts: $101'
    speed = 4
    w = (28*6+2+10)*PIX
    h = 11*PIX
    for n in range(45):
        makeRunningLeds(line1, w, h, w-(1+n)*PIX*speed+9*PIX, 2.5*PIX, speed)
    for flash in range(4):
        makeFlash(line1, w, h, 9*PIX, 2.5*PIX)
    #for n in range(int(round(len(message)*6))):
    #    makeRunningLeds(message, w, h, -(1+n)*PIX*speed, 3*PIX, speed)
    for flash in range(6):
        makeFlash(line2, w, h, 7*PIX, 2.5*PIX, color1=(0.3, 0.9, 0), color2=(0.1, 0.3, 0))
           
    openTypeFeatures(liga=False, zero=False, onum=False, lnum=False, hwid=False, ss01=False, ss02=False, 
        ss04=False, ss05=False, ss06=False, pcap=False, smcp=False, c2sc=False)
            
    saveImage('_export/runningLedsPropExtendedTN.gif')


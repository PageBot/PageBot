#
#    Typetr logo animation
#

bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName and not 'Italic' in fontName and 'Mono' in fontName and 'Single' in fontName:
        bitcountNames.append(fontName)

PIX = 6


GRID_COLOR = 0.4, 0.7, 1 
FONTS = {
    'GridSingle': 'BitcountGridSingle-RegularCircle',
    'GridDouble': 'BitcountGridDouble-RegularCircle',
    'SingleMediumItalic': 'BitcountMonoSingle-SemiboldCircleItalic',
    'SingleMedium': 'BitcountMonoSingle-SemiboldCircle',
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

    'GridDoubleMediumItalic': 'BitcountGridDouble-SemiboldCircleItalic',
    'GridDoubleMedium': 'BitcountGridDouble-SemiboldCircle',
    'GridDoubleBold': 'BitcountGridDouble-BoldCircle',
    'GridDoubleBoldItalic': 'BitcountGridDouble-BoldCircleItalic',
    'GridDouble': 'BitcountGridDouble-RegularCircle',
    'GridDoubleItalic': 'BitcountGridDouble-RegularCircleItalic',
}
H = 9*PIX
W = 32*PIX
X = Y = PIX
FS = PIX*10
FRAMES = 16



def drawString(s, px, py, fontName, color=None, gridColor=None):
       
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
    text(s, (px, py))

def makeFlash(s, w, h, px, py):
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)
    drawString(s, px, py, 'GridDoubleBold', (0.3, 0, 0))
    drawString(s, px, py, 'GridDoubleMedium', (0.6, 0.0, 0))
    drawString(s, px, py, 'GridDouble', (1, 0, 0))
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)

def makeRunningLeds(s, w, h, px, py, speed=1):
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)
    drawString(s, px, py, 'GridDoubleBoldItalic', (0.3, 0, 0))
    drawString(s, px, py, 'GridDoubleMediumItalic', (0.6, 0.0, 0))
    drawString(s, px, py, 'GridDoubleItalic', (1, 0, 0))
    
message = 'Led 5x7 pixels'# áçcëñt'
speed = 1
w = (18*6+2+10)*PIX
h = 9*PIX
for n in range(100):
    makeRunningLeds(message, w, h, w-(1+n)*PIX*speed, 2*PIX, speed)
for flash in range(10):
    makeFlash(message, w, h, 20*PIX, 2*PIX)
#for n in range(int(round(len(message)*6))):
#    makeRunningLeds(message, w, h, -(1+n)*PIX*speed, 3*PIX, speed)
for flash in range(10):
    makeFlash(u'05:07 Bitcount Grid 18°', w, h, 3*PIX, 2*PIX)
       
        
saveImage('../images/runningLeds.gif')
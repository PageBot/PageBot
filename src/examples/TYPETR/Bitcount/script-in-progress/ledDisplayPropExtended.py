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

    'PropSingleMediumItalic': 'BitcountPropSingle-SemiboldCircleItalic',
    'PropSingleMedium': 'BitcountPropSingle-SemiboldCircle',
    'PropSingleBold': 'BitcountPropSingle-BoldCircle',
    'PropSingleBoldItalic': 'BitcountPropSingle-BoldCircleItalic',
    'PropSingle': 'BitcountPropSingle-RegularCircle',
    'PropSingleItalic': 'BitcountPropSingle-RegularCircleItalic',

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
        r, g, b, t = color
        fill(r, g, b, t)
    else:
        fill(color or 0)
    text(s, (px, py))

def makeFlash(s, w, h, px, py, color=None):
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)
    if color is None:
        r, g, b = 1, 9, 0
    else:
        r, g, b = color        
    drawString(s, px, py, 'PropSingleBold', (r, g, b, 0.2))
    drawString(s, px, py, 'PropSingleMedium', (r, g, b, 0.5))
    drawString(s, px, py, 'PropSingle', (r, g, b, 1))
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)

def makeRunningLeds(s, w, h, px, py, speed=1):
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)
    drawString(s, px, py, 'PropSingleBoldItalic', (0.3, 0, 0, 1))
    drawString(s, px, py, 'PropSingleMediumItalic', (0.6, 0.0, 0, 1))
    drawString(s, px, py, 'PropSingleItalic', (1, 0, 0, 1))
    
openTypeFeatures(onum=True, lnum=True, hwid=True, ss01=True, ss02=True, 
    ss04=False, ss05=False, ss06=True, pcap=False, smcp=False, c2sc=False)
    
message = 'Dísplãy pìxëls'# áçcëñt'
speed = 2
w = (18*6+2+10)*PIX
h = 12*PIX
for n in range(45):
    makeRunningLeds(message, w, h, w-(1+n)*PIX*speed, 3*PIX, speed)
for flash in range(4):
    makeFlash(message, w, h, 30*PIX, 3*PIX)
#for n in range(int(round(len(message)*6))):
#    makeRunningLeds(message, w, h, -(1+n)*PIX*speed, 3*PIX, speed)
for flash in range(10):
    makeFlash(u'23:10 Bitcount Prop 23°', w, h, 2*PIX, 3*PIX, color=(0, 1, 0))
       
openTypeFeatures(liga=False, zero=False, onum=False, lnum=False, hwid=False, ss01=False, ss02=False, 
    ss04=False, ss05=False, ss06=False, pcap=False, smcp=False, c2sc=False)
        
saveImage('../images/runningLedsPropExtended.gif')
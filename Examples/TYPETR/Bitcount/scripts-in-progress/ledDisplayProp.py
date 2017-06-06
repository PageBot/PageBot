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
        r, g, b = color
        fill(r, g, b)
    else:
        fill(color or 0)
    text(s, (px, py))

def makeFlash(s, w, h, px, py):
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)
    drawString(s, px, py, 'PropSingleBold', (0.3, 0, 0))
    drawString(s, px, py, 'PropSingleMedium', (0.6, 0.0, 0))
    drawString(s, px, py, 'PropSingle', (1, 0, 0))
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)

def makeRunningLeds(s, w, h, px, py, speed=1):
    newPage(w, h)
    fill(0)
    rect(0, 0, w, h)
    drawString(s, px, py, 'PropSingleBoldItalic', (0.3, 0, 0))
    drawString(s, px, py, 'PropSingleMediumItalic', (0.6, 0.0, 0))
    drawString(s, px, py, 'PropSingleItalic', (1, 0, 0))
    
message = 'Dísplãy pïxëls'# áçcëñt'
speed = 1
w = (len(message)*6+2+10)*PIX
h = 12*PIX
for n in range(int(round(len(message)*6))):
    makeRunningLeds(message, w, h, w-(1+n)*PIX*speed, 3*PIX, speed)
for flash in range(10):
    makeFlash(message, w, h, PIX, 3*PIX)
#for n in range(int(round(len(message)*6))):
#    makeRunningLeds(message, w, h, -(1+n)*PIX*speed, 3*PIX, speed)
for flash in range(10):
    makeFlash(u'16:10 Bitcount Prop 12°', w, h, PIX, 3*PIX)
       
        
saveImage('../images/runningLedsProp.gif')
#
#    Typetr logo animation
#

bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName and not 'Italic' in fontName and 'Mono' in fontName and 'Single' in fontName:
        bitcountNames.append(fontName)

PIX = 50

GRID_COLOR = 0.4, 0.7, 1 
FONTS = {
    'GridSingle': 'BitcountGridSingle-RegularCircle',
    'GridDouble': 'BitcountGridDouble-RegularCircle',
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

def drawString(s, px, py, fontName, color=None, gridColor=None, showLayer=False):
    if 0 and showLayer:
        fill(0.8, 0.8, 0.8, 0.25)
        stroke(None)
        rect(X+(px-1)*PIX, Y+(py-1)*PIX, (4*6+1)*PIX, 9*PIX)
 
    if showLayer or gridColor is not None:
        r, g, b = color or gridColor or GRID_COLOR
        stroke(r, g, b)
        strokeWidth(PIX/20)
        fill(None)
        rect(X+(px-1)*PIX, Y+(py-1)*PIX, (4*6+1)*PIX, 9*PIX)
       
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

    
def XXXdrawGrid(w, h, offsetX=0, offsetY=0, color=None):
    newPath()
    for x in range(w):
        moveTo((PIX*(x+offsetX), Y+PIX*offsetY))
        lineTo((PIX*(x+offsetX), Y+PIX*(h-offsetY)))
    for y in range(h):
        moveTo((X+PIX*offsetX, PIX*(y+1+offsetY)))
        lineTo((X+PIX*(w-2-offsetX), PIX*(y-1+offsetY)))
    fill(None)
    r, g, b = color or GRID_COLOR
    stroke(r, g, b)
    strokeWidth(PIX/20)
    drawPath()
        
def make_perspective_Bitc(frame, drawNames=False, randomFont=False, showLayer=False):
    s = 'Bitc'
    Fy = 0.3
    Fx = 0.2
    w = len(s)*6+2
    newPage(PIX*(w-5), PIX*(w-8))
    save()
    translate(30, -50)
    skew(-40)
    rotate(20)
    scale(1, 0.4)
    z = frame*3/4
    
    F1 = FONTS['SingleBold']
    if randomFont:
        F2 = choice(bitcountNames)
        F3 = choice(bitcountNames)
    else:
        F2 = FONTS['SingleSquare']
        F3 = FONTS['SingleBook']
    
    drawString(s, 6+0*z*Fx, 0*z*Fy, F1, color=(0.2, 0.1, 0.2), gridColor=GRID_COLOR, showLayer=showLayer)
    drawString(s, 6+1*z*Fx, 1*z*Fy, F2, color=(0.7, 0.1, 0.2), showLayer=showLayer)
    drawString(s, 6+2*z*Fx, 2*z*Fy, F3, color=(1, 0.6, 0.1), showLayer=showLayer)
    restore()
    if drawNames:
        x = 50
        fontSize(32)
        font(F1)
        fill(0.2, 0.1, 0.2)
        text(F1, (x, 720))
        font(F2)
        fill(0.7, 0.1, 0.2)
        text(F2, (x, 760))
        font(F3)
        fill(0.8, 0.5, 0.1)
        text(F3, (x, 800))
    

for n in range(15):
    make_perspective_Bitc(0, randomFont=True)   
for n in range(5):
    make_perspective_Bitc(0)   
for frame in range(FRAMES):
    make_perspective_Bitc(frame, drawNames=True)   
for n in range(15    ):
    make_perspective_Bitc(FRAMES, drawNames=True, showLayer=True)   
for frame in range(FRAMES):
    make_perspective_Bitc(FRAMES-frame, drawNames=True)   
for n in range(5):
    make_perspective_Bitc(0)   
        
saveImage('../images/referenceImages2.gif')
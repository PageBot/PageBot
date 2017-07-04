
from random import shuffle

GLYPHNAMES = ['Instance@Bold_Circle', 'Instance@Bold_Line_Circle', 'Instance@Bold_Line_Square', 'Instance@Bold_Plus', 'Instance@Bold_Square', 'Instance@Book_Circle', 'Instance@Book_Line_Circle', 'Instance@Book_Line_Square', 'Instance@Book_Plus', 'Instance@Book_Square', 'Instance@Light_Circle', 'Instance@Light_Line_Circle', 'Instance@Light_Line_Square', 'Instance@Light_Plus', 'Instance@Light_Square', 'Instance@Medium_Circle', 'Instance@Medium_Line_Circle', 'Instance@Medium_Line_Square', 'Instance@Medium_Plus', 'Instance@Medium_Square', 'Instance@Regular_Circle', 'Instance@Regular_Line_Circle', 'Instance@Regular_Line_Square', 'Instance@Regular_Plus', 'Instance@Regular_Square', 'InstanceItalic@Bold_Circle', 'InstanceItalic@Bold_Line_Circle', 'InstanceItalic@Bold_Line_Square', 'InstanceItalic@Bold_Plus', 'InstanceItalic@Bold_Square', 'InstanceItalic@Book_Circle', 'InstanceItalic@Book_Line_Circle', 'InstanceItalic@Book_Line_Square', 'InstanceItalic@Book_Plus', 'InstanceItalic@Book_Square', u'InstanceItalic@Light_Circle', 'InstanceItalic@Light_Line_Circle', 'InstanceItalic@Light_Line_Square', u'InstanceItalic@Light_Plus', 'InstanceItalic@Light_Square', 'InstanceItalic@Medium_Circle', 'InstanceItalic@Medium_Line_Circle', 'InstanceItalic@Medium_Line_Square', 'InstanceItalic@Medium_Plus', 'InstanceItalic@Medium_Square', 'InstanceItalic@Regular_Circle', 'InstanceItalic@Regular_Line_Circle', 'InstanceItalic@Regular_Line_Square', 'InstanceItalic@Regular_Plus', 'InstanceItalic@Regular_Square']
GLYPHNAMES.sort()
print '\n'.join(GLYPHNAMES)
print len(GLYPHNAMES) 

def drawA(fs, frame):
    PIX = 80
    LM = 80 + frame*10
    text(fs, (LM+PIX, LM))
    text(fs, (LM+2*PIX, LM))
    text(fs, (LM+4*PIX, LM))

    text(fs, (LM, LM+PIX))
    text(fs, (LM+3*PIX, LM+PIX))
    text(fs, (LM+4*PIX, LM+PIX))

    text(fs, (LM+PIX, LM+2*PIX))
    text(fs, (LM+2*PIX, LM+2*PIX))
    text(fs, (LM+3*PIX, LM+2*PIX))
    text(fs, (LM+4*PIX, LM+2*PIX))

    text(fs, (LM+3*PIX, LM+3*PIX))
    text(fs, (LM+4*PIX, LM+3*PIX))

    text(fs, (LM+PIX, LM+4*PIX))
    text(fs, (LM+2*PIX, LM+4*PIX))
    text(fs, (LM+3*PIX, LM+4*PIX))


W = H = 750
glyphNames = []
glyphNamesItalic = []
for glyphName in GLYPHNAMES:
    #if 'Circle' in glyphName:
    #    continue
    if 'Square' in glyphName:
        continue
    if 'Plus' in glyphName:
        continue
    if 'Line' in glyphName:
        continue
    #if not 'Line' in glyphName:
    #    continue
    if not 'Italic' in glyphName:
        glyphNames.append(glyphName)
    else:
        glyphNamesItalic.append(glyphName)

if 0: # Italic
    glyphNames = glyphNamesItalic

WEIGHTS = (
    'Instance@Bold_Circle',
    'Instance@Medium_Circle',
    'Instance@Regular_Circle',
    'Instance@Book_Circle',
    'Instance@Light_Circle',
)

glyphNames = []
for glyphName in WEIGHTS:
    for n in range(5):
        glyphNames.append(glyphName)
        
print glyphNames, 'InstanceItalic@Regular_Square' in glyphNames
            
   
if 1: # Animated pixesl as "a"

    colors = []
    glyphNames = glyphNames
    #shuffle(glyphNames)
    FRAMES = len(glyphNames)
    for frame in range(len(glyphNames)):
        t = 0
        if random() < 100:
            # Blue
            #colors.append((random()*0.2, random()*0.5, random()*0.5+0.5, 0.8))
            colors.append((random()*0.2*frame/FRAMES, random()*0.5*frame/FRAMES, random()*0.5+0.5*frame/FRAMES, 0.8))
            # Red
            #colors.append((random()*0.5+0.5, random()*0.5, random(), 0.8))
        else:
            colors.append((1, 1, 1, 0.8))
        while t <= 0.8:
            newPage(W, H)
            for index, glyphName in enumerate(glyphNames[0:frame]):
                if index != frame-1:
                    fs = FormattedString('', fontSize=800, font='Bitcount-Pixels', fill=colors[index])
                    fs.appendGlyph(glyphName)
                    drawA(fs, index)
            if frame:
                r, g, b, _ = colors[-1]
                fs = FormattedString('', fontSize=800, font='Bitcount-Pixels', fill=(r, g, b, t))
                fs.appendGlyph(glyphName)
                drawA(fs, index)
                #fs = FormattedString(glyphName, fontSize=7, font='Verdana', fill=0)
                #text(fs, (100, 100))
            t += 0.8
    
    saveImage('ShadowOverlayA_1.gif')


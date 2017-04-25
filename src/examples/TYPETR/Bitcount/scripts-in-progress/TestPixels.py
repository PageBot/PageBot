
from random import shuffle

GLYPHNAMES = ['Instance@Bold_Circle', 'Instance@Bold_Line_Circle', 'Instance@Bold_Line_Square', 'Instance@Bold_Plus', 'Instance@Bold_Square', 'Instance@Book_Circle', 'Instance@Book_Line_Circle', 'Instance@Book_Line_Square', 'Instance@Book_Plus', 'Instance@Book_Square', 'Instance@Light_Circle', 'Instance@Light_Line_Circle', 'Instance@Light_Line_Square', 'Instance@Light_Plus', 'Instance@Light_Square', 'Instance@Medium_Circle', 'Instance@Medium_Line_Circle', 'Instance@Medium_Line_Square', 'Instance@Medium_Plus', 'Instance@Medium_Square', 'Instance@Regular_Circle', 'Instance@Regular_Line_Circle', 'Instance@Regular_Line_Square', 'Instance@Regular_Plus', 'Instance@Regular_Square', 'InstanceItalic@Bold_Circle', 'InstanceItalic@Bold_Line_Circle', 'InstanceItalic@Bold_Line_Square', 'InstanceItalic@Bold_Plus', 'InstanceItalic@Bold_Square', 'InstanceItalic@Book_Circle', 'InstanceItalic@Book_Line_Circle', 'InstanceItalic@Book_Line_Square', 'InstanceItalic@Book_Plus', 'InstanceItalic@Book_Square', u'InstanceItalic@Light_Circle', 'InstanceItalic@Light_Line_Circle', 'InstanceItalic@Light_Line_Square', u'InstanceItalic@Light_Plus', 'InstanceItalic@Light_Square', 'InstanceItalic@Medium_Circle', 'InstanceItalic@Medium_Line_Circle', 'InstanceItalic@Medium_Line_Square', 'InstanceItalic@Medium_Plus', 'InstanceItalic@Medium_Square', 'InstanceItalic@Regular_Circle', 'InstanceItalic@Regular_Line_Circle', 'InstanceItalic@Regular_Line_Square', 'InstanceItalic@Regular_Plus', 'InstanceItalic@Regular_Square']
GLYPHNAMES.sort()
print '\n'.join(GLYPHNAMES)
print len(GLYPHNAMES) 

def drawA(fs):
    PIX = 80
    LM = 80
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


W = H = 540
glyphNames = []
glyphNamesItalic = []
for glyphName in GLYPHNAMES:
    #if 'Circle' in glyphName:
    #    continue
    #if 'Square' in glyphName:
    #    continue
    #if 'Plus' in glyphName:
    #    continue
    #if not 'Line' in glyphName:
    #    continue
    if not 'Italic' in glyphName:
        glyphNames.append(glyphName)
    else:
        glyphNamesItalic.append(glyphName)

if 0: # Italic
    glyphNames = glyphNamesItalic

print glyphNames, 'InstanceItalic@Regular_Square' in glyphNames
            
if 0: # Animated super-imposed.
    colors = []
    glyphNames = glyphNames*2
    shuffle(glyphNames)
    for frame in range(len(glyphNames)):
        t = 0
        if random() < 0.7:
            # Blue
            #colors.append((random()*0.2, random()*0.5, random()*0.5+0.5, 0.8))
            # Red
            colors.append((random()*0.5+0.5, random()*0.5, random(), 0.8))
        else:
            colors.append((1, 1, 1, 0.8))
        while t <= 0.8:
            newPage(W, H)
            for index, glyphName in enumerate(glyphNames[0:frame]):
                if index != frame-1:
                    fs = FormattedString('', fontSize=2000, font='Bitcount-Pixels', fill=colors[index])
                    fs.appendGlyph(glyphName)
                    text(fs, (100, 100))
            if frame:
                r, g, b, _ = colors[-1]
                fs = FormattedString('', fontSize=2000, font='Bitcount-Pixels', fill=(r, g, b, t))
                fs.appendGlyph(glyphName)
                text(fs, (100, 100))

                #fs = FormattedString(glyphName, fontSize=7, font='Verdana', fill=0)
                #text(fs, (100, 100))
            t += 0.2
            
    saveImage('testAllPixelsOverlay.gif')
        
elif 1: # Animated pixesl as "a"

    colors = []
    glyphNames = glyphNames*2
    shuffle(glyphNames)
    for frame in range(len(glyphNames)):
        t = 0
        if random() < 0.5:
            # Blue
            #colors.append((random()*0.2, random()*0.5, random()*0.5+0.5, 0.8))
            # Red
            colors.append((random()*0.5+0.5, random()*0.5, random(), 0.8))
        else:
            colors.append((1, 1, 1, 0.8))
        while t <= 0.8:
            newPage(W, H)
            for index, glyphName in enumerate(glyphNames[0:frame]):
                if index != frame-1:
                    fs = FormattedString('', fontSize=800, font='Bitcount-Pixels', fill=colors[index])
                    fs.appendGlyph(glyphName)
                    drawA(fs)
            if frame:
                r, g, b, _ = colors[-1]
                fs = FormattedString('', fontSize=800, font='Bitcount-Pixels', fill=(r, g, b, t))
                fs.appendGlyph(glyphName)
                drawA(fs)
                #fs = FormattedString(glyphName, fontSize=7, font='Verdana', fill=0)
                #text(fs, (100, 100))
            t += 0.2

    saveImage('AllPixelsOverlayA_7.gif')

else: # As example grid of 18x18 combinations
    if 0: # Italic
        glyphNames = glyphNamesItalic
    S = 50    
    for x in range(18):
        for y in range(18):
            n1 = choice(glyphNames)
            n2 = choice(glyphNames)
            n3 = choice(glyphNames)
            for n in (n1, n2, n3):
                fs = FormattedString('', fontSize=250, font='Bitcount-Pixels', fill=(random(), random(), random(), 0.8))
                fs.appendGlyph(n)
                text(fs, (S+10+x*S, S+10+y*S))
            
    saveImage('testAllPixelsOverlay.png')


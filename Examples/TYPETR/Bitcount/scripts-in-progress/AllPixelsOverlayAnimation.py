
from random import shuffle

def run():
    GLYPHNAMES = ['Instance@Bold_Circle', 'Instance@Bold_Line_Circle', 'Instance@Bold_Line_Square', 'Instance@Bold_Plus', 'Instance@Bold_Square', 'Instance@Book_Circle', 'Instance@Book_Line_Circle', 'Instance@Book_Line_Square', 'Instance@Book_Plus', 'Instance@Book_Square', 'Instance@Light_Circle', 'Instance@Light_Line_Circle', 'Instance@Light_Line_Square', 'Instance@Light_Plus', 'Instance@Light_Square', 'Instance@Medium_Circle', 'Instance@Medium_Line_Circle', 'Instance@Medium_Line_Square', 'Instance@Medium_Plus', 'Instance@Medium_Square', 'Instance@Regular_Circle', 'Instance@Regular_Line_Circle', 'Instance@Regular_Line_Square', 'Instance@Regular_Plus', 'Instance@Regular_Square', 'InstanceItalic@Bold_Circle', 'InstanceItalic@Bold_Line_Circle', 'InstanceItalic@Bold_Line_Square', 'InstanceItalic@Bold_Plus', 'InstanceItalic@Bold_Square', 'InstanceItalic@Book_Circle', 'InstanceItalic@Book_Line_Circle', 'InstanceItalic@Book_Line_Square', 'InstanceItalic@Book_Plus', 'InstanceItalic@Book_Square', u'InstanceItalic@Light_Circle', 'InstanceItalic@Light_Line_Circle', 'InstanceItalic@Light_Line_Square', u'InstanceItalic@Light_Plus', 'InstanceItalic@Light_Square', 'InstanceItalic@Medium_Circle', 'InstanceItalic@Medium_Line_Circle', 'InstanceItalic@Medium_Line_Square', 'InstanceItalic@Medium_Plus', 'InstanceItalic@Medium_Square', 'InstanceItalic@Regular_Circle', 'InstanceItalic@Regular_Line_Circle', 'InstanceItalic@Regular_Line_Square', 'InstanceItalic@Regular_Plus', 'InstanceItalic@Regular_Square']
    GLYPHNAMES.sort()
    print '\n'.join(GLYPHNAMES)
    print len(GLYPHNAMES) 

    W = H = 800
    glyphNames = []
    glyphNamesItalic = []
    for glyphName in GLYPHNAMES:
        if not 'Italic' in glyphName:
            glyphNames.append(glyphName)
        else:
            glyphNamesItalic.append(glyphName)
            
    if 1:
        for n in range(3):
            colors = []
            shuffle(glyphNames)
            for frame in range(len(glyphNames)):
                newPage(W, H)
                colors.append((random(), random(), random(), 0.4))
                for index, glyphName in enumerate(GLYPHNAMES[0:frame]):
                    fs = FormattedString('', fontSize=2000, font='Bitcount-Pixels', fill=colors[index])
                    fs.appendGlyph(glyphName)
                    text(fs, (100, 100))
                    fill(None)

        saveImage('testAllPixelsOverlay.gif')
            

    else:
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
                
        saveImage('testAllPixelsOverlay.pdf')

if __name__ == '__main__':
    run()

    
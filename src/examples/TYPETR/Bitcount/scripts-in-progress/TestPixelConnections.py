


GLYPHNAMES = ('Instance@Light_Square', 
'Instance@Regular_Square', 
'Instance@Book_Line_Square', 
'Instance@Bold_Circle', 
'InstanceItalic@Book_Circle', 
'InstanceItalic@Medium_Circle', 
'InstanceItalic@Book_Line_Square', 
'Instance@Medium_Circle', 
'Instance@Light_Circle', 
'InstanceItalic@Bold_Plus', 
'InstanceItalic@Bold_Square', 
'InstanceItalic@Bold_Line_Circle', 
'InstanceItalic@Medium_Square', 
'InstanceItalic@Regular_Line_Circle', 
'InstanceItalic@Regular_Square', 
'Instance@Book_Circle', 
'Instance@Medium_Square', 
'InstanceItalic@Book_Plus', 
'Instance@Book_Square', 
'Instance@Light_Plus_Italic', 
'InstanceItalic@Book_Line_Circle', 
'Instance@Regular_Line_Square', 
'InstanceItalic@Bold_Circle', 
'Instance@Bold_Line_Square', 
'InstanceItalic@Medium_Line_Circle', 
'InstanceItalic@Regular_Circle', 
'Instance@Regular_Line_Circle', 
'Instance@Light_Plus', 
'Instance@Medium_Line_Square', 
'InstanceItalic@Medium_Line_Square', 
'InstanceItalic@Regular_Line_Square', 
'Instance@Book_Plus', 
'InstanceItalic@Book_Square', 
'Instance@Regular_Plus', 
'Instance@Bold_Square', 
'Instance@Light_Line_Circle', 
'Instance@Bold_Plus', 
'InstanceItalic@Medium_Plus', 
'InstanceItalic@Light_Line_Square', 
'Instance@Medium_Line_Circle', 
'Instance@Regular_Circle', 
'InstanceItalic@Regular_Plus', 
'InstanceItalic@Light_Square', 
'InstanceItalic@Bold_Line_Square', 
'Instance@Book_Line_Circle', 
'Instance@Light_Line_Square', 
'Instance@Medium_Plus', 
'Instance@Bold_Line_Circle', 
'InstanceItalic@Light_Line_Circle', 
)
glyphNames = []
glyphNamesItalic = []
for glyphName in GLYPHNAMES:
    if not 'Italic' in glyphName:
        glyphNames.append(glyphName)
    else:
        glyphNamesItalic.append(glyphName)
        
"""
for glyphName in GLYPHNAMES:
    if 'Italic' in glyphName: 
        continue
    fontSize(200)
    fill(random(), random(), random(), 0.1)
    fs = FormattedString('', fontSize=5000, font='Bitcount-Pixels', fill=(random(), random(), random(), 0.1))
    fs.appendGlyph(glyphName)
    text(fs, (200, 200))"""

glyphNames = glyphNamesItalic
S = 50    
for x in range(18):
    for y in range(18):
        n1 = choice(glyphNames)
        n2 = choice(glyphNames)
        n3 = choice(glyphNames)
        for n in (n1, n2, n3):
            ss = 400/5
            fs = FormattedString('', fontSize=ss, font='Bitcount-Pixels', fill=(random(), random(), random(), 0.8))
            fs.appendGlyph(n)
            for xx in range(5):
                for yy in range(5):
                    text(fs, (xx*ss/10+S+10+x*S+yy*14/100*ss/10, yy*ss/10+S+10+y*S))
            
saveImage('testPixels.pdf')
        
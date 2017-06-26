# Show all installed font names that have "Caslon" inside
for fontName in installedFonts():
    if 'Caslon' in fontName:
        print fontName
        
# Get function that goes from font name to font path
from pagebot.fonttoolbox.objects.font import getFontPathOfFont, Font

# Get the path
path = getFontPathOfFont('ACaslonPro-BoldItalic')
# Make a PageBot font
f = Font(path)
print f.info.familyName

# Get a PageBot glyph object
g = f['A']
print g.name, g.width
# Print the kerning pairs that have "A" on the left and their values.
for pair, value in f.kerning.items():
    if pair[0] == g.name:
        print pair, value
        
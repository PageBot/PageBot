# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#    modifyTTFont.py
#
#    Although not really intended as such, PageBot (in combination with fonttools),
#    can be use to alter and save existing TTF/OTF font files.

from pagebot.fonttoolbox.objects.family import guessFamiliesByPatterns
family = guessFamiliesByPatterns('Georgia')['Georgia']
font = family.fontStyles['Normal'][0]
print('Font path %s' % font.path)

# Assume that we want to increment all spacing by 1/8em, calculate them from the
# font.info.unitsPerEm, as we don't know the size of units.
# Use the calculated increment value also to change the name of font and style.
# Note that for simplicity of the example, the family is not change, nor is the font installed.
INCREMENT = font.info.unitsPerEm/8

# Add 25 units to all glyphs in the font that have a width.
for gName in font.keys():
    g = font[gName]
    if g.width is not None:
        newWidth = g.width + INCREMENT
        print('Change width of %s from %d to %d' % (gName, g.width, newWidth))
        g.width = newWidth
# Change the family name
font.info.familyName = '%s_%d' %(font.info.familyName, INCREMENT)
print('Changed family name to "%s"' % font.info.familyName)
# Make a new path name in local _export folder, so it won't update on git.
exportPath = '_export/' + font.path.split('/')[-1].replace('.ttf', '_%d.ttf' % INCREMENT)
print('Exporting to %s' % exportPath)
font.save(exportPath)


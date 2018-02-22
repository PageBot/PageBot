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
#     FamilyUsage.py
#
#     This script shows examples how to use the Family implementaton of PageBot.
# 
from pagebot.fonttoolbox.objects.family import guessFamiliesByPatterns

LINE = 60

testFamilyName = 'Verdana'

# Try to construct a Verdana 
families = guessFamiliesByPatterns(testFamilyName)
print '-'*LINE
print 'Dictionary of found families with this name pattern:', families
print '-'*LINE
family = families['Verdana']
print 'Family:', family
print 'Family.name:', family.name
print 'Family size', len(family), 'same as len(family.fonts)', len(family.fonts)

if 1:
    print '-'*LINE
    print 'family.fonts is a dict(fontFilename: Font, ...)'
    print '.'*LINE
    print family.fonts

if 1:
    # In family.fontStyles they Font instances are ordered as list, with our own style names.
    print '-'*LINE
    print 'Fonts ordered by style name (either defined or from font.info.styleName.'
    print '.'*LINE
    print family.fontStyles

if 1:
    # In family.fontStyles they Font instances are ordered as list, with our own style names.
    print '-'*LINE
    print 'Find font that is closes to (weight/width/angle) == (5,400,0),'
    print 'using the font.info.weightClass, font.info.widthClass, font.info.italicAngle'
    print family.getRegularFont()

if 1:
    print '-'*LINE
    print "Initially we don't know if one of the fonts is installed, so there is no DrawBot name for them."
    print '.'*LINE
    print family.installedFonts
    print 'Then install by family.install()'
    family.install()
    print 'Now the fonts are installed and can be used in a formatted string or style. family.installedFonts is a transformer dictionary between DrawBot font name and PageBot fontKey.'
    print family.installedFonts
    print 'Get the Font wrapper by:'
    print "family.installedFonts[%s']:" % testFamilyName, family.installedFonts[testFamilyName] 
    print "family.fonts[family.installedFonts['Georgia']]:", family.fonts[family.installedFonts[testFamilyName]]



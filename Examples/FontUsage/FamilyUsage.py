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
from pagebot.fonttoolbox.objects.family import Family

def run():

    LINE = 50 # Separator line.

    LIB_PATH = '/Library/Fonts/'
    SOME_SYSTEM_FONTS = {
        # Let's try some plain OSX system fonts, while they are still there (not variable yet).
        'Georgia': dict(Regular=LIB_PATH+'Georgia.ttf', Bold=LIB_PATH+'Georgia Bold.ttf', 
                        Italic=LIB_PATH+'Georgia Italic.ttf', BoldItalic=LIB_PATH+'Georgia Bold Italic.ttf'),
        'Verdana': dict(Regular=LIB_PATH+'Verdana.ttf', Bold=LIB_PATH+'Verdana Bold.ttf', 
                        Italic=LIB_PATH+'Verdana Italic.ttf', BoldItalic=LIB_PATH+'Verdana Bold Italic.ttf'),
    }

    familyName = 'Georgia'
    family = Family(familyName, fontStyles=SOME_SYSTEM_FONTS[familyName])
    # Now there is a family container of Font instances (which are wrappers around opened TTFont objects).
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
        print "family.installedFonts['Georgia']:", family.installedFonts['Georgia'] 
        print "family.fonts[family.installedFonts['Georgia']]:", family.fonts[family.installedFonts['Georgia']]


if __name__ == '__main__':
    run()

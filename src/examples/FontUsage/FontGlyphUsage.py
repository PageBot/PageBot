# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     FontUsage.py
#
#     This script shows examples how to use the Font implementaton of PageBot.
#     Font is a wrapper class around the fonttools TTFont, implementing functions
#     more closely to what is expected from RoboFont fonts.
#     The output is showing several parameters of the Variation Font.
# 
from pagebot import getFontPath # Import to know the path of non-Python resources.
from pagebot.fonttoolbox.objects.font import Font

LINE = 50 # Separator line.

#    F O N T  S T U F F 

# Get the variation font.
decovarPath = getFontPath() + '/fontbureau/Decovar-VF_2017-02-06.ttf'
decovar = Font(decovarPath)

if 1: # Font info stuff.
    # Font Info as in RoboFont objects
    print '-'*LINE
    print 'Family name:', decovar.info.familyName
    print 'Style name:', decovar.info.styleName
    print 'Path:', decovar.path
    print 'Units per em:', decovar.info.unitsPerEm
    
if 1: # Variation stuff
    # Show the axes in this font. Key is axis name. Value is (minValue, defaultValue, maxValue)
    print '-'*LINE
    axes = decovar.axes # Get dictionary of axes in the font.
    print 'Axes (%d) in the font {name: (minValue, defaultValue, maxValue), ...}' % len(axes)
    print '.'*LINE
    print axes

if 1: # Kerning stuff
    print '-'*LINE
    print 'Kerning (%d pairs) in %s' % (len(decovar.kerning), decovar.info.familyName)
    print '.'*LINE
    print decovar.kerning
       
if 1:
    # Show the available tables in the TTFont
    print '-'*LINE
    print 'Tables in', decovar.info.familyName
    print '.'*LINE
    print decovar.ttFont.keys()

#   G L Y P H  S T U F F

if 1:
    g = decovar['A'] # Get the Glyph instance.
    print '-'*LINE
    print 'Glyph width of', g.name, g.width # Gets the value of ttFont['htmx']
    print '.'*LINE
    print 'Add 10 to width and print again'
    g.width += 10 # We can change the value in the "live" font. f.save() 
    print 'New width of', g.name, g.width
    print 'This give the interesting opportunity to let the page layout program alter values inside the font.'
    print 'if that is needed for a particular design.'
   
if 1:
    # Info inside the TTGlyph structure.
    print '-'*LINE
    print 'help(g.ttGlyph)'
    print '.'*LINE
    help(g.ttGlyph)
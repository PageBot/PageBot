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
#     This script shows exampels how to use the Font implementaton of PageBot.
#     Font is a wrapper class around the fonttools TTFont, implementing functions
#     more closely to what is expected from RoboFont fonts.
# 
from pagebot import getFontPath # Import to know the path of non-Python resources.
from pagebot.fonttoolbox.objects.font import Font

#    F O N T  S T U F F 

# Get the variation font.
decovarPath = getFontPath() + '/fontbureau/Decovar-VF_2017-02-06.ttf'
f = Font(decovarPath)

if 0: # Font info stuff.
    # Font Info as in RoboFont objects
    print 'Units per em', f.info.unitsPerEm
    
if 1: # Variation stuff
    # Show the axes in this font. Key is axis name. Value is (minValue, defaultValue, maxValue)
    print f.axes

if 1: # Kerning stuff
    print f.kerning
       
# Show the available tables in the TTFont
if 1:
    print f.ttFont.keys()

#   G L Y P H  S T U F F

g = f['A']
if 1:
    print g.width # Gets the value of ttFont['htmx']
    g.width += 10 # We can change the value in the "live" font. f.save() 
    print 'Width of', g.name, g.width
    

if 0:
    # Info inside the TTGlyph structure.
    help(g.ttGlyph)
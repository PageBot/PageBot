# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     ModifyFonts.py
#
import pagebot
from pagebot.contexts.platform import getContext
from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance, getConstrainedLocation

fontPath = pagebot.getFontPath()
f = Font(fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf', install=False)
# Now we have a variable font open.
print f.axes
# Get an instance at a certain location

location = getConstrainedLocation(f, dict(wdth=3944/10, wght=760/10))
instance = getVarFontInstance(f, location, install=False, cached=False)

c.drawPath(instance['H'].path, (100, 100), sx=0.4)
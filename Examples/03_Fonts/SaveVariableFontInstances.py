# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     ModifyFonts.py
#
import pagebot
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance, getConstrainedLocation

c = getContext()

f = findFont('Amstelvar-Roman-VF') # Get PageBot Font instance of Variable font.

# Now we have a variable font open.
print(f.axes)
# Get an instance at a certain location

location = getConstrainedLocation(f, dict(wdth=3944/10, wght=760/10))
instance = getVarFontInstance(f, location, cached=False)

c.drawPath(instance['H'].path, (100, 100), sx=0.4)

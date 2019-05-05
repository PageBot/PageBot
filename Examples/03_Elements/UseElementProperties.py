# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     UseElementProperties.py
#
from pagebot.elements import *

W = H = 500
# Create a new container class (or use other specialized ELements.
e = Element(name='myElement')
# Default Element instance has origin on (0,0) and width/height of (1, 1)
print(e)
print('Position and size:', (e.x, e.y, e.w, e.h))
# Set the position. (Most) elements own their position and size as properties.
e.x = 200
e.y = 100
e.w = 400
e.h = 500
print('New position and size:', (e.x, e.y, e.w, e.h))
print('Unique element Id (eId) for this element:', e.eId)

# Get the element info string, as used in meta info boxes
print('-'*20)
print(e.getMetricsString())
print('-'*20)


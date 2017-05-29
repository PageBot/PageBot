# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     UseElementProperties.py
#
from pagebot.elements import *

def run():
	W = H = 500
	# Create a new container class (or use other specialized ELements.
	e = Element(name='myElement')
	# Default Element instance has origin on (0,0) and width/height of (1, 1)
	print e
	print 'Position and size:', (e.x, e.y, e.w, e.h)
	# Set the position. (Most) elements own their position and size as properties.
	e.x = 200
	e.y = 100
	e.w = 400
	e.h = 500
	print 'New position and size:', (e.x, e.y, e.w, e.h)
	print 'Uniek element Id (eId) for this element:', e.eId
	# Set minimal and maximal boundary values
	e.setMinSize(10) # Set all 3 min values 
	e.setMaxSize(W, W+100, W+200) # Set max values separate
	print 'Minimal size', e.minW, e.minH, e.minD, e.getMinSize()
	print 'Maximal size', e.maxW, e.maxH, e.maxD, e.getMaxSize()

	# Get the element info string, as used in meta info boxes
	print '-'*20
	print e.getElementInfoString()
	print '-'*20

if __name__ == '__main__':
	run()
	
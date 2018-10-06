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
#     ScalingAnImage.py
#
#     How to scale an image (without being an element) in plain DrawBot?
#     Since the core DrawBot does not support w/h attrbiutes for images,
#     it needs to be done by using the scale() function.
#
#     Unfortunately this also changes to x/y position scale, so when
#     drawing an image on the canvas, the position must be scaled the
#     other way around. In this example it doesn't matter, because the
#     scaled image is positioned at (0, 0).
#
import os # Import module that communicates with the file system.
import sys

from pagebot.document import Document
from pagebot import getResourcesPath
from pagebot.toolbox.units import pt
from pagebot import getContext
from pagebot.constants import A4
from pagebot.elements import *
from pagebot.conditions import *

context = getContext()

W, H = A4
M = pt(8) # Margin between the images

EXPORT_PATH = '_export/CacheScaledImage.pdf'

if __name__ == '__main__':

	# Define the path where to find the example image.
	path = getResourcesPath() + "/images/cookbot1.jpg"
	# Use the standard DrawBot function to get the width/height of the image from the file.
	doc = Document(w=W, h=1.35*H, originTop=False, context=context) # New simple document with default padding.

	page = doc[1] # Get first (and only) automatic page.
	factor = 1 # Incremental scale division factor of the image width.

	for n in range(12): # Stop before they become invisible small
		# Create a range of scaled imaged that try to fit by floating conditions.
		newImage(path, w=page.pw/factor, mr=M, mb=M, parent=page, 
			conditions=(Right2Right(), Float2Top(), Float2Left()))
		factor *= 1.6

	doc.solve() # Solve the fitting of the scaled images on the page.

	doc.export(EXPORT_PATH)

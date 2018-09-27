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

from pagebot import getResourcesPath
from pagebot.toolbox.units import pt
from pagebot import getContext
context = getContext()

if __name__ == '__main__':

	# Define the path where to find the example image.
	path = getResourcesPath() + "/images/cookbot1.jpg"
	# Use the standard DrawBot function to get the width/height of the image from the file.
	w, h = context.imageSize(path)

	# Let's say we want to scale it to 50%. The 0.5 is the multiplication factor.
	newScale = 0.5

	# Make a page with the size of the scaled image, rounded to whole pixels.
	context.newPage(pt(int(w*newScale)), pt(int(h*newScale)))

	# Save the “graphics state“, just in case the script is extended later, where other
	# operation need to work in 100%.
	context.save()
	context.scale(newScale) # Make all drawing scale to 50%
	context.image(path, pt(0, 0)) # Draw the scaled image at the bottom-left corner. It fills the whole page.
	# Save the page as png file (and also do conversion from jpg to png this way).
	# Save to _export folder, so the file will not upload into git. Otherwise anyone running this script will update the (same) image.
	if not os.path.exists('_export/'):
	    os.makedirs('_export/')
	# Note that resulting images may look sharper, by has 4.5x the size of the .jpg.
	context.saveImage('_export/cookbot1-%d.png' % (newScale*100)) # 944Kb size
	context.saveImage('_export/cookbot1-%d.jpg' % (newScale*100)) # 168Kb size
	context.saveImage('_export/cookbot1-%d.gif' % (newScale*100)) # 346Kb size
	# Restore the graphics state, so DrawBot scaling is back to 100% after this.
	context.restore()
	print('Done')


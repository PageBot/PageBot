# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     SystemFontSpecimen.py
#
from pagebot.fonttoolbox.objects.family import getSystemFontPaths
from pagebot.publications.typespecimen import TypeSpecimen

DEBUG = False # Make True to see grid and element frames.

if __name__ == '__main__':
	# Create a new specimen publications and add the list of system fonts.
	typeSpecimen = TypeSpecimen(getSystemFontPaths(), showGrid=DEBUG) 
	# Build the pages of the publication, interpreting the font list.
	typeSpecimen.build()
	# Export the document of the publication to PDF.
	typeSpecimen.export('SystemFontSpecimen.pdf')
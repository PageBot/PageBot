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
#     SystemFontSpecimen.py
#
from pagebot.fonttoolbox.objects.family import getSystemFontPaths
from pagebot.publications.typespecimen import TypeSpecimen

DEBUG = False # Make True to see grid and element frames.

if __name__ == '__main__':
	# Create a new specimen publications and add the list of system fonts.
	typeSpecimen = TypeSpecimen(styleNames=getSystemFontPaths(), showGrid=DEBUG) 
	# Build the pages of the publication, interpreting the font list.
	# Create as  many pages as needed for the found families
	typeSpecimen.build()
	# Export the document of the publication to PDF.
	typeSpecimen.export('_export/SystemFontSpecimen.pdf')
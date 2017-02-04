# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     SystemFonts.py
#
import pagebot.publications.typespecimen
reload(pagebot.publications.typespecimen)
from pagebot.publications.typespecimen import TypeSpecimen

# Create a new specimen publications and add the list of system fonts.
typeSpecimen = TypeSpecimen(installedFonts()) 
# Build the pages of the publication, interpreting the font list.
typeSpecimen.build()
# Export the document of the publication to PDF.
typeSpecimen.export('SystemFontSpecimen.pdf')
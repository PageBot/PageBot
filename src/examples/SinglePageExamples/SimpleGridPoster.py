# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     SimpleGridPoster.py
#
import pagebot # Import to know the path of non-Python resources.

from pagebot.publications.poster import Poster

if __name__ == '__main__':
		
	# Get templates for the content and design, as expected by the Poster class.
	myContent = Poster.getContentModel()
	myDesign = Poster.getDesignModel()
	# Create a new Poster instance with the defined content and design paramters.
	poster = Poster(myContent, myDesign) 
	# Build the poster, interpreting the content and the directions for the design.
	poster.build()
	# Export the document of the publication to PDF.
	poster.export('SimpleGridPoster.pdf')
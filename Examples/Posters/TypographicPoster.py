# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Free to use. Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     TypographicPoster.py
#
from pagebot.typesetter import Typesetter
from pagebot.composer import Composer
from pagebot.publications.publication import Publication

# Path to markdown file, including Python code blocks.
MD_PATH = u"TypographicPoster.md"
# Export path to save the poster PDF.
EXPORT_PATH = '_export/TypographicPoster.pdf'

# Create an unbound Typesetter instance (trying to find a Poster
# (inheriting from Document) instance in one of the codeblock results. 
# If no Galley instance is supplied to the Typesetter, it will create one.
t = Typesetter()
# Parse the markdown content and execute the embedded Python code blocks.
# The blocks, global defined variables and text content are in the 
# typesetter t.galley.
t.typesetFile(MD_PATH)
# The typesetter produced a single Galley with content and code blocks.
# Now use a composer (automatic "designer") to fit the pieces together.
# Takes a galley as soruce and a document for target pages. 
Composer().compose(t.galley, t.doc)

if 0: # Print some results of the typesetter
    # Typesetter found document definition inside content.
    print 'Poster title:', t.doc.title, round(t.doc.w), round(t.doc.h)
    # Multiple code blocks found with identical identifier.
    # Added counter 'Views_0' to 'Views' to make it unique. 
    print 'Found code blocks:', t.codeBlocks.keys()
    #print t.galley.elements[0].text
    template = t.doc.pageTemplate
    print template.elements
    page = t.doc[0]
    print page.template.w, page.w, page.h

t.doc.export(EXPORT_PATH)
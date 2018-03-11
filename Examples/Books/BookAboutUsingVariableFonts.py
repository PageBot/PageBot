# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Free to use. Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     BookAboutUsingVariableFonts.py
#
from pagebot.typesetter import Typesetter
from pagebot.composer import Composer
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.conditions import *

# Path to markdown file, including Python code blocks.
MD_PATH = u"UsingVariableFonts.md"
# Export path to save the poster PDF.
EXPORT_PATH = '_export/UsingVariableFonts.pdf'

class BookMaker(object):
    u"""Create a BookMaker class here. Most of the definition of the book will be
    done in the "UsingVariableFonts.md" markdown file. This class only holds the 
    typesetter, composer and template(s) together. And it contains the settings of
    the view for the book (e.g. flags for showing cropmarks and registration marks).
    
    Working this way (combining content with page templates) is a choice.
    Another approach it so keep the markdown file for formatted text only, and 
    defined the templates in a scripts like this.
    """
    
    def build(self):
        # Create an unbound Typesetter instance (trying to find a Book
        # (inheriting from Document) instance in one of the codeblock results. 
        # If no Galley instance is supplied to the Typesetter, it will create one.
        t = Typesetter()
        # Parse the markdown content and execute the embedded Python code blocks.
        # The blocks, global defined variables and text content are in the 
        # typesetter t.galley.
        t.typesetFile(MD_PATH)
        # The markdown document created a t.doc Document instance, 
        
        # The typesetter produced a single Galley with content and code blocks.
        # Now use a composer (automatic "designer") to fit the pieces together.
        # Takes a galley as soruce and a document for target pages. 
        #Composer().compose(t.galley, t.doc)

        # Show a "help-manual" of what the document can do.
        help(t.doc)
        
        # DEBUGGING Stuff
        if 0: # Print some results of the typesetter
            # Typesetter found document definition inside content.
            print 'Book title:', t.doc.title, round(t.doc.w), round(t.doc.h)
            # Multiple code blocks found with identical identifier.
            # Added counter 'Views_0' to 'Views' to make it unique. 
            print 'Found code blocks: %d' % len(t.codeBlocks.keys())
            #print t.galley.elements[0].text
            #page = t.doc[0]
            #print page.padding
            #print page.w, page.h

        if 0: # Debugging, show the pages with their names.
            print t.doc.css('gridL')
            for templateName, template in t.doc.templates.items():
                print templateName, template.name
            for pn, pages in t.doc.getSortedPages():
                for page in pages:
                    print '\t', page, page.w, page.h, page.template.name
                    #page.isLeft(), page.isRight(), page.getGridColumns()

        # Views define the way documents are exported.
        # Add space for cropmarks and registrations marks
        view = t.doc.getView()
        view.padding = 30
        view.showPageNameInfo = True
        view.showPagePadding = False # No need, as we are drawing the grid
        view.showPageCropMarks = True
        view.showPageRegistrationMarks = True
        view.showPageFrame = True 
        view.showGrid = False

        view.style['viewGridStroke'] = (0, 0, 1)
        view.style['viewGridStrokeWidth'] = 0.5

        t.doc.solve()

        t.doc.export(EXPORT_PATH)
        
# Create the maker and builder the book.
BookMaker().build()

# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     poster.py
#
from pagebot import newFS
from pagebot.publications.publication import Publication
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT, NO_COLOR
# Document is the main instance holding all information about the document together 
# (pages, styles, etc.)
from pagebot.document import Document
# Page and Template instances are holding all elements of a page together.
from pagebot.elements.pbpage import Template

 
class Poster(Publication):
        
    def __init__(self, content, design):
        Publication.__init__(self)
        self.content = content # Content dictionary, as derived and altered from Poster.getContentModel()
        self.design = design # Design dictionary, as derived and altered from Poster.getDesignModel()
        
    @classmethod
    def getContentModel(self):
        u"""Answer the model of content data that the Poster instance expect to work with."""
        return dict()
        
    @classmethod
    def getDesignModel(self):
        u"""Answer the model of design data that the Poster instances expect to work with."""
        return dict()
        
    def build(self, title=None):
        rs = getRootStyle()
        rs['language'] = 'en' # Make English hyphenation default. 
        
        # Define the ids of the page boxes
        self.mainContentId = 'mainContentId'
        
        # Template for the main page.
        template = Template(style=rs) # Create template, using the root sttle. This is for the main pages.
        # Add named text box to template for main specimen text.
        template.cTextBox('', 1, 0, 5, 7, eId=self.mainContentId) 
        
        posterTitle = title or 'Simple Poster Example'      
        # Create new document with (w,h) and start with a single page.
        self.documents['Specimen'] = doc = Document(rs, title=posterTitle, pages=1, template=template) 
        # Make number of pages with default document size.
        # When building, make all pages default with template.
        # Call with separate method, so inheriting specimen publications classes can redefine.\   
        self.buildPoster(doc[1])
        
    def buildPoster(self, page):
        u"""Build the poster document, using the self.content and self.design as data."""
        # TODO: Make sample poster drawing here.
        print 'Poster layout under development.'
    

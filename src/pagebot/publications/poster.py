# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     poster.py
#
import pagebot 
reload(pagebot)
from pagebot import getFormattedString

import pagebot.publication
reload(pagebot.publication)
from pagebot.publication import Publication
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT_ALIGN, NO_COLOR
# Document is the main instance holding all information about the document together 
# (pages, styles, etc.)
import pagebot.document
reload(pagebot.document)
from pagebot.document import Document
# Page and Template instances are holding all elements of a page together.
from pagebot.page import Template

 
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
        
    def build(self):
        rs = getRootStyle()
        rs['language'] = 'en' # Make English hyphenation default. 
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        # Show grid columns and margins if rootStyle.showGrid or 
        # rootStyle.showGridColumns are True.
        # The grid is just a regular element, like all others on the page. Same parameters apply.
        template.grid(rs)  
        # Add named text box to template for main specimen text.
        template.cTextBox('', 1, 0, 5, 7, eId=self.specimenBoxId, style=rs)       
        # Create new document with (w,h) and start with a single page.
        self.documents['Specimen'] = doc = Document(rs, title='OS Type Specimen', pages=1, template=template) 
        # Make number of pages with default document size.
        # When building, make all pages default with template.
        # Call with separate method, so inheriting specimen publications classes can redefine.\   
        self.buildPoster(doc)
        
    def buildPoster(self):
        u"""Build the poster document, using the self.content and self.design as data."""
        
        
    

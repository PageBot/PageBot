# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     typespecimen.py
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
from pagebot.page import Page, Template

 
class TypeSpecimen(Publication):
    def __init__(self, fontNames=None):
        Publication.__init__(self)
        self.fontNames = fontNames
        
    def build(self):
        rs = getRootStyle()
        rs['language'] = 'en' # Make English hyphenation default. 
        rs['fill'] = NO_COLOR   
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        # Show grid columns and margins if rootStyle.showGrid or 
        # rootStyle.showGridColumns are True.
        # The grid is just a regular element, like all others on the page. Same parameters apply.
        template.grid(rs)  
        print rs
        template.cTextBox('', 1, 0, 5, 7, eId='specimen', style=rs)       
        # Create new document with (w,h) and start with a single page.
        self.documents['Specimen'] = doc = Document(rs, title='TypeSpeciment', pages=1, template=template) 
        # Make number of pages with default document size.
        # When building, make all pages default with template.
        # Call with separate method, so inheriting specimen publications classes can redefine.\   
        self.buildPages(doc)
        
    def buildPages(self, doc):
        # Find the family relation of all fonts in the list.
        families = {}
        page = doc[1]
        for fontName in self.fontNames:
            if fontName.startswith('.'):
                continue
            familyName = fontName.replace(' ', '-').split('-')[0]
            if not familyName in families:
                families[familyName] = []
            families[familyName].append(fontName)
        for familyName, fonts in families.items():
            column = page.getElement('specimen')
            fs = getFormattedString(familyName+'\n\n', dict(fontSize=16, font=fonts[0]))
            for fontName in fonts:
                fs += getFormattedString(fontName+'\n', style=dict(fontSize=32, font=fontName))
            column.append(fs)	
            page = doc.newPage()    
       
        
    

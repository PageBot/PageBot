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
    
    MIN_STYLES = 4 # Don't show, if families have fewer amount of style.
    
    def __init__(self, styleNames=None):
        Publication.__init__(self)
        self.styleNames = styleNames
        self.specimenBoxId = 'specimenBox'
        
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
        self.buildPages(doc)
        
    def buildPages(self, doc):
        # Find the family relation of all fonts in the list.
        families = {}
        # Get the current page of the document, created automatic with template.
        # Using the first page as cover (to be filled...)
        coverPage = doc[1]
        # Fill cover here.
        for styleName in self.styleNames:
            if styleName.startswith('.'): # Filter the system fonts that has a name with initial "."
                continue
            familyName = styleName.replace(' ', '-').split('-')[0] # Split family name part by space or hyphen.
            if not familyName in families: # Make a family collection of style names, if not already there.
                families[familyName] = []
            families[familyName].append(styleName) # Store the style name in the family collection.
        # Now we collected a families and styles in the OS, create one page per family.
        for familyName, styleNames in sorted(families.items()): # For all the sorted family collections...
            # Only show the "serious" families, that have at least MIN_STYLES amout of styles.
            if len(styleNames) < self.MIN_STYLES:
                continue
            # Create a new page for the this family, using the default template.
            page = doc.newPage()    
            column = page.getElement(self.specimenBoxId) # Find the column element on the current page.
            # Create the formatted string with the style names shown in their own style.
            # The first one in the list is also used to show the family Name.
            fs = getFormattedString(familyName+'\n\n', dict(fontSize=32, font=styleNames[0]))
            for styleName in sorted(styleNames):
                fs += getFormattedString(styleName+'\n', style=dict(fontSize=16, font=styleName, rLeading=1.4))
            column.append(fs)	
       
        
    

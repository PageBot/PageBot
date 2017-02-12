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

from pagebot.fonttoolbox.family import Family
from pagebot.fonttoolbox.font import Font, getFontPathOfFont

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
    
    def __init__(self, styleNames=None, showGrid=False, showGridColumns=False):
        Publication.__init__(self)
        self.styleNames = styleNames
        # Identifiers of template text box elements.
        self.titleBoxId = 'titleBoxId'
        self.specimenBoxId = 'specimenBoxId'
        self.infoBoxId = 'infoBoxId'
        # Display flags
        self.showGrid = showGrid
        self.showGridColumns = showGridColumns
        
    def makeTemplate(self, rs):
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        # Show grid columns and margins if rootStyle.showGrid or 
        # rootStyle.showGridColumns are True.
        # The grid is just a regular element, like all others on the page. Same parameters apply.
        template.grid(rs)  
        # Add named text box to template for main specimen text.
        template.cTextBox('', 0, 0, 6, 1, eId=self.titleBoxId, style=rs)       
        template.cTextBox('', 2, 1, 4, 6, eId=self.specimenBoxId, style=rs)       
        template.cTextBox('', 0, 1, 2, 6, eId=self.infoBoxId, style=rs)
        # Some lines, positioned by vertical and horizontal column index.
        template.cLine(0, 0, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 1, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 7, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        return template
        
    def build(self):
        rs = getRootStyle(showGrid=self.showGrid, showGridColumns=self.showGridColumns)
        rs['language'] = 'en' # Make English hyphenation default. 
        template = self.makeTemplate(rs)
        # Create new document with (w,h) and start with a single page.
        self.documents['Specimen'] = doc = Document(rs, title='OS Type Specimen', pages=1, template=template) 
        # Make number of pages with default document size.
        # When building, make all pages default with template.
        # Call with separate method, so inheriting specimen publications classes can redefine.\   
        self.buildPages(doc)
        
    def buildPages(self, doc):
        # Build the pages, one page per family. Compsition 
        # Get the current page of the document, created automatic with template.
        # Using the first page as cover (to be filled...)
        coverPage = doc[1]
        # Fill cover here.
        
        # Collect the families, style names and their font paths.
        families = self.getFamilies()
        
        # Now we collected a families and styles in the OS, create one page per family.
        for familyName, family in sorted(families.items()): # For all the sorted family collections...
            # Only show the "serious" families, that have at least MIN_STYLES amout of styles.
            if len(family) < self.MIN_STYLES:
                continue
            # Create a new page for the this family, using the default template.
            page = doc.newPage()    
            self.buildFamilyPage(page, family)
    
    def buildFamilyPage(self, page, family):
        u"""Build the family page. Layout depends on the content of the family and the type of font."""
        
        # Get the "most regular style" in the family.
        style = family.getRegularStyle()

        # Get the title box and try to fit the add family name.
        title = page.getElement(self.titleBoxId) 
        fs = getFormattedString(family.name, dict(fontSize=48, font=style.name))
        title.append(fs)
        
        if style.info.description:
            info = page.getElement(self.infoBoxId)
            fs = getFormattedString(style.info.description, dict(fontSize=9, leading=15, font=style.name))
            info.append(fs)
        
        column = page.getElement(self.specimenBoxId) # Find the specimen column element on the current page.
        # Create the formatted string with the style names shown in their own style.
        # The first one in the list is also used to show the family Name.
        fs = getFormattedString('')
        for index, (name, style) in enumerate(sorted(family.styles.items())):
            # We can assume these are defined, otherwise the style is skipped.
            styleName = style.info.styleName
            fs += getFormattedString('%s %s %d %d %0.2f\n' % (family.name, styleName, 
                style.info.weightClass, style.info.widthClass, style.info.italicAngle), 
                style=dict(fontSize=16, font=style.name, rLeading=1.4))
            
        column.append(fs)	
               
    def getFamilies(self):
        # Find the family relation of all fonts in the list.
        families = {} # Keys is guessed family name.

        for styleName in self.styleNames:
            if styleName.startswith('.'): # Filter the system fonts that has a name with initial "."
                continue
            path = getFontPathOfFont(styleName)
            if not path.lower().endswith('.ttf') and not path.lower().endswith('.otf'):
                continue
            # Try to open the font in font tools, so we have access to a lot of information for our proof.
            # Create Style instance, as storage within our page composition passes.
            style = Style(path, styleName)
            if style.info is None:
                continue # Could not open the font file.            
            # Skip if there is not a clear family name and style name derived from FontInfo    
            if  style.info.familyName and style.info.styleName:
                # Make a family collection of style names, if not already there.
                if not style.info.familyName in families: 
                    families[style.info.familyName] = Family(style.info.familyName)
                # Store the style name and path in the family collection.
                families[style.info.familyName].addStyle(style) 

        return families 

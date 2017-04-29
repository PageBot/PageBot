# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     randompage.py
#

import pagebot 
import pagebot.publication

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT, NO_COLOR
        
class RandomPage(Publication):
    
    def __init__(self, title=None, showGrid=False, showGridColumns=False):
        Publication.__init__(self)
        self.title = title or 'One Page'
        # Identifiers of template text box elements.
        self.titleBoxId = 'titleBoxId'
        self.specimenBoxId = 'specimenBoxId'
        self.infoBoxId = 'infoBoxId'
        # Display flags
        self.showGrid = showGrid
        self.showGridColumns = showGridColumns
        
    def build(self):
        # Get the PageBot root style, including all default parameters.
        # Then onlt change the values that are not default.
        rs = getRootStyle(showGrid=self.showGrid, showGridColumns=self.showGridColumns)
        rs['language'] = 'en' # Make English hyphenation default. 
        # Create a template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True.
        # The grid is just a regular element, like all others on the page. Same parameters apply.
        template.grid(rs)  
        # Add named text box to template for main specimen text.
        template.cTextBox('', 0, 0, 6, 1, eId=self.titleBoxId, style=rs)       
        template.cTextBox('', 2, 1, 4, 6, eId=self.specimenBoxId, style=rs)       
        template.cTextBox('', 0, 1, 2, 6, eId=self.infoBoxId, style=rs)
        # Some lines
        template.cLine(0, 1, 6, 1, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 7, 6, 7, style=rs, stroke=0, strokeWidth=0.25)       
        # Create new document with (w,h) and start with a single page.
        self.documents['OnePage'] = doc = Document(rs, title=self.title, pages=1, template=template) 
        # Make number of pages with default document size.
        # When building, make all pages default with template.
        # Call with separate method, so inheriting specimen publications classes can redefine.\   
        self.buildPage(doc)
        
    def buildPage(self, doc):
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
    

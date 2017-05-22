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
#     Generic Type Specimen Publiction. Use straight, if the default behavior
#     and templates are hood enough. Inherit the redefine functions otherwise.
#     Example of an inherited publications is FBFamilySpecimen.py
#
from pagebot import newFS

from pagebot.fonttoolbox.objects.family import Family, guessFamilies
from pagebot.fonttoolbox.objects.font import Font, getFontPathOfFont

from pagebot.publications.publication import Publication
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT, NO_COLOR, A4
# Document is the main instance holding all information about the document together 
# (pages, styles, etc.)
from pagebot.document import Document
# Page and Template instances are holding all elements of a page together.
from pagebot.elements.pbpage import Page, Template
 
W, H = A4

class TypeSpecimen(Publication):
    
    MIN_STYLES = 4 # Don't show, if families have fewer amount of style.
    
    FONT_CLASS = Font
    FAMILY_CLASS = Family
    
    def __init__(self, styleNames=None, pageTitle=None, showGrid=False, showGridColumns=False):
        Publication.__init__(self)
        self.styleNames = styleNames
        self.pageTitle = pageTitle
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
        # Add named text box to template for main specimen text.
        template.cTextBox('', 0, 0, 6, 1, eId=self.titleBoxId, style=rs)       
        template.cTextBox('', 2, 1, 4, 6, eId=self.specimenBoxId, style=rs)       
        template.cTextBox('', 0, 1, 2, 6, eId=self.infoBoxId, style=rs)
        # Some lines, positioned by vertical and horizontal column index.
        template.cLine(0, 0, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 1, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 7, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        return template
        
    def build(self, font):
        rs = getRootStyle(showGrid=self.showGrid, showGridColumns=self.showGridColumns)
        rs['language'] = 'en' # Make English hyphenation default. 
        template = self.makeTemplate(rs)
        pageTitle = self.pageTitle or 'Unnamed Type Specimen'
        # Create new document with (w,h) and start with a single page.
        self.documents['Specimen'] = doc = Document(rs, w=W, h=H, title=pageTitle, pages=1, template=template) 
        # Make number of pages with default document size.
        # When building, make all pages default with template.
        # Call with separate method, so inheriting specimen publications classes can redefine.\   
        self.buildPages(doc, font)
        
    def buildPages(self, doc):
        # Build the pages, one page per family. Compsition 
        # Get the current page of the document, created automatic with template.
        # Using the first page as cover (to be filled...)
        coverPage = doc[0]
        # Fill cover here.
        
        # Collect the system families, style names and their font paths. Guess their family relation.
        families = guessFamilies(self.styleNames)
        
        # Now we collected a families and styles in the OS, create one page per family.
        for familyName, family in sorted(families.items()): # For all the sorted family collections...
            # Only show the "serious" families, that have at least MIN_STYLES amount of styles.
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
        fs = newFS(family.name, dict(fontSize=48, font=style.name))
        title.append(fs)
        
        if style.info.description:
            info = page.getElement(self.infoBoxId)
            fs = newFS(style.info.description, dict(fontSize=9, leading=15, font=style.name))
            info.append(fs)
        
        column = page.getElement(self.specimenBoxId) # Find the specimen column element on the current page.
        # Create the formatted string with the style names shown in their own style.
        # The first one in the list is also used to show the family Name.
        fs = newFS('')
        for index, (name, style) in enumerate(sorted(family.styles.items())):
            # We can assume these are defined, otherwise the style is skipped.
            styleName = style.info.styleName
            fs += newFS('%s %s %d %d %0.2f\n' % (family.name, styleName, 
                style.info.weightClass, style.info.widthClass, style.info.italicAngle), 
                style=dict(fontSize=16, font=style.name, rLeading=1.4))
            
        column.append(fs)	

          

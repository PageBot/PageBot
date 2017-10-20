# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     typespecimen.py
#
#     Generic Type Specimen Publiction. Use straight, if the default behavior
#     and templates are hood enough. Inherit the redefine functions otherwise.
#     Example of an inherited publications is FBFamilySpecimen.py
#

from pagebot.fonttoolbox.objects.family import Family, guessFamilies
from pagebot.fonttoolbox.objects.font import Font, getFontPathOfFont

from pagebot.publications.publication import Publication
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT, NO_COLOR, A4
# Document is the main instance holding all information about the document together 
# (pages, styles, etc.)
from pagebot.document import Document
# Page and Template instances are holding all elements of a page together.
# And import all other element constructors.
from pagebot.elements import *
# Import conditions for layout placements and other element status.
from pagebot.conditions import *
 
W, H = A4

class TypeSpecimen(Publication):
    
    MIN_STYLES = 4 # Don't show, if families have fewer amount of style.
    
    FONT_CLASS = Font
    FAMILY_CLASS = Family
    
    def __init__(self, styleNamePattern=None, styleNames=None, pageTitle=None, showGrid=False, showGridColumns=False):
        Publication.__init__(self)
        # Name pattern to match available installed fonts.
        self.styleNamePattern = styleNamePattern 
        self.styleNames = []
        for styleName in self.view.installedFonts():
            if styleNamePattern is None or styleNamePattern in styleName:
                self.styleNames.append(styleName)
        
        self.pageTitle = pageTitle
        # Identifiers of template text box elements.
        self.titleBoxId = 'titleBoxId'
        self.specimenBoxId = 'specimenBoxId'
        self.infoBoxId = 'infoBoxId'
        # Display flags
        self.showGrid = showGrid
        self.showGridColumns = showGridColumns
        
    def XXXmakeTemplate(self):
        # Generic conditions to build stacked elements page with full width.
        lw = 0.25
        lineColor = 0
        conditions = (Float2Top(), Left2Left(), Fit2Width())
        # Template for the main page.
        template = Template() # Create second template. This is for the main pages.
        # Add named text box to template for main specimen text.
        newTextBox('', eId=self.titleBoxId, parent=template, conditions=conditions)       
        # Some lines, positioned by vertical and horizontal column index.
        newLine(stroke=lineColor, strokeWidth=lw, parent=template, 
            conditions=conditions)       
        newTextBox('', eId=self.specimenBoxId, parent=template)       
        newLine(stroke=lineColor, strokeWidth=lw, parent=template, 
            conditions=conditions)       
        newTextBox('', eId=self.infoBoxId, parent=template)
        newLine(stroke=lineColor, strokeWidth=lw, parent=template, 
            conditions=conditions)       
        return template
        
    def XXXbuild(self):
        template = self.makeTemplate()
        pageTitle = self.pageTitle or 'Unnamed Type Specimen'
        # Create new document with (w,h) and start with a single page.
        # Make number of pages with default document size.
        # When building, make all pages default with template.
        # Call with separate method, so inheriting specimen publications classes can redefine.\   
        doc = Document(w=W, h=H, title=pageTitle, originTop=False, 
            autoPages=1, template=template) 
        
    def XXXbuildPages(self, doc):
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
    
    def XXXbuildFamilyPage(self, page, family):
        u"""Build the family page. Layout depends on the content of the family and the type of font."""
        
        # Get the "most regular style" in the family.
        style = family.getRegularStyle()

        # Get the title box and try to fit the add family name.
        title = page.getElement(self.titleBoxId) 
        fs = self.context.newString(family.name, dict(fontSize=48, font=style.name))
        title.append(fs)
        
        if style.info.description:
            info = page.getElement(self.infoBoxId)
            fs = self.context.newString(style.info.description, dict(fontSize=9, leading=15, font=style.name))
            info.append(fs)
        
        column = page.getElement(self.specimenBoxId) # Find the specimen column element on the current page.
        # Create the formatted string with the style names shown in their own style.
        # The first one in the list is also used to show the family Name.
        fs = self.context.newString('')
        for index, (name, style) in enumerate(sorted(family.styles.items())):
            # We can assume these are defined, otherwise the style is skipped.
            styleName = style.info.styleName
            fs += self.context.newString('%s %s %d %d %0.2f\n' % (family.name,
                                                                  styleName,
                                                                  style.info.weightClass,
                                                                  style.info.widthClass,
                                                                  style.info.italicAngle),
                                         style=dict(fontSize=16,
                                                    font=style.name,
                                                    rLeading=1.4))
            
        column.append(fs)	

          

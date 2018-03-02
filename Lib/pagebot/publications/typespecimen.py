#!/usr/bin/env python
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
#     and templates are good enough. Inherit the redefine functions and templates
#     otherwise. Example of an inherited publications is FBFamilySpecimen.py
#
# Publication (inheriting from Document) is the main instance holding all information 
# about the document together (pages, styles, etc.)
from pagebot.publications.publication import Publication 

# Page and Template instances are holding all elements of a page together.
# And import all other element constructors.
#from pagebot.elements import *

# Import conditions for layout placements and other element status.
#from pagebot.conditions import *
 
class TypeSpecimen(Publication):
    
    '''
    To deleted soon.
    There should be only templates here to choose from
    def __init__(self, styleNamePattern=None, styleNames=None, pageTitle=None, showGrid=False, showGridColumns=False, **kwargs):
        u"""Generic base class document for type specimes.

        >>> specimen = TypeSpecimen(title='MySpecimen', w=400, h=600)
        >>> specimen.title
        'MySpecimen'
        >>> specimen.w, specimen.h
        (400, 600)
        """
        Publication.__init__(self, **kwargs)
        # Name pattern to match available installed fonts.
        self.styleNamePattern = styleNamePattern 
        self.styleNames = []
        for styleName in self.context.installedFonts():
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

    '''

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

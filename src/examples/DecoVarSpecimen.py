# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     SystemFontSpecimen.py
#
import pagebot
from pagebot import getFormattedString
from pagebot.page import Template
from pagebot.fonttoolbox.style import Style

from pagebot.publications.typespecimen import TypeSpecimen
from pagebot.fonttoolbox.elements.variationcube import VariationCube

DEBUG = False # Make True to see grid and element frames.

FONT_PATH = pagebot.getFontPath()
DecovarPath = FONT_PATH + 'fontbureau/Decovar-VF_2017-02-06.ttf'

decovarName = installFont(DecovarPath)
s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789'

class VariationTypeSpecimen(TypeSpecimen):

    def makeTemplate(self, rs):
        hyphenation(False)
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        # Show grid columns and margins if rootStyle.showGrid or 
        # rootStyle.showGridColumns are True.
        # The grid is just a regular element, like all others on the page. Same parameters apply.
        template.grid(rs)  
        # Add named text box to template for main specimen text.
        template.cTextBox('', 0, 0, 6, 1, eId=self.titleBoxId, style=rs)       
        template.cTextBox('', 1, 1, 5, 6, eId=self.specimenBoxId, style=rs)       
        #template.cTextBox('', 0, 1, 2, 6, eId=self.infoBoxId, style=rs)
        # Some lines, positioned by vertical and horizontal column index.
        template.cLine(0, 0, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 1, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 7, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        return template
 
    def buildVariationPage(self, page):
        style = Style(DecovarPath)
        
        title = page.getElement(self.titleBoxId) 
        fs = getFormattedString(style.info.fullName, dict(fontSize=48, font=style.path))
        title.append(fs)
 
        column = page.getElement(self.specimenBoxId) # Find the specimen column element on the current page.
        # Create the formatted string with the style names shown in their own style.
        # The first one in the list is also used to show the family Name.
        for fontSize in (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24):
            fs = getFormattedString('%dpt %s' % (fontSize, s), 
                style=dict(font=decovarName, fontSize=fontSize, hyphenation=False))
            column.append(fs)
        
    def buildPages(self, doc):
        # Build the pages, showing axes, samples, etc.
        # Using the first page as cover (to be filled...)
        coverPage = doc[1]
        # Fill cover here.
        
        page = doc.newPage()    
        self.buildVariationPage(page)
        page = doc.newPage()
        vCube = VariationCube(path=DecovarPath, w=500, h=500, s='a', 
            fontSize=86, dimensions=dict(wght=5, wdth=5))
        page.place(vCube, 50, 160)

    
# Create a new specimen publications and add the list of system fonts.
typeSpecimen = VariationTypeSpecimen([decovarName], showGrid=DEBUG) 
# Build the pages of the publication, interpreting the font list.
typeSpecimen.build()
# Export the document of the publication to PDF.
typeSpecimen.export('DecovarSpecimen.pdf')
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     AmstelVarSpecimen.py
#
from __future__ import division

import pagebot
from pagebot import getFormattedString
from pagebot.page import Template
from pagebot.fonttoolbox.font import Font

from pagebot.publications.typespecimen import TypeSpecimen
from pagebot.fonttoolbox.elements.variationcube import VariationCube
from pagebot.fonttoolbox.elements.variationscatter import VariationScatter

DEBUG = False # Make True to see grid and element frames.

SCATTER_SPECIMENS = True
MATRIX_SPECIMENS = False

if SCATTER_SPECIMENS:
    OUTPUT_FILE = 'AmstelvarRandomSpecimen.pdf'
else:
    OUTPUT_FILE = 'AmstelvarMatrixSpecimen.pdf'

FONT_PATH = pagebot.getFontPath()
DecovarPath = FONT_PATH + 'fontbureau/AmstelvarAlpha-Variations.ttf'
#DecovarPath = u"/Users/petr/git/PageBotTYPETR/src/fonts/BitcountVar/BitcountGrid-GX.ttf"

decovarName = installFont(DecovarPath)

s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'

class VariationTypeSpecimen(TypeSpecimen):

    def getAxisCombinations(self):
        # Answer specific interesting combinations for axes in Decovar.
        combinations = []
        for skl in SKL:
            for bld in BLD:
                combinations.append((skl, bld))
            for terminal in TERMINALS:
                combinations.append((skl, terminal))
        return combinations
    
    STEP = 8
    def normalizedRange(self,  minV, maxV):
        maxV = 1000
        minV = int(round(minV/maxV*1000))
        return range(minV, maxV+1, int(round((maxV-minV)/self.STEP)))
        
    def getLocations(self, font):
        u"""Answer all possible locations."""
        locations = []
        axes = font.axes
        axisNames = sorted(axes.keys())
        for srfr in self.normalizedRange(0, 96):
            for xhgt in self.normalizedRange(890, 1200): 
                for wdth in self.normalizedRange(120, 804):
                    for prwg in self.normalizedRange(10, 1000):
                        for opsz in self.normalizedRange(10, 72):
                            for cntr in self.normalizedRange(8, 170):
                                for wght in self.normalizedRange(75, 500):
                                    for grad in self.normalizedRange(50, 500):
                                        locations.append(dict(srfr=srfr, xhgt=xhgt, wdth=wdth, prwg=prwg, opsz=opsz, cntr=cntr, wght=wght, grad=grad)) 
        return locations

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
 
    def buildVariationPage(self, varFont, page):
        title = page.getElement(self.titleBoxId) 
        fs = getFormattedString(varFont.info.fullName.upper(), dict(fontSize=32, font=decovarName))
        title.append(fs)
 
        column = page.getElement(self.specimenBoxId) # Find the specimen column element on the current page.
        # Create the formatted string with the style names shown in their own style.
        # The first one in the list is also used to show the family Name.
        for fontSize in (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24):
            fs = getFormattedString('%dPT %s\n' % (fontSize, s), 
                style=dict(font=decovarName, fontSize=fontSize, hyphenation=False))
            column.append(fs)
        
    def buildPages(self, doc):
        # Build the pages, showing axes, samples, etc.
        # Using the first page as cover (to be filled...)
        coverPage = doc[1]
        # Fill cover here.

        varFont = Font(DecovarPath)
        print varFont.axes
        
        page = doc.newPage()    
        self.buildVariationPage(varFont, page)
        
        if SCATTER_SPECIMENS:
            locations = self.getLocations(varFont)
            print 'Total amount of locations', len(locations)
            for n in range(30):
                page = doc.newPage()
                glyphName = choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                scatter = VariationScatter(varFont, w=500, h=500, s=glyphName, showRecipe=False,
                    sizeX=5, sizeY=5, fontSize=72, locations=locations)
                page.place(scatter, 50, 100)
                
        elif MATRIX_SPECIMENS:
            # Build axis combinations on pages
            for axis1, axis2 in self.getAxisCombinations():
                page = doc.newPage()
                vCube = VariationCube(varFont, w=500, h=500, s='A', 
                    fontSize=72, dimensions={axis1:5, axis2:5})
                page.place(vCube, 50, 100)

    
# Create a new specimen publications and add the list of system fonts.
typeSpecimen = VariationTypeSpecimen([decovarName], showGrid=DEBUG) 
# Build the pages of the publication, interpreting the font list.
typeSpecimen.build()
# Export the document of the publication to PDF.
typeSpecimen.export(OUTPUT_FILE)


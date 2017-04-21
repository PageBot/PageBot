# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     DecovarSpecimen.py
#
from __future__ import division

import pagebot
from pagebot import getFormattedString
from pagebot.elements.page import Template
from pagebot.fonttoolbox.objects.font import Font

from pagebot.publications.typespecimen import TypeSpecimen
from pagebot.elements.variablefonts.variablecube import VariableCube
from pagebot.elements.variablefonts.variablescatter import VariableScatter

DEBUG = False # Make True to see grid and element frames.

SCATTER_SPECIMENS = True
MATRIX_SPECIMENS = False

if SCATTER_SPECIMENS:
    OUTPUT_FILE = 'DecovarRandomSpecimen.pdf'
else:
    OUTPUT_FILE = 'DecovarMatrixSpecimen.pdf'

FONT_PATH = pagebot.getFontPath()
DecovarPath = FONT_PATH + 'fontbureau/Decovar-VF_2017-02-06.ttf'
#DecovarPath = u"/Users/petr/git/PageBotTYPETR/src/fonts/BitcountVar/BitcountGrid-GX.ttf"

decovarName = installFont(DecovarPath)

s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'

TERMINALS = ('trmA', 'trmB', 'trmC', 'trmD', 'trmE', 'trmF', 'trmG', 'trmH', 'trmF', 'trmG', 'trmK', 'trmL',)
SKL = ('sklA', 'sklB', 'sklD')
BLD = ('bldA', 'bldB')
WMX = ('wmx2',)

class VariableTypeSpecimen(TypeSpecimen):

    def getAxisCombinations(self):
        # Answer specific interesting combinations for axes in Decovar.
        combinations = []
        for skl in SKL:
            for bld in BLD:
                combinations.append((skl, bld))
            for terminal in TERMINALS:
                combinations.append((skl, terminal))
        return combinations
    
    def getLocations(self, font):
        u"""Answer all possible locations."""
        print font.axes
        locations = []
        # A+B
        for terminal in TERMINALS:
            for t in (500, 1000):
                for skeleton in SKL:
                    for s in (250, 500, 750, 1000):
                        locations.append({terminal:t, skeleton:s})
        # A+C
        for terminal in TERMINALS:
            for t in (500, 1000):
                for parametric in WMX:
                    for p in range(125, 1001, int((1000-125)/8)):
                        locations.append({terminal:t, parametric:p})
        # B+C
        for skeleton in SKL:
            for s in (250, 500, 750, 1000):
                for parametric in WMX:
                    for p in range(125, 1001, int((1000-125)/8)):
                        locations.append({skeleton:s, parametric:p})
        # A+B+C
        for terminal in TERMINALS:
            for t in (500, 1000):
                for skeleton in SKL:
                    for s in (250, 500, 750, 1000):
                        for parametric in WMX:
                            for p in range(125, 1001, int((1000-125)/8)):
                                locations.append({skeleton:s, parametric:p, terminal:t})
        # C+D
        for blending in BLD:
            for b in range(125, 1001, int((1000-125)/8)):
                for parametric in WMX:
                    for p in range(125, 1001, int((1000-125)/8)):
                        locations.append({blending:b, parametric:p})
        
        return locations

    def makeTemplate(self, rs):
        hyphenation(False)
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        # Show grid columns and padding if rootStyle.showGrid or 
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
 
    def buildVariablePage(self, varFont, page):
        title = page.getElement(self.titleBoxId) 
        fs = getFormattedString(varFont.info.fullName.upper(), self, dict(fontSize=32, font=decovarName))
        title.append(fs)
 
        column = page.getElement(self.specimenBoxId) # Find the specimen column element on the current page.
        # Create the formatted string with the style names shown in their own style.
        # The first one in the list is also used to show the family Name.
        for fontSize in (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24):
            fs = getFormattedString('%dPT %s\n' % (fontSize, s), self, 
                style=dict(font=decovarName, fontSize=fontSize, hyphenation=False))
            column.append(fs)
        
    def buildPages(self, doc):
        # Build the pages, showing axes, samples, etc.
        # Using the first page as cover (to be filled...)
        coverPage = doc[1]
        # Fill cover here.

        varFont = Font(DecovarPath)
        
        page = doc.newPage()    
        self.buildVariablePage(varFont, page)
        
        if SCATTER_SPECIMENS:
            locations = self.getLocations(varFont)
            print 'Total amount of locations', len(locations)
            for n in range(20):
                page = doc.newPage()
                glyphName = choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                scatter = VariableScatter(varFont, w=500, h=500, s=glyphName, showRecipe=True,
                    sizeX=5, sizeY=5, fontSize=72, locations=locations)
                page.place(scatter, 50, 100)
                
        elif MATRIX_SPECIMENS:
            # Build axis combinations on pages
            for axis1, axis2 in self.getAxisCombinations():
                page = doc.newPage()
                vCube = VariableCube(varFont, w=500, h=500, s='A', 
                    fontSize=72, dimensions={axis1:5, axis2:5})
                page.place(vCube, 50, 100)

    
# Create a new specimen publications and add the list of system fonts.
typeSpecimen = VariableTypeSpecimen([decovarName], showGrid=DEBUG) 
# Build the pages of the publication, interpreting the font list.
typeSpecimen.build()
# Export the document of the publication to PDF.
typeSpecimen.export(OUTPUT_FILE)


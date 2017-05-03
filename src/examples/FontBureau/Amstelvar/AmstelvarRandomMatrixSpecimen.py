# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     AmstelvarSpecimen.py
#
#     Make pages with 6x6 random variable instances of random selected Amstelvar glyphs.
#     Show the axis values of the location as legenda with each glyph.
#
from __future__ import division

import pagebot
from pagebot import getFormattedString
from pagebot.page import Template
from pagebot.style import A4,MM
from pagebot.fonttoolbox.objects.font import Font

from pagebot.publications.typespecimen import TypeSpecimen
from pagebot.fonttoolbox.elements.variablecube import VariableCube
from pagebot.fonttoolbox.elements.variablescatter import VariableScatter

DEBUG = False # Make True to see grid and element frames.

W, H = A4
PADDING = 20*MM

NUM_PAGES = 5 # Number of pages to generate

OUTPUT_FILE = 'AmstelvarRandomSpecimen.pdf'

FONT_PATH = pagebot.getFontPath() # Location of PageBot fonts.
AmstelVarPath = FONT_PATH + 'fontbureau/AmstelvarAlpha-Variables.ttf'
print 'Using font', AmstelVarPath

# Installing the font in DrawBot
amstelVarName = installFont(AmstelVarPath)

s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'

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

    STEP = 10

    def normalizedRange(self,  minV, maxV):
        r = []
        n = minV
        step = (maxV - minV)/self.STEP
        while n <= maxV:
            r.append(n)
            n += step
        return r

    def getLocations(self, font):
        u"""Answer all possible locations."""
        locations = []
        axes = font.axes

        #for axisName, a in axes.items():
        #    print axisName, a, self.normalizedRange(a[0], a[2])

        minV, dV, maxV = axes['srfr']
        for srfr in self.normalizedRange(minV, maxV):
            minV, dV, maxV = axes['wdth']
            for wdth in self.normalizedRange(minV, maxV):
                minV, dV, maxV = axes['wght']
                for wght in self.normalizedRange(minV, maxV):
                    minV, dV, maxV = axes['prwg']
                    for prwg in [dV]: #self.normalizedRange(minV, maxV):
                        minV, dV, maxV = axes['prwd']
                        for prwd in [dV]: #self.normalizedRange(minV, maxV):
                            minV, dV, maxV = axes['cntr']
                            for cntr in [dV]:#self.normalizedRange(minV, maxV):
                                minV, dV, maxV = axes['opsz']
                                for opsz in [dV]:#self.normalizedRange(minV, maxV):
                                    minV, dV, maxV = axes['grad']
                                    for grad in [dV]:#self.normalizedRange(minV, maxV):
                                        locations.append(dict(
                                            srfr=srfr,
                                            xhgt=axes['xhgt'][1],
                                            wdth=wdth,
                                            prwg=prwg,
                                            prwd=prwd,
                                            opsz=opsz,
                                            cntr=cntr,
                                            wght=wght,
                                            grad=grad
                                        ))
        return locations

    def makeTemplate(self, rs):
        hyphenation(False)
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        # Show grid columns and paddings if rootStyle.showGrid or
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
        fs = getFormattedString(varFont.info.fullName.upper(), self, dict(fontSize=32, font=amstelVarName))
        title.append(fs)

        column = page.getElement(self.specimenBoxId) # Find the specimen column element on the current page.
        # Create the formatted string with the style names shown in their own style.
        # The first one in the list is also used to show the family Name.
        for fontSize in (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24):
            fs = getFormattedString('%dPT %s\n' % (fontSize, s), self,
                style=dict(font=amstelVarName, fontSize=fontSize, hyphenation=False))
            column.append(fs)

    def buildVariableMatrixPage(self, varFont, page, locations, textFill=0):
        glyphName = choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        # Make a random selection of locations. Note that this shows the full range of all axes,
        # not necessarily representing the design space limitation or design preferences.
        wh = W-2*PADDING
        scatter = VariableScatter(varFont, w=wh, h=wh, s=glyphName, showRecipe=False,
            recipeAxes=['srfr', 'wdth', 'wght', 'opsz', 'cntr', 'grad'], sizeX=5, sizeY=5, fontSize=64, locations=locations,
            textFill=textFill)
        page.place(scatter, 50, 100)

    def buildPages(self, doc):

        # Get the font
        varFont = Font(AmstelVarPath)

        # Build the pages, showing axes, samples, etc.

        print 'Variable A X E S'
        for axisName, (minValue, defaultValue, maxValue) in varFont.axes.items():
            print axisName, 'minValue', minValue, 'defaultValue', defaultValue, 'maxValue', maxValue


        locations = self.getLocations(varFont)

        # Using the first page as cover (to be filled...)
        coverPage = doc[1]
        # Fill cover here.
        coverPage.rect(0, 0, W, H, fill=(1, 0, 0)) 
        #coverPage.text(amstelVarName, x=PADDING, y=H-3*PADDING, style=dict(font=amstelVarName, fontSize=50, textColor=1) )
        self.buildVariableMatrixPage(varFont, coverPage, locations, textFill=1)

        print 'Total amount of locations', len(locations)
        for n in range(NUM_PAGES):
            page = doc.newPage()
            self.buildVariableMatrixPage(varFont, page, locations)


# Create a new specimen publications and add the list of system fonts.
typeSpecimen = VariableTypeSpecimen([amstelVarName], showGrid=DEBUG)
# Build the pages of the publication, interpreting the font list.
typeSpecimen.build()
# Export the document of the publication to PDF.
typeSpecimen.export(OUTPUT_FILE)


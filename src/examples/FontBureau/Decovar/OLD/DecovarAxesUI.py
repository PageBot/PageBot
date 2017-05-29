# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     DecovarAxes.py
#
#     Show a page with a single Decovar /A.
#     Open floating window with sliders for each axis. 
#     Glyph is updating for each move of a slider.
#
#     @@@ TODO: Speed could be optimized if we export a new font with just one glyph.
#     Now the whole font is interpreted if the variaion location changes.
#
from __future__ import division

import pagebot
from pagebot.page import Template
from pagebot.fonttoolbox.objects.font import Font

from pagebot.publications.typespecimen import TypeSpecimen
from pagebot.fonttoolbox.elements.variableglyphs import VariableGlyphs

DEBUG = False # Make True to see grid and element frames.

OUTPUT_FILE = 'DecovarAxes.pdf'

FONT_PATH = pagebot.getFontPath()
DecovarPath = FONT_PATH + 'fontbureau/Decovar-VF_2017-02-06.ttf'
#DecovarPath = u"/Users/petr/git/PageBotTYPETR/src/fonts/BitcountVar/BitcountGrid-GX.ttf"

decovarName = installFont(DecovarPath)

varFont = Font(DecovarPath)

s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'

TERMINALS = ('trmA', 'trmB', 'trmC', 'trmD', 'trmE', 'trmF', 'trmG', 'trmF', 'trmG', 'trmK', 'trmL',)
SKL = ('sklA', 'sklB', 'sklD')
BLD = ('bldA', 'bldB')
WMX = ('wmx2',)

axes = varFont.axes

trmA = axes['trmA'][0]
trmB = axes['trmB'][0]
trmC = axes['trmC'][0]
trmD = axes['trmD'][0]
trmE = axes['trmE'][0]
trmF = axes['trmF'][0]
trmG = axes['trmG'][0]
trmF = axes['trmF'][0]
trmG = axes['trmG'][0]
trmK = axes['trmK'][0]
trmL = axes['trmL'][0]
sklA = axes['sklA'][0]
sklB = axes['sklB'][0]
sklD = axes['sklD'][0]
bldA = axes['bldA'][0]
bldB = axes['bldB'][0]
wmx2 = axes['wmx2'][0]

VARIABLES = []
for axisName, (minValue, defaultValue, maxValue) in axes.items():
    VARIABLES.append(dict(name=axisName, ui='Slider', 
        args=dict(value=defaultValue, minValue=minValue, maxValue=maxValue)))
    globals()[axisName] = defaultValue        
Variable(VARIABLES, globals())

class VariableTypeSpecimen(TypeSpecimen):

    def makeTemplate(self, rs):
        # Template for the main page.
        template = Template(rs) # Create second template. This is for the main pages.
        return template
         
    def buildPages(self, doc):
        # Build the pages, showing axes, samples, etc.
        # Using the first page as cover (to be filled...)
        page = doc[1] 
        location = dict(trmA=trmA, trmB=trmB, trmC=trmC, trmD=trmD, trmE=trmE, 
            trmF=trmF, trmG=trmG, trmK=trmK,
            trmL=trmL, sklA=sklA, sklB=sklB, sklD=sklD, bldA=bldA, bldB=bldB,
            wmx2=wmx2)
        variableGlyphs = VariableGlyphs(varFont, s='A', style=page.style, fontSize=500, location=location) 
        page.place(variableGlyphs, (250, 100))

# Create a new specimen publications and add the list of system fonts.
typeSpecimen = VariableTypeSpecimen([decovarName], showGrid=DEBUG) 
# Build the pages of the publication, interpreting the font list.
typeSpecimen.build()
#typeSpecimen.draw()
# Export the document of the publication to PDF.
typeSpecimen.export(OUTPUT_FILE)


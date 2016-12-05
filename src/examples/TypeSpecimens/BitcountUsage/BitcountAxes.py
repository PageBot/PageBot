# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     AutomaticPageComposition.py
#
#     This script generates an article (in Dutch) of 2009 about the approach to
#     generate automatic layouts, using Style, Galley, Typesetter and Composer classes.
#
from fontTools.ttLib import TTFont

from pagebot import getFormattedString, textBoxBaseLines

import pagebot
reload(pagebot)
import pagebot

import pagebot.style
reload(pagebot.style)
from pagebot.style import getRootStyle, LEFT_ALIGN

import pagebot.document 
reload(pagebot.document)
from pagebot.document import Document

import pagebot.page
reload(pagebot.page)
from pagebot.page import Page, Template

import pagebot.composer
reload(pagebot.composer)
from pagebot.composer import Composer

import pagebot.typesetter
reload(pagebot.typesetter)
from pagebot.typesetter import Typesetter

import pagebot.elements
reload(pagebot.elements)
from pagebot.elements import Galley, Rect

import pagebot.fonttoolbox.elements.variationcube
reload(pagebot.fonttoolbox.elements.variationcube)
from pagebot.fonttoolbox.elements.variationcube import VariationCube

import pagebot.fonttoolbox.variationbuilder
reload(pagebot.fonttoolbox.variationbuilder)
from pagebot.fonttoolbox.variationbuilder import getVariationFont, drawGlyphPath
    
DEBUG = False

SHOW_GRID = DEBUG
SHOW_GRID_COLUMNS = DEBUG
SHOW_BASELINE_GRID = DEBUG
SHOW_FLOW_CONNECTIONS = DEBUG

EXPORT_PATH = 'export/variableFontDesign.pdf'
  
# Get the default root style and overwrite values for this document.
U = 7
baselineGrid = 2*U
listIndent = 1.5*U

RS = getRootStyle(
    u = U, # Page base unit
    # Basic layout measures altering the default rooT STYLE.
    w = 595, # Om root level the "w" is the page width 210mm, international generic fit.
    h = 11 * 72, # Page height 11", international generic fit.
    ml = 7*U, # Margin left rs.mt = 7*U # Margin top
    baselineGrid = baselineGrid,
    g = U, # Generic gutter.
    # Column width. Uneven means possible split in 5+1+5 or even 2+1+2 +1+ 2+1+2
    # 11 is a the best in that respect for column calculation.
    cw = 11*U, 
    ch = 6*baselineGrid - U, # Approx. square and fitting with baseline.
    listIndent = listIndent, # Indent for bullet lists
    listTabs = [(listIndent, LEFT_ALIGN)], # Match bullet+tab with left indent.
    # Display option during design and testing
    showGrid = SHOW_GRID,
    showGridColumns = SHOW_GRID_COLUMNS,
    showBaselineGrid = SHOW_BASELINE_GRID,
    showFlowConnections = SHOW_FLOW_CONNECTIONS,
    # Text measures
    leading = baselineGrid,
    rLeading = 0,
    fontSize = 9
)
# Tracking presets
H1_TRACK = H2_TRACK = 0.015 # 1/1000 of fontSize, multiplier factor.
H3_TRACK = 0.030 # Tracking as relative factor to font size.
P_TRACK = 0.030

ROOT_DIR = '/'.join(pagebot.__file__.split('/')[:-2]) + '/'
FONT_DIR = ROOT_DIR + 'fonts/'
FONT_NAME = 'BitcountGrid-GX.ttf'
FONT_PATH = FONT_DIR + FONT_NAME

AXES_LOCATIONS = (
    (('line', 'wght'),  {'line': 0, 'open': 0, 'rndi': 1000, 'rndo': 1000, 'sqri':1000, 'sqro':1000, 'wght':1000}),
    (('line', 'wght'),  {'line': 0, 'open': 0, 'rndi': 500, 'rndo': 0, 'sqri':1000, 'sqro':1000, 'wght':1000}),
    (('line', 'open'),  {'line': 0, 'open': 0, 'rndi': 500, 'rndo': 0, 'sqri':1000, 'sqro':1000, 'wght':1000}),
    (('line', 'wght'),  {'line': 0, 'open': 500, 'rndi': 500, 'rndo': 0, 'sqri':1000, 'sqro':1000, 'wght':1000}),
    (('line', 'open'),  {'line': 0, 'open': 1000, 'rndi': 1000, 'rndo': 1000, 'sqri':1000, 'sqro':1000, 'wght':500}),
    )
# -----------------------------------------------------------------         
def makeSpecimen(rs):
        
    # Template 1
    template1 = Template(rs) # Create template of main size. Front page only.
    # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True
    template1.grid(rs) 
    # Show baseline grid if rs.showBaselineGrid is True
    template1.baselineGrid(rs)
   
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template2
    doc = Document(rs, pages=1, template=template1) 
    page = doc[1]
    """
    for (axis1, axis2), location in AXES_LOCATIONS:
        vCube = VariationCube(FONT_PATH, w=500, h=500, s='a', fontSize=86, dimensions={axis1:8, axis2:8}, location=location)
        page.place(vCube, 50, 160)
        page = doc.newPage()
    """
    vMasterFont = TTFont(FONT_PATH)
    for c in ((0.2, 0, 0.5), (1, 0, 0), (0, 0.1, 0)):
        for ix in range(15):
            for iy in range(15):
                location = {'line': int(random()*1000), 'open': int(random()*1000), 'rndi': int(random()*1000), 'rndo': int(random()*1000), 'sqri': int(random()*1000), 'sqro': int(random()*1000), 'wght': int(random()*1000)}
                drawGlyphPath(vMasterFont, 'a', 50 + ix * 500/8, 50 + iy * 500/8, location=location, s=0.09, fillColor=c)
        #page = doc.newPage()

    return doc
        
d = makeSpecimen(RS)
d.export(EXPORT_PATH) 


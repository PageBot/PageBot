# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in Drawbot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     AutomaticLayout.py
#
#     This script generates an article in Dustch the apporach to
#     generate automatic layouts, using Galley, Typesetter and Composer classes.
#
from time import time

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
from pagebot.elements import Galley

import pagebot.fonttoolbox.variationbuilder
reload(pagebot.fonttoolbox.variationbuilder)
from pagebot.fonttoolbox.variationbuilder import generateInstance

SHOW_TIMER = False

SHOW_GRID = True
SHOW_GRID_COLUMNS = True
SHOW_BASELINE_GRID = True
SHOW_FLOW_CONNECTIONS = True

if SHOW_GRID:
    BOX_COLOR = (0.8, 0.8, 0.8, 0.4)
else:
    BOX_COLOR = None
    
# Get the default root style and overwrite values for this document.
U = 7
baselineGrid = 2*U
listIndent = 2*U

rs = getRootStyle(
    u = U, # Page base unit
    # Basic layout measures altering the default rooT STYLE.
    pw = 595, # Page width 210mm, international generic fit.
    ph = 11 * 72, # Page height 11", international generic fit.
    ml = 7*U, # Margin leftrs.mt = 7*U # Margin top
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
    showBaselineGrid = False,
    showFlowConnections = SHOW_FLOW_CONNECTIONS,
    BOX_COLOR = BOX_COLOR,
    # Text measures
    leading = baselineGrid,
    rLeading = 0,
    fontSize = 9
)
    # LANGUAGE-SWITCH Language settings
if 0: # EN version of the article.
    rs['langauge'] = 'en'
    MD_PATH = 'automaticPageComposition_en.md'
    EXPORT_PATH = 'export/AutomaticPageComposition.pdf'
else: # NL version of the article.
    rs['language'] = 'nl-be' # Make Dutch hyphenation.
    MD_PATH = 'automatischePaginaCompositie_nl.md'
    EXPORT_PATH = 'export/AutomatischePaginaOpmaak.pdf'

MAIN_FLOW = 'main' # ELement id of the text box on pages the hold the main text flow.

# Tracking presets
H1_TRACK = H2_TRACK = 0.015 # 1/1000 of fontSize, multiplier factor.
H3_TRACK = 0.030 # Tracking as relative factor to font size.
P_TRACK = 0.030

VARS = True

if VARS:
    FONT_PATH = '../../fonts/'

    FONT_LOCATIONS = {
        #'Promise-BoldCondensed': {"wght": 750, "wdth": 500, },
        #'Promise-LightCondensed': {"wght": 0, "wdth": 500},
        'Promise-Light': {"wght": 0, "wdth": 1000},
        'Promise-Book': {"wght": 250, "wdth": 1000},
        'Promise-Regular': {"wght": 400, "wdth": 1000},    
        'Promise-Medium': {"wght": 600, "wdth": 1000},    
        'Promise-Semibold': {"wght": 750, "wdth": 1000},    
        'Promise-Bold': {"wght": 1000, "wdth": 1000},
    }
    FONTS = {}
    # Install the test V-font
    if not 'Promise-Bold' in installedFonts():
        installFont(FONT_PATH + 'Promise-GX.ttf')
    for name, location in FONT_LOCATIONS.items():
        fontName, fontPath = generateInstance(FONT_PATH + 'Promise-GX.ttf', 
        location, targetDirectory=FONT_PATH + 'instances')
        FONTS[name] = fontName#fontPath # Instead of fontName, no need to uninstall.
    if 0:
        BOOK = FONTS['Promise-LightCondensed']
        BOOK_ITALIC = FONTS['Promise-LightCondensed']
        MEDIUM = FONTS['Promise-LightCondensed']
        SEMIBOLD = FONTS['Promise-LightCondensed']
        BOLD = FONTS['Promise-LightCondensed']
    else:
        LIGHT = FONTS['Promise-Light']
        BOOK = FONTS['Promise-Book']
        BOOK_ITALIC = FONTS['Promise-Book']
        MEDIUM = FONTS['Promise-Medium']
        SEMIBOLD = FONTS['Promise-Semibold']
        BOLD = FONTS['Promise-Bold']
else:
    BOOK = MEDIUM = 'Verdana'
    BOOK_ITALIC = 'Verdana-Italic'
    BOLD = SEMIBOLD = 'Verdana-Bold'
# -----------------------------------------------------------------         
def makeDocument():
    u"""Demo page composer."""
    tt = time() # Keep track of time, in case SHOW_TIMER is True

    # Set some values of the default template (as already generated by the document).
    # Make squential unique names for the flow boxes inside the templates
    flowId0 = MAIN_FLOW+'0' 
    flowId1 = MAIN_FLOW+'1'
    flowId2 = MAIN_FLOW+'2'
    
    # Template 1
    template1 = Template(rs) # Create template of main size. Front page only.
    # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True
    template1.grid(rs) 
    # Show baseline grid if rs.showBaselineGrid is True
    template1.baselineGrid(rs)
    # Create empty image place holders. To be filled by running content on the page.
    template1.cContainer(4, 0, 2, 4, rs)  # Empty image element, cx, cy, cw, ch
    template1.cContainer(0, 5, 2, 3, rs)
    # Create linked text boxes. Note the "nextPage" to keep on the same page or to next.
    template1.cTextBox('', 0, 0, 2, 5, rs, flowId0, nextBox=flowId1, nextPage=0, fill=BOX_COLOR)
    template1.cTextBox('', 2, 0, 2, 8, rs, flowId1, nextBox=flowId2, nextPage=0, fill=BOX_COLOR)
    template1.cTextBox('', 4, 4, 2, 4, rs, flowId2, nextBox=flowId0, nextPage=1, fill=BOX_COLOR)
    # Create page number box. Pattern pageNumberMarker is replaced by actual page number.
    template1.cText(rs['pageNumberMarker'], 6, 0, rs, font=BOOK, fontSize=12, fill=BOX_COLOR)

    # Template 2
    template2 = Template(rs) # Create second template. This is for the main pages.
    # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True
    template2.grid(rs) 
    # Show baseline grid if rs.showBaselineGrid is True
    template2.baselineGrid(rs)
    template2.cContainer(4, 0, 2, 3, rs)  # Empty image element, cx, cy, cw, ch
    template2.cContainer(0, 5, 2, 3, rs)
    template2.cContainer(2, 2, 2, 2, rs)
    template2.cContainer(2, 0, 2, 2, rs)
    template2.cContainer(4, 6, 2, 2, rs)
    template2.cTextBox('', 0, 0, 2, 5, rs, flowId0, nextBox=flowId1, nextPage=0, fill=BOX_COLOR)
    template2.cTextBox('', 2, 4, 2, 4, rs, flowId1, nextBox=flowId2, nextPage=0, fill=BOX_COLOR)
    template2.cTextBox('', 4, 3, 2, 3, rs, flowId2, nextBox=flowId0, nextPage=1, fill=BOX_COLOR)
    # Create page number box. Pattern pageNumberMarker is replaced by actual page number.
    template2.cText(rs['pageNumberMarker'], 6, 0, rs, font=BOOK, fontSize=12, fill=BOX_COLOR)
   
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template2
    doc = Document(rs, pages=2, template=template2) 
 
    # Cache some values from the root style that we need multiple time to create the tag styles.
    fontSize = rs['fontSize']
    leading = rs['leading']
    rLeading = rs['rLeading']
    listIndent = rs['listIndent']
    language = rs['language']
    
    # Add styles for whole document and text flows.  
    # Note that some values are defined here for clarity, even if their default root values
    # are the same.             
    doc.newStyle(name='chapter', font=BOOK)    
    doc.newStyle(name='title', fontSize=3*fontSize, font=BOLD)
    doc.newStyle(name='subtitle', fontSize=2*fontSize, font=BOOK_ITALIC)
    doc.newStyle(name='author', fontSize=2*fontSize, font=BOOK, fill=(1, 0, 0))
    doc.newStyle(name='h1', fontSize=2*fontSize, font=SEMIBOLD, fill=(1, 0, 0),
        leading=2*fontSize, tracking=H1_TRACK, postfix='\n')
    doc.newStyle(name='h2', fontSize=1.5*fontSize, font=SEMIBOLD, fill=(0, 0.5, 1),
        leading=1*fontSize, rLeading=0, tracking=H2_TRACK, postfix='\n')
    doc.newStyle(name='h3', fontSize=1.2*fontSize, font=MEDIUM, fill=0, 
        leading=1.5*fontSize, rLeading=0, rNeedsBelow=2*rLeading, tracking=H3_TRACK,
        paragraphTopSpacing=U, paragraphBottomSpacing=U/2, postfix='\n')
    
    # Spaced paragraphs.
    doc.newStyle(name='p', fontSize=fontSize, font=BOOK, fill=0.1, prefix='', postfix='\n',
        rTracking=P_TRACK, align=LEFT_ALIGN, hyphenation=True)
    doc.newStyle(name='b', font=SEMIBOLD)
    doc.newStyle(name='em', font=BOOK_ITALIC)
    doc.newStyle(name='hr', stroke=(1, 0, 0), strokeWidth=4)
    doc.newStyle(name='br', postfix='\n')
    doc.newStyle(name='img', leading=leading, fontSize=fontSize, font=BOOK,)
    
    # Footnote reference index.
    doc.newStyle(name='sup', font=MEDIUM, rBaselineShift=0.6,
        fontSize=0.65*fontSize)
    doc.newStyle(name='li', fontSize=fontSize, font=BOOK, 
        tracking=P_TRACK, leading=leading, hyphenation=True, 
        # Lists need to copy the listIndex over to the regalar style value.
        tabs=[(listIndent, LEFT_ALIGN)], indent=listIndent, 
        firstLineIndent=1, postfix='\n')
    doc.newStyle(name='ul',)
    doc.newStyle(name='literatureref', fill=0.5, rBaselineShift=0.2, fontSize=0.8*fontSize)
    doc.newStyle(name='footnote', fill=(1, 0, 0), fontSize=0.8*U, font=BOOK)
    doc.newStyle(name='caption', tracking=P_TRACK, language=language, fill=0.2, 
        leading=leading*0.8, fontSize=0.8*fontSize, font=BOOK_ITALIC, 
        indent=U/2, tailIndent=-U/2, hyphenation=True)

    if SHOW_TIMER:
        print 'Time styles %0.3f' % (time()-tt)
        tt = time()
    
    # Change template of page 1
    doc[0].setTemplate(template1)
    if SHOW_TIMER:
        print 'Time template %0.3f' % (time()-tt)
        tt = time()
    
    # Create main Galley for this page, for pasting the sequence of elements.    
    g = Galley() 
    t = Typesetter(doc, g)
    t.typesetFile(MD_PATH)
    
    if SHOW_TIMER:
        print 'Time typesetter %0.3f' % (time()-tt)
        tt = time()
    
    # Fill the main flow of text boxes with the ML-->XHTML formatted text. 
    c = Composer(doc)
    c.compose(g, doc[0], flowId0)
    
    if SHOW_TIMER:
        print 'Time compose %0.3f' % (time()-tt)
    
    return doc
        
tt = time()
d = makeDocument()
if SHOW_TIMER:
    print 'Make document %0.3f' % (time()-tt)

tt = time()
d.export(EXPORT_PATH) 
if SHOW_TIMER:
    print 'Time export %0.3f' % (time()-tt)


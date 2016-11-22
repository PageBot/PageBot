# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     Healthy.py
#
from datetime import datetime # Make date fit today.
from pagebot import getFormattedString

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

PREVIEW = False

SHOW_GRID = PREVIEW
SHOW_GRID_COLUMNS = PREVIEW
SHOW_BASELINE_GRID = PREVIEW
SHOW_FLOW_CONNECTIONS = PREVIEW

if SHOW_GRID:
    BOX_COLOR = (0.8, 0.8, 0.8, 0.4)
else:
    BOX_COLOR = None
    
# Get the default root style and overwrite values for this document.
U = 7
baselineGrid = 2*U
listIndent = 1.5*U
W = 595
H = 11 * 72

if PREVIEW:
    docW = docH = None # Document same size as pages, don't show crop-marks
else:
    docW = W+50
    docH = H+50
    
RS = getRootStyle(
    u = U, # Page base unit
    # Basic layout measures altering the default rooT STYLE.
    w = W, # On root level the "w" is the page width 595pt ~ 210mm, international generic fit.
    h = H, # 11 * 72 Page height 11", international generic fit.
    docW = docW, # Oversize document to shoq crop-marks
    docH = docH,
    ml = 7*U, # Margin left rs.mt = 7*U # Margin top
    baselineGrid = 14,#baselineGrid,
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
    BOX_COLOR = BOX_COLOR,
    # Text measures
    leading = 14,
    rLeading = 0,
    fontSize = 9
)
FS = getFormattedString(FormattedString(''), RS)

# LANGUAGE-SWITCH Language settings
RS['language'] = 'en'
MD_PATH = 'lemonHerbChicken.md'
EXPORT_PATH = 'export/CookBotBook.pdf'
COVER_IMAGE_PATH1 = 'images/cookbot2.jpg'
COVER_IMAGE_PATH2 = 'images/cookbot3.jpg'
COVER_IMAGE_PATH3 = 'images/cookbot4.jpg'
COVER_IMAGE_PATH4 = 'images/cookbot5.jpg'
COVER_IMAGE_PATH5 = 'images/cookbot6.jpg'

#MD_PATH = 'testPaginaCompositie_nl.md'

MAIN_FLOW = 'main' # ELement id of the text box on pages the hold the main text flow.

# Tracking presets
H1_TRACK = H2_TRACK = 0.015 # 1/1000 of fontSize, multiplier factor.
H3_TRACK = 0.030 # Tracking as relative factor to font size.
P_TRACK = 0.030

VARS = True

if VARS:
    FONT_PATH = '../../fonts/'

    FONT_LOCATIONS = {
        #'PromisePageBot-BoldCondensed': {"wght": 750, "wdth": 500, },
        #'PromisePageBot-LightCondensed': {"wght": 0, "wdth": 500},
        'PromisePageBot-Thin': {"wght": 0, "wdth": 1000},
        'PromisePageBot-Light': {"wght": 100, "wdth": 1000},
        'PromisePageBot-Book': {"wght": 250, "wdth": 1000},
        'PromisePageBot-BookCondensed': {"wght": 250, "wdth": 800},
        'PromisePageBot-Regular': {"wght": 400, "wdth": 1000},    
        'PromisePageBot-Medium': {"wght": 600, "wdth": 1000},    
        'PromisePageBot-Semibold': {"wght": 750, "wdth": 1000},    
        'PromisePageBot-SemiboldCondensed': {"wght": 250, "wdth": 100},    
        'PromisePageBot-Bold': {"wght": 1000, "wdth": 1000},
    }
    FONTS = {}
    VFONT_PATH = 'PromisePageBot-GX.ttf'
    # Install the test V-font
    if not 'PromisePageBot-Bold' in installedFonts():
        installFont(FONT_PATH + VFONT_PATH)
    for name, location in FONT_LOCATIONS.items():
        fontName, fontPath = generateInstance(FONT_PATH + VFONT_PATH, 
            location, targetDirectory=FONT_PATH + 'instances')
        FONTS[name] = fontName#fontPath # Instead of fontName, no need to uninstall.
    THIN = FONTS['PromisePageBot-Thin']
    LIGHT = FONTS['PromisePageBot-Light']
    BOOK_CONDENSED = FONTS['PromisePageBot-BookCondensed']
    BOOK = FONTS['PromisePageBot-Book']
    BOOK_ITALIC = FONTS['PromisePageBot-Book']
    MEDIUM = FONTS['PromisePageBot-Medium']
    SEMIBOLD = FONTS['PromisePageBot-Semibold']
    SEMIBOLD_CONDENSED = FONTS['PromisePageBot-SemiboldCondensed'] 
    BOLD = FONTS['PromisePageBot-Bold']
else:
    BOOK = MEDIUM = 'Georgia'
    BOOK_ITALIC = 'Georgia-Italic'
    BOLD = SEMIBOLD = 'Georgia-Bold'

RS['font'] = BOOK

def makeCoverTemplate(imagePath, rs):
    bleed = rs['bleed']
    # Cover
    coverTemplate = Template(rs) # Cover template of the magazine.
    coverTemplate.image(imagePath, -200, -bleed, h=rs['h'] + 2 * bleed)
    coverTitle = FormattedString('Healthy', font=LIGHT, fontSize=180, fill=1, tracking=-9)
    coverTemplate.text(coverTitle, 10, rs['h'] - 148)
    
    # Make actual date in top-right with magazine title.
    dt = datetime.now()
    d = dt.strftime("%B %Y")
    fs = FormattedString(d, font=MEDIUM, fontSize=18, fill=1, tracking=0.5)
    coverTemplate.text(fs, 436, rs['h'] - 26)

    # Titles could come automatic from chapters in the magazine.
    fs = FormattedString('$4.90', font=BOOK, fontSize=12, fill=1, tracking=0.5,
        lineHeight=12 )
    coverTemplate.text(fs, 540, rs['h'] - 765)
  
    return coverTemplate
       
# -----------------------------------------------------------------         
def makeDocument(rs):
    u"""Demo page composer."""

    # Set some values of the default template (as already generated by the document).
    # Make squential unique names for the flow boxes inside the templates
    flowId1 = MAIN_FLOW+'1' 
    flowId2 = MAIN_FLOW+'2'
    flowId3 = MAIN_FLOW+'3'

    coverTemplate1 = makeCoverTemplate(COVER_IMAGE_PATH1, rs)
    coverTemplate2 = makeCoverTemplate(COVER_IMAGE_PATH2, rs)
    coverTemplate3 = makeCoverTemplate(COVER_IMAGE_PATH3, rs)
    coverTemplate4 = makeCoverTemplate(COVER_IMAGE_PATH4, rs)
    coverTemplate5 = makeCoverTemplate(COVER_IMAGE_PATH5, rs)
    
    # Titles could come automatic from chapters in the magazine.
    fs = FormattedString('Lemon Herb\nChicken', font=BOOK_CONDENSED, fontSize=48, fill=1, tracking=0.5,
        lineHeight=48)
    coverTemplate1.text(fs, 22, rs['h'] - 270)

    # Titles could come automatic from chapters in the magazine.
    fs = FormattedString('Seasonal:\n', font=MEDIUM, fontSize=32, fill=1, tracking=0.5,
        lineHeight=34)
    fs += FormattedString('Hot served dinners', font=BOOK, fontSize=32, fill=1, tracking=0.5,
        lineHeight=34)
    coverTemplate1.text(fs, 22, rs['h'] - 420)
        
    # Titles could come automatic from chapters in the magazine.
    fs = FormattedString('Cranberry\nBean Sauce', font=LIGHT, fontSize=60, fill=1, tracking=0.5,
        lineHeight=52 )
    coverTemplate1.text(fs, 18, rs['h'] - 690)
        
    # Titles could come automatic from chapters in the magazine.
    fs = FormattedString('Arizona:\n', font=MEDIUM, fontSize=32, fill=1, tracking=0.5,
        lineHeight=34)
    fs += FormattedString('Cran-Turkey Enchilada', font=BOOK, fontSize=32, fill=1, tracking=0.5,
        lineHeight=34)
    coverTemplate1.text(fs, 22, rs['h'] - 730)
        
    # Titles could come automatic from chapters in the magazine.
    fs = FormattedString('Fresh', font=MEDIUM, fontSize=60, fill=(1, 1, 1, 0.5), tracking=0.5,
        lineHeight=52 )
    coverTemplate1.text(fs, 400, rs['h'] - 270)
                
 
    # Template 16
    template1 = Template(rs) # Create template of main size. Front page only.
    # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True
    template1.grid(rs) 
    # Show baseline grid if rs.showBaselineGrid is True
    template1.baselineGrid(rs)
    # Create empty image place holders. To be filled by running content on the page.
    template1.cContainer(2, -0.7, 5, 4, rs)  # Empty image element, cx, cy, cw, ch
    template1.cContainer(0, 5, 2, 3, rs)
    # Create linked text boxes. Note the "nextPage" to keep on the same page or to next.
    template1.cTextBox(FS, 0, 0, 2, 5, rs, flowId1, nextBox=flowId2, nextPage=0, fill=BOX_COLOR)
    template1.cTextBox(FS, 2, 3, 2, 5, rs, flowId2, nextBox=flowId3, nextPage=0, fill=BOX_COLOR)
    template1.cTextBox(FS, 4, 3, 2, 5, rs, flowId3, nextBox=flowId1, nextPage=1, fill=BOX_COLOR)
    # Create page number box. Pattern pageNumberMarker is replaced by actual page number.
    template1.cText(FS+rs['pageIdMarker'], 6, 0, style=rs, font=BOOK, fontSize=12, fill=BOX_COLOR)

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
    template2.cTextBox(FS, 0, 0, 2, 5, rs, flowId1, nextBox=flowId2, nextPage=0, fill=BOX_COLOR)
    template2.cTextBox(FS, 2, 4, 2, 4, rs, flowId2, nextBox=flowId3, nextPage=0, fill=BOX_COLOR)
    template2.cTextBox(FS, 4, 3, 2, 3, rs, flowId3, nextBox=flowId1, nextPage=1, fill=BOX_COLOR)
    # Create page number box. Pattern pageNumberMarker is replaced by actual page number.
    template2.cText(FS+rs['pageIdMarker'], 6, 0, style=rs, font=BOOK, fontSize=12, fill=BOX_COLOR)
   
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template2.
    # Oversized document (docW, docH) is defined in the rootStyle.
    doc = Document(rs, pages=6, template=template2) 
 
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
    doc.newStyle(name='subtitle', fontSize=2.6*fontSize, font=BOOK_ITALIC)
    doc.newStyle(name='author', fontSize=2*fontSize, font=BOOK, fill=(1, 0, 0))
    doc.newStyle(name='h1', fontSize=3.85*fontSize, font=SEMIBOLD_CONDENSED, fill=(1, 0, 0), 
        leading=2.5*leading, tracking=H1_TRACK, postfix='\n')
    doc.newStyle(name='h2', fontSize=1.5*fontSize, font=SEMIBOLD, 
        fill=0, leading=1*leading, rLeading=0, tracking=H2_TRACK, 
        prefix='', postfix='\n')
    doc.newStyle(name='h3', fontSize=1.1*fontSize, font=MEDIUM, fill=0, 
        leading=leading, rLeading=0, rNeedsBelow=2*rLeading, tracking=H3_TRACK,
        prefix='\n', postfix='\n')
    doc.newStyle(name='h4', fontSize=1.1*fontSize, font=BOOK, fill=0, 
        leading=leading, rLeading=0, rNeedsBelow=2*rLeading, tracking=H3_TRACK,
        paragraphTopSpacing=U, paragraphBottomSpacing=U, prefix='\n', postfix='\n')
    
    # Spaced paragraphs.
    doc.newStyle(name='p', fontSize=fontSize, font=BOOK, fill=0.1, prefix='', postfix='\n',
        rTracking=P_TRACK, leading=14, rLeading=0, align=LEFT_ALIGN, hyphenation=True)
    doc.newStyle(name='b', font=SEMIBOLD)
    doc.newStyle(name='em', font=BOOK_ITALIC)
    doc.newStyle(name='hr', stroke=(1, 0, 0), strokeWidth=4)
    doc.newStyle(name='br', postfix='\n') # Simplest way to make <br/> show newline
    doc.newStyle(name='a', prefix='', postfix='')
    doc.newStyle(name='img', leading=leading, fontSize=fontSize, font=BOOK)
    
    # Footnote reference index.
    doc.newStyle(name='sup', font=MEDIUM, rBaselineShift=0.6, prefix='', postfix=' ',
        fontSize=0.6*fontSize)
    doc.newStyle(name='li', fontSize=fontSize, font=BOOK, 
        tracking=P_TRACK, leading=leading, hyphenation=True, 
        # Lists need to copy the listIndex over to the regalar style value.
        tabs=[(listIndent, LEFT_ALIGN)], indent=listIndent, 
        firstLineIndent=1, postfix='\n')
    doc.newStyle(name='ul', prefix='', postfix='')
    doc.newStyle(name='literatureref', fill=0.5, rBaselineShift=0.2, fontSize=0.8*fontSize)
    doc.newStyle(name='footnote', fill=(1, 0, 0), fontSize=0.8*U, font=BOOK)
    doc.newStyle(name='caption', tracking=P_TRACK, language=language, fill=0.2, 
        leading=leading*0.8, fontSize=0.8*fontSize, font=BOOK_ITALIC, 
        indent=U/2, tailIndent=-U/2, hyphenation=True)
    
    # Change template of page 1
    page1 = doc[1]
    page1.setTemplate(coverTemplate1)
    
    page2 = doc[2]
    page2.setTemplate(coverTemplate2)
    
    page3 = doc[3]
    page3.setTemplate(coverTemplate3)
    
    page4 = doc[4]
    page4.setTemplate(coverTemplate4)
    
    page5 = doc[5]
    page5.setTemplate(coverTemplate5)
    
    page6 = doc[6]
    page6.setTemplate(template1)
    
    # Create main Galley for this page, for pasting the sequence of elements.    
    g = Galley() 
    t = Typesetter(doc, g)
    t.typesetFile(MD_PATH)
    
    # Fill the main flow of text boxes with the ML-->XHTML formatted text. 
    c = Composer(doc)
    c.compose(g, page6, flowId1)
    
    return doc
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 


# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
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
from pagebot import textBoxBaseLines

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
# Page and Template instances are holding all elements of a page together.
from pagebot.page import Page, Template
# The Typesetter instance takes content from a file (typically MarkDown text) and converts that 
# into Galley list of elements.
from pagebot.typesetter import Typesetter
# The Composer instance distributes the Galley content of the pages, according to the defined Templates.
from pagebot.composer import Composer
# Elements that can placed on pages and templates.
from pagebot.elements import Galley, Rect
# Get functions to create instances style from Variable fonts.
from pagebot.fonttoolbox.variablebuilder import getVariableFont

# Some flags to turn on/off extra debug information on the output pages.    
DEBUG = True

SHOW_GRID = DEBUG
SHOW_GRID_COLUMNS = DEBUG
SHOW_BASELINE_GRID = DEBUG
SHOW_FLOW_CONNECTIONS = DEBUG

# Optional the columns can be shown in transparant color.
if SHOW_GRID:
    BOX_COLOR = (0.8, 0.8, 0.8, 0.4)
else:
    BOX_COLOR = None
    
# Get the default root style and overwrite values for this example document.
U = 7 # Basic unit measure for the whole layout.
baselineGrid = 2*U
listIndent = 1.5*U

# Create a RootStyle instance by calling function. Alter some of the default values
# on initialization, so we don't that to replace them later for our version of the 
# root style.
RS = getRootStyle(
    u = U, # Page base unit
    # Basic layout measures altering the default rooT STYLE.
    w = 595, # Om root level the "w" is the page width 210mm, international generic fit.
    h = 11 * 72, # Page height 11", international generic fit.
    ml = 7*U, # Margin left rs.mt = 7*U # Margin top
    baselineGrid = baselineGrid, # Set the baseline grid, as shown when SHOW_BASELINE_GRID is True.
    gw = 2*U, # Generic gutter, equal for width and height
    gh = 2*U,
    # Column width. Uneven means possible split in 5+1+5 or even 2+1+2 +1+ 2+1+2
    # 11 is a the best in that respect for column calculation.
    cw = 11*U, 
    ch = 6*baselineGrid - U, # Approx. square and fitting with baseline.
    listIndent = listIndent, # Indent for bullet lists
    listTabs = [(listIndent, LEFT)], # Match bullet+tab with left indent.
    # Display option during design and testing. Pass the debug paramers into the root style.
    showGrid = SHOW_GRID,
    showGridColumns = SHOW_GRID_COLUMNS,
    showBaselineGrid = SHOW_BASELINE_GRID,
    showFlowConnections = SHOW_FLOW_CONNECTIONS,
    BOX_COLOR = BOX_COLOR,
    # Text measures
    leading = baselineGrid, # Basic leading of body text as fixed value (indepdent of font size) to 2 x U = 14.
    rLeading = 0, # Set relative leading (dependent on font size) to 0.
    fontSize = U+2 # Set default font size of body text to U + 2 = 9 pt.
)

if 0: # In case an English MarkDown text of this example article is ready.
    RS['language'] = 'en' # Tell RootStyle instance to use Englisch hyphenation.
    MD_PATH = 'automaticPageComposition_en.md' # Path of the MarkDown text in local folder.
    EXPORT_PATH = '_export/AutomaticPageComposition.pdf' # Export part of generated PDF output document.
else: # NL version of the article.
    RS['language'] = 'nl-be' # Tell RootStyle instance to use Dutch hyphenation..
    MD_PATH = 'automatischePaginaCompositie_nl.md' # Path of the MarkDown text in local folder.
    EXPORT_PATH = '_export/AutomatischePaginaOpmaak.pdf' # Export part of generated PDF output document.

MAIN_FLOW = 'main' # ELement id of the text box on pages the hold the main text flow.

# Some tracking presets
H1_TRACK = H2_TRACK = 0.015 # 1/1000 of fontSize, multiplier factor.
H3_TRACK = 0.030 # Tracking as relative factor to font size.
P_TRACK = 0.030

# Path to the Variable font source, from which width/weight instances will be created.
FONT_PATH = '../../fonts/PromisePageBot-GX.ttf'
# Create instance, depending on the location in the Variable axes.
LIGHT = getVariableFont(FONT_PATH, {"wght": 100, "wdth": 1000})
LIGHT_CONDENSED = getVariableFont(FONT_PATH, {"wght": 100, "wdth": 800})
BOOK_LIGHT = getVariableFont(FONT_PATH, {"wght": 175, "wdth": 1000})
BOOK_CONDENSED = getVariableFont(FONT_PATH, {"wght": 250, "wdth": 800})
BOOK = getVariableFont(FONT_PATH, {"wght": 250, "wdth": 1000})
BOOK_ITALIC = getVariableFont(FONT_PATH, {"wght": 250, "wdth": 1000})
MEDIUM = getVariableFont(FONT_PATH, {"wght": 400, "wdth": 1000})
SEMIBOLD = getVariableFont(FONT_PATH, {"wght": 400, "wdth": 1000})
SEMIBOLD_CONDENSED = getVariableFont(FONT_PATH, {"wght": 600, "wdth": 500})
BOLD = getVariableFont(FONT_PATH, {"wght": 800, "wdth": 1000})
BOLD_ITALIC = getVariableFont(FONT_PATH, {"wght": 800, "wdth": 1000})
BLACK = getVariableFont(FONT_PATH, {"wght": 1000, "wdth": 1000})

RS['font'] = BOOK

# -----------------------------------------------------------------         
def makeDocument(rs):
    u"""Demo page composer."""

    # Set some values of the default template (as already generated by the document).
    # Make squential unique names for the flow boxes inside the templates
    flowId1 = MAIN_FLOW+'1' 
    flowId2 = MAIN_FLOW+'2'
    flowId3 = MAIN_FLOW+'3'
        
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
    template1.cTextBox(FS, 0, 0, 2, 5, rs, flowId1, nextBox=flowId2, nextPage=0, fill=BOX_COLOR)
    template1.cTextBox(FS, 2, 0, 2, 8, rs, flowId2, nextBox=flowId3, nextPage=0, fill=BOX_COLOR)
    template1.cTextBox(FS, 4, 4, 2, 4, rs, flowId3, nextBox=flowId1, nextPage=1, fill=BOX_COLOR)
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
    # Initially make all pages default with template2
    doc = Document(rs, autoPages=1, template=template2) 
 
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
    doc.newStyle(name='author', fontSize=2*fontSize, font=BOOK, textFill=(1, 0, 0))
    doc.newStyle(name='h1', fontSize=2.6*fontSize, font=SEMIBOLD_CONDENSED, textFill=0.2, 
        leading=2.6*fontSize, tracking=H1_TRACK, prefix='\n', postfix='\n', 
        paragraphTopSpacing=U, paragraphBottomSpacing=U)
    doc.newStyle(name='h2', fontSize=2*fontSize, font=LIGHT_CONDENSED, textFill=(1, 0, 0),
        leading=2.2*leading, rLeading=0, tracking=H2_TRACK, 
        prefix='', postfix='\n')
    doc.newStyle(name='h3', fontSize=1.1*fontSize, font=MEDIUM, textFill=0, 
        leading=1.4*fontSize, rLeading=0, rNeedsBelow=2*rLeading, tracking=H3_TRACK,
        prefix='', postfix='\n')
    # paragraphTopSpacing=U, paragraphBottomSpacing=U only work if there is a prefix/postfix
    doc.newStyle(name='h4', fontSize=1.1*fontSize, font=BOOK, textFill=0, 
        leading=leading, rLeading=0, rNeedsBelow=2*rLeading, tracking=H3_TRACK,
        paragraphTopSpacing=U, paragraphBottomSpacing=U, prefix='\n', postfix='\n')
    
    # Spaced paragraphs.
    doc.newStyle(name='p', fontSize=fontSize, font=BOOK, textFill=0.1, 
        prefix='', postfix='\n',
        rTracking=P_TRACK, leading=14, rLeading=0, xTextAlign=LEFT, hyphenation=True)
    doc.newStyle(name='b', font=SEMIBOLD)
    doc.newStyle(name='em', font=BOOK_ITALIC)
    doc.newStyle(name='hr', stroke=(1, 0, 0), strokeWidth=4)
    doc.newStyle(name='br', postfix='\n') # Simplest way to make <br/> show newline
    doc.newStyle(name='a', prefix='', postfix='')
    doc.newStyle(name='img', leading=leading, fontSize=fontSize, font=BOOK,
        stroke=1, fill=None)
    
    # Footnote reference index.
    doc.newStyle(name='sup', font=MEDIUM, rBaselineShift=0.6, prefix='', postfix=' ',
        fontSize=0.6*fontSize)
    doc.newStyle(name='li', fontSize=fontSize, font=BOOK, 
        tracking=P_TRACK, leading=leading, hyphenation=True, 
        # Lists need to copy the listIndex over to the regalar style value.
        tabs=[(listIndent, LEFT)], indent=listIndent,
        firstLineIndent=1, prefix='', postfix='\n'), 
    doc.newStyle(name='ul', prefix='', postfix='')
    doc.newStyle(name='literatureref', fill=0.5, rBaselineShift=0.2, fontSize=0.8*fontSize)
    doc.newStyle(name='footnote', fill=(1, 0, 0), fontSize=0.8*U, font=BOOK)
    doc.newStyle(name='caption', tracking=P_TRACK, language=language, fill=0.2, 
        leading=leading*0.8, fontSize=0.8*fontSize, font=BOOK_ITALIC, 
        tailIndent=-U/2, hyphenation=True)
    
    # Change template of page 1
    page1 = doc[1]
    page1.setTemplate(template1)
    
    # Create main Galley for this page, for pasting the sequence of elements.    
    galley = Galley() 
    t = Typesetter(doc, galley)
    t.typesetFile(MD_PATH)
    
    # Fill the main flow of text boxes with the ML-->XHTML formatted text. 
    c = Composer(doc)
    c.compose(galley, page1, flowId1)
    
    return doc
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 


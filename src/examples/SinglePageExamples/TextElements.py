# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     TextElements.py
#
#     This script generates a fake article on a single page, using Filibuster text,
#     automatic layout template, Galley, Typesetter and Composer classes.
#
import pagebot # Import to know the path of non-Python resources.

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT, A4, A3, A2, NO_COLOR
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
# Page and Template instances are holding all elements of a page together.
from pagebot.elements.page import Page, Template
# The Typesetter instance takes content from a file (typically MarkDown text) and converts that 
# into Galley list of elements.
from pagebot.typesetter import Typesetter
# The Composer instance distributes the Galley content of the pages, according to the defined Templates.
from pagebot.composer import Composer
# Elements that can placed on pages and templates.
from pagebot.elements import Galley, Rect
# Get functions to create instances style from Variable fonts.
from pagebot.fonttoolbox.variablebuilder import getVariableFont, generateInstance

# For clarity, most of the OnePage.py example document is setup as a sequential excecution of
# Python functions. For complex documents this is not the best method. More functions and classes
# will be used in the real templates, which are available from the OpenSource PageBotTemplates repository.

# Some flags to turn on/off extra debug information on the output pages.    
DEBUG = True

SHOW_GRID = DEBUG # Show the colums as color squares.
SHOW_GRID_COLUMNS = DEBUG # Show the column grid in the background as lines
SHOW_BASELINE_GRID = DEBUG # SHow the baseline grid of body text.
SHOW_FLOW_CONNECTIONS = DEBUG # Show arrow connections between the column flows.

if SHOW_GRID: # If showing ths grid a square, use this transparant color.
    BOX_COLOR = (0.8, 0.8, 0.8, 0.4)
else:
    BOX_COLOR = None # No square columns showing.
    
# Get the default root style and overwrite values for this example one-page document.
U = 7 # Basic unit in points of all measurements on the page. Simple way to do responsive scaling of all elements.
baselineGrid = 2*U # Set baseline grid value for body text.
listIndent = 2*U # Default indent for bullet-list indents.

W, H = A3

G = U # Gutter
CW = 12*U # Creates 6 columns width on A4
CH = 12*U

ML = (W - int((W-CW)/(CW+G))*(CW+G)+G)/2
MT = ML

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot values are filled by their default values. The root style is kept in RS
# as reference to for all ininitialzaiton of elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle(
    u = U, # Page base unit
    # Basic layout measures altering the default rooT STYLE.
    w = W, # On root level the "w" is the page width 210mm, international generic fit.
    h = H, # Page height 11", international generic fit.
    baselineGrid = baselineGrid,
    g = G, # Generic gutter, identical to the page unit.
    # Column width. Uneven means possible split in 5+1+5 or even 2+1+2 +1+ 2+1+2
    # 11 is a the best in that respect for column calculation.
    cw = CW, 
    ch = CH, # Approx. square and fitting with baseline.
    ml = ML, # Margin left between left side of the page and grid, centered.
    mt = MT, # Margin top between page top and grid.
    listIndent = listIndent, # Indent for bullet lists
    listTabs = [(listIndent, LEFT)], # Match bullet+tab with left indent.
    # Display option during design and testing. Copy them in the root style for elements to check on.
    showGrid = SHOW_GRID,
    showGridColumns = SHOW_GRID_COLUMNS,
    showBaselineGrid = SHOW_BASELINE_GRID,
    showFlowConnections = SHOW_FLOW_CONNECTIONS,
    showElementInfo = True,
    BOX_COLOR = BOX_COLOR, # Overwrite default color for column squares.
    # Text measures
    leading = baselineGrid, # Set default dependent on scalable with unit size.
    rLeading = 0, # In this example, leading is hard-coded as points. Not relative to the point size.
    fontSize = round(1.3*U) # Arbitrary scalable fontSize -- unit relation.
)
RS['language'] = 'en' # Make English hyphenation default.

ROOT_PATH = pagebot.getRootPath()
EXPORT_PATH = '_export/TextElements.pdf' # Export in folder that does not commit un Git. Force to export PDF.

MAIN_FLOW = 'main' # Element id of the text box on pages the hold the main text flow.

# Common tracking presets for typographic style.
# Note that – different from CSS – using Python as descriptor language, it is easy to make calculating relations.
H1_TRACK = H2_TRACK = 0.015 # 1/1000 of fontSize, multiplier factor.
H3_TRACK = 0.030 # Tracking as relative factor to font size.
P_TRACK = 0.030

# -----------------------------------------------------------------         
# PageBot is supporting the use of OpenType Variable fonts. As the OS may not fully support this yet,
# we'll calculate instances at certain locations and store them as fixed font files.
# Note that the example fonts supplied with PageBot subsets, to be used inside PageBot examples only,
# under MIT license. Full license to the complete fonts is available on the typenetwork.com site.
 
# -----------------------------------------------------------------         
def makeDocument(rs):
    u"""Demo page composer."""

    # Set some values of the default template (as already generated by the document).
    # Make squential unique names for the flow boxes inside the templates
    flowId0 = MAIN_FLOW+'0' 
    flowId1 = MAIN_FLOW+'1'
    flowId2 = MAIN_FLOW+'2'
    headlineId = 'headLine'
    
    # Template 2
    template = Template(style=rs) # Create second template. This is for the main pages.
    # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True.
    # The grid is just a regular element, like all others on the page. Same parameters apply.
    template.grid() 
    # Show baseline grid if rs.showBaselineGrid is True.
    # The baseline grid is just a regular element, like all others on the page. Same parameters apply.
    template.baselineGrid()
    # Add image containers to the page, that images + captions, within the defined space.
    template.cContainer(4, 0, 2, 3)  # Empty image element, cx, cy, cw, ch
    template.cContainer(0, 5, 2, 3)
    template.cContainer(2, 2, 2, 2)
    template.cContainer(4, 6, 2, 2)
    
    # In this simple example page, we won't have the headline run in the galley of the main text.
    # Create separate text box here to accommodate the headline.
    template.cTextBox('', 0, 0, 4, 2, eId=headlineId, fill=BOX_COLOR)

    # Make linked text box elemnents, where position and size is defined by columns.
    template.cTextBox('', 0, 2, 2, 3, eId=flowId0, nextBox=flowId1, nextPage=0, fill=BOX_COLOR)
    template.cTextBox('', 2, 4, 2, 4, eId=flowId1, nextBox=flowId2, nextPage=0, fill=BOX_COLOR)
    # Final column flow on the page does not link to next page. We want this demo one page only.
    template.cTextBox('', 4, 3, 2, 3, eId=flowId2, fill=BOX_COLOR)
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rs, pages=2, template=template) 
 
    # Change template of page 1
    onePage = doc[1]
        
    # Create main Galley for this page, for pasting the sequence of elements.    
    g = Galley() 
    t = Typesetter(g)                
    """
    blurbNames = (('h1', 'news_headline'), ('h2', 'article_ankeiler'))
    t.typesetFilibuster(blurbNames)

    c = Composer(doc)
    c.compose(g, onePage, headlineId)

    g = Galley() 
    t = Typesetter(doc, g)                
    blurbNames = (('h3', 'article_ankeiler'), ('h2', 'article_summary'), ('p', 'article'))
    t.typesetFilibuster(blurbNames)
    
    # Fill the main flow of text boxes with the ML-->XHTML formatted text. 
    c = Composer(doc)
    c.compose(g, onePage, flowId0)
    """
    return doc
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 


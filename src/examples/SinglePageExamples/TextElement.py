# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     TextElement.py
#
#     This script generates a fake article on a single page, using Filibuster text,
#     automatic layout template, Galley, Typesetter and Composer classes.
#
import pagebot # Import to know the path of non-Python resources.
from pagebot import getFormattedString, textBoxBaseLines

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT_ALIGN, A4
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
# Page and Template instances are holding all elements of a page together.
from pagebot.elements.page import Page, Template
# The Typesetter instance takes content from a file (typically MarkDown text) and converts that 
# into Galley list of elements.
from pagebot.typesetter import Typesetter
# The Composer instance distributes the Galley content of the pages, according to the defined Templates.
from pagebot.composer import Composer
# Elements that can placed on pages and templates.
from pagebot.elements.galley import Galley
from pagebot.elements.rect import Rect
# Get functions to create instances style from Variation fonts.
from pagebot.fonttoolbox.variationbuilder import getVariationFont, generateInstance

# For clarity, most of the OnePage.py example documenet is setup as a sequential excecution of
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

W, H = A4
# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot values are filled by their default values. The root style is kept in RS
# as reference to for all ininitialzaiton of elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

CW = 11*10
CH = 6*10
cc = None
def callback(sender):
    print sender
    
Variable([
    # create a variable called 'w'
    # and the related ui is a Slider.
    dict(name="CW", ui="Slider"),
    # create a variable called 'h'
    # and the related ui is a Slider.
    # create a variable called 'useColor'
    # and the related ui is a CheckBox.
    dict(name="CH", ui="Slider"),
    dict(name="cc", ui="Button", callback=callback),
    # create a variable called 'c'
    # and the related ui is a ColorWell.
    ], globals())

RS = getRootStyle(
    u = U, # Page base unit
    # Basic layout measures altering the default rooT STYLE.
    w = W, # On root level the "w" is the page width 210mm, international generic fit.
    h = H, # Page height 11", international generic fit.
    ml = 7*U, # Margin left between left side of the page and grid.
    mt = 7*U, # Margin top between page top and grid.
    baselineGrid = baselineGrid,
    g = U, # Generic gutter, identical to the page unit.
    # Column width. Uneven means possible split in 5+1+5 or even 2+1+2 +1+ 2+1+2
    # 11 is a the best in that respect for column calculation.
    cw = CW/6*U, 
    ch = CH/6*baselineGrid - U, # Approx. square and fitting with baseline.
    listIndent = listIndent, # Indent for bullet lists
    listTabs = [(listIndent, LEFT_ALIGN)], # Match bullet+tab with left indent.
    # Display option during design and testing. Copy them in the root style for elements to check on.
    showGrid = SHOW_GRID,
    showGridColumns = SHOW_GRID_COLUMNS,
    showBaselineGrid = SHOW_BASELINE_GRID,
    showFlowConnections = SHOW_FLOW_CONNECTIONS,
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
# PageBot is supporting the use of OpenType Variation fonts. As the OS may not fully support this yet,
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
    template.grid(style=rs) 
    # Show baseline grid if rs.showBaselineGrid is True.
    # The baseline grid is just a regular element, like all others on the page. Same parameters apply.
    template.baselineGrid(style=rs)
    # Add image containers to the page, that images + captions, within the defined space.
    template.cContainer(4, 0, 2, 3, rs)  # Empty image element, cx, cy, cw, ch
    template.cContainer(0, 5, 2, 3, rs)
    template.cContainer(2, 2, 2, 2, rs)
    template.cContainer(4, 6, 2, 2, rs)
    
    # In this simple example page, we won't have the headline run in the galley of the main text.
    # Create separate text box here to accommodate the headline.
    template.cTextBox('', 0, -0.2, 4, 2+0.2, rs, headlineId, fill=BOX_COLOR)

    # Make linked text box elemnents, where position and size is defined by columns.
    template.cTextBox('', 0, 2, 2, 3, rs, flowId0, nextBox=flowId1, nextPage=0, fill=BOX_COLOR)
    template.cTextBox('', 2, 4, 2, 4, rs, flowId1, nextBox=flowId2, nextPage=0, fill=BOX_COLOR)
    # Final column flow on the page does not link to next page. We want this demo one page only.
    template.cTextBox('', 4, 3, 2, 3, rs, flowId2, fill=BOX_COLOR)
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rs, pages=2, template=template) 
 
    # Cache some values from the root style that we need multiple time to create the tag styles.
    fontSize = rs['fontSize']
    leading = rs['leading']
    rLeading = rs['rLeading']
    listIndent = rs['listIndent']
    language = rs['language']
    h1Size = 4*fontSize
    h2Size = 3*fontSize
    
    # Add styles for whole document and text flows.  
    # Note that some values are defined here for clarity, even if their default root values
    # are the same.             
    """
    doc.newStyle(name='chapter', font=BOOK)    
    doc.newStyle(name='title', fontSize=3*fontSize, font=BOLD)
    doc.newStyle(name='subtitle', fontSize=2*fontSize, font=BOOK_ITALIC)
    doc.newStyle(name='author', fontSize=2*fontSize, font=BOOK, fill=(1, 0, 0))
    doc.newStyle(name='h1', fontSize=h1Size, font=SEMIBOLD, fill=(1, 0, 0),
        leading=1.1*h1Size, tracking=H1_TRACK, postfix='\n')
    doc.newStyle(name='h2', fontSize=h2Size, font=BOOK, fill=(1, 0, 0),
        leading=1.1*h2Size, rLeading=0, tracking=H2_TRACK, postfix='\n')
    doc.newStyle(name='h3', fontSize=1.2*fontSize, font=MEDIUM, fill=0, 
        leading=1.4*fontSize, rLeading=0, rNeedsBelow=2*rLeading, tracking=H3_TRACK,
        postfix='\n')
    
    # Spaced paragraphs.
    doc.newStyle(name='p', fontSize=fontSize, font=BOOK, fill=0.1, prefix='', postfix='\n',
        rTracking=P_TRACK, leading=14, rLeading=0, align=LEFT_ALIGN, hyphenation=True)
    doc.newStyle(name='b', font=SEMIBOLD)
    doc.newStyle(name='em', font=BOOK_ITALIC)
    doc.newStyle(name='hr', stroke=(1, 0, 0), strokeWidth=4)
    doc.newStyle(name='br', postfix='\n') # Simplest way to make <br/> be newline
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
    """
    # Change template of page 1
    onePage = doc[1]
        
    # Create main Galley for this page, for pasting the sequence of elements.    
    g = Galley() 
    t = Typesetter(doc, g)                
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
    
    return doc
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 


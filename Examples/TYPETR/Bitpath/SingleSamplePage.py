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
#     BitcountReference.py
#
#     This script the PDF document with Bitcount refernce information.
#
from drawBot import FormattedString

import pagebot
from pagebot import findMarkers, textBoxBaseLines, newFS
from pagebot.style import getRootStyle, LEFT, NO_COLOR
from pagebot.document import Document
from pagebot.elements import Page, Template, Galley
from pagebot.composer import Composer
from pagebot.typesetter import Typesetter
from pagebot.style import A4
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot.contributions.filibuster.blurb import blurb

DEBUG = False

SHOW_GRID = True
SHOW_GRID_COLUMNS = True
SHOW_BASELINE_GRID = DEBUG
SHOW_FLOW_CONNECTIONS = DEBUG

if SHOW_GRID:
    BOX_COLOR = (0.8, 0.8, 0.8, 0.4)
else:
    BOX_COLOR = None

# Unpack A4 standard A4 size.
W, H = A4
H = W # For now.
   
# Get the default root style and overwrite values for this document.
U = 7
baselineGrid = 2*U
listIndent = 1.5*U

RS = getRootStyle(
    u = U, # Page base unit
    # Basic layout measures altering the default rooT STYLE.
    w = W, # Om root level the "w" is the page width 210mm, international generic fit.
    h = H, # 842 = A4 height. Other example: page height 11", international generic fit.
    ml = 8*U, # Margin left rs.mt = 7*U # Margin top
    baselineGrid = 14,#baselineGrid,
    gw = 2*U, # Generic gutter, equal for width and height
    gh = 2*U,
    # Column width. Uneven means possible split in 5+1+5 or even 2+1+2 +1+ 2+1+2
    # Uneven a the best in that respect for column calculation,
    # as it is possible to make micro columsn with the same gutter.
    cw = 8*U, 
    ch = 5*baselineGrid - U, # Approx. square and fitting with baseline.
    listIndent = listIndent, # Indent for bullet lists
    listTabs = [(listIndent, LEFT)], # Match bullet+tab with left indent.
    # Display option during design and testing
    showGrid = SHOW_GRID,
    showGridColumns = SHOW_GRID_COLUMNS,
    showBaselineGrid = SHOW_BASELINE_GRID,
    showFlowConnections = SHOW_FLOW_CONNECTIONS,
    BOX_COLOR = BOX_COLOR,
    # Text measures
    leading = 14,
    rLeading = 0,
    rTracking = 0,
    fontSize = 9
)
FS = newFS(FormattedString(''), style=RS)
# LANGUAGE-SWITCH Language settings
RS['language'] = 'en'

Monospaced = False
Headline_Tracking = False
Body_Tracking = False
Single = False
Ligatures = False # [liga]
Slashed_Zero = True # [zero]
Fraction = True # [frac]
Italic = False
Italic_Shapes = False # [ss08]
Condensed = False # [ss07] Excludes Double if selected
Smallcaps = False # [smcp]
Caps_As_Smallcaps = False # [c2cs]
Extended_Ascenders = False # [ss01]
Extended_Capitals = False # [ss02]
Extended_Descenders = False # [ss03]
Contrast_Pixel = False # [ss04]
Alternative_g = False # [ss09]
LC_Figures = False # [onum]

EXPORT_PATH = '_export/SingleSamplePage.pdf'

# Tracking presets
H1_TRACK = H2_TRACK = 10 # 1/1000 of fontSize, multiplier factor.
H3_TRACK = 0 # Tracking as relative factor to font size.
P_TRACK = 0

#-----------------------------------------------------------------         
def makeDocument(rs):
    u"""Demo Bitpath Reference composer."""
    mainId = 'mainId'

    features = dict(
        kern = True,
        liga = Ligatures,
        zero = Slashed_Zero,
        frac = Fraction,
        smcp = Smallcaps,
        c2sc = Caps_As_Smallcaps,
        ss08 = Italic_Shapes,
        ss07 = Condensed,
        ss01 = Extended_Ascenders,
        ss02 = Extended_Capitals,
        ss03 = Extended_Descenders,
        ss04 = Contrast_Pixel,
        ss09 = Alternative_g,
        onum = LC_Figures,
    )
    if HeadlineTracking:
        headlineTracking = 0.1
    else:
        headlineTracking = 0
    
    if BodyTracking:
        bodyTracking = 0.1
    else:
        bodyTracking = 0
    
    if Single:
        singleDouble = 'Single'
    else:
        singleDouble = 'Double'
    
    if Monospaced:
        spacing = 'Mono'
    else:
        spacing = 'Prop'

    if Italic:
        italic = 'Italic'
    else:
        italic = ''
        
    spacing = 'Grid'
    singleDouble = 'Double'
    
    BOOK = '%s%s%s-BlackLineRound%s' % (familyName, spacing, singleDouble, italic)
    MEDIUM = '%s%s%s-RegularLineRound%s' % (familyName, spacing, singleDouble, italic)
    BOOK_ITALIC = '%s%s%s-RegularLineRound%s' % (familyName, spacing, singleDouble, italic)
    BOLD = '%s%s%s-RegularLineRound%s' % (familyName, spacing, singleDouble, italic)
    SEMIBOLD = '%s%s%s-RegularLineRound%s' % (familyName, spacing, singleDouble, italic)
     
    # Template 1
    template1 = Template(rs) # Create template of main size. Front page only.
    # Show baseline grid if rs.showBaselineGrid is True
    template1.baselineGrid(rs)
    # Create linked text boxes. Note the "nextPage" to keep on the same page or to next.
    template1.cTextBox(FS, 1, 0, 6, 6, rs, eId=mainId)
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template2
    doc = Document(rs, pages=1, template=template1) 
 
    page = doc[1]
    # Index by element id, answers ([e1, ...], (x, y)) tuple. There can be multiple elements
    # with the same Id, and there can be multiple elements on the same position).
    #page[mainId]
    e = page.getElement(mainId)
    
    fs = newFS(Sample_Text + ' V.T.TeY.Yjy\n', style=dict(font=BOLD, fontSize=32, rTracking=headlineTracking, openTypeFeatures = features))
    e.append(fs)
    fs = newFS(blurb.getBlurb('sports_headline', noTags=True)+'\n', style=dict(font=BOOK, fontSize=32, rTracking=headlineTracking, openTypeFeatures = features))
    e.append(fs)
    fs = newFS(blurb.getBlurb('aerospace_headline', noTags=True)+'\n', style=dict(font=BOOK, fontSize=16, rTracking=headlineTracking, openTypeFeatures = features))
    e.append(fs)
    fs = newFS(blurb.getBlurb('article_content', noTags=True)+'\n', style=dict(font=BOOK, fontSize=12, rTracking=bodyTracking, openTypeFeatures = features))
    e.append(fs)

    return doc

if __name__ == '__main__':
    familyName = 'Bitpath'
    BitcountPaths = getFamilyFontPaths(familyName) 
    for k in BitcountPaths.keys():
        if 'Line' in k:
            print k

    UI = [
        dict(name='Sample_Text', ui='EditText', args=dict(text=u'Typetr')),
        dict(name='Monospaced', ui='CheckBox'),
        dict(name='HeadlineTracking', ui='CheckBox'),
        dict(name='BodyTracking', ui='CheckBox'),
        dict(name='Italic', ui='CheckBox'),
    ]
    UI.append(dict(name='Italic_Shapes', ui='CheckBox')) # [ss08]
    UI.append(dict(name='Single', ui='CheckBox')) # Single/Double
    UI.append(dict(name='Ligatures', ui='CheckBox')) # [ss08]
    UI.append(dict(name='Condensed', ui='CheckBox')) # Used Condensed feaure. Excludes "Double" Bitcount font selection.
    UI.append(dict(name='Slashed_Zero', ui='CheckBox')) # Used Condensed feaure. Excludes "Double" Bitcount font selection.
    UI.append(dict(name='Fraction', ui='CheckBox')) # Fraction 123/456.
    UI.append(dict(name='Smallcaps', ui='CheckBox')) # [smcp]
    UI.append(dict(name='Caps_As_Smallcaps', ui='CheckBox')) # [c2sc].
    UI.append(dict(name='Extended_Ascenders', ui='CheckBox')) # [ss01].
    UI.append(dict(name='Extended_Capitals', ui='CheckBox')) # [ss02].
    UI.append(dict(name='Extended_Descenders', ui='CheckBox')) # [ss03].
    UI.append(dict(name='Contrast_Pixel', ui='CheckBox')) # [ss04].
    UI.append(dict(name='Alternative_g', ui='CheckBox')) # [ss09].
    UI.append(dict(name='LC_Figures', ui='CheckBox')) # [onum].

    Variable(UI, globals())
            
    d = makeDocument(RS)
    d.export(EXPORT_PATH) 


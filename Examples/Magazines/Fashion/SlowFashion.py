# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     SlowFashion.py
#
from __future__ import division

import pagebot
from datetime import datetime # Make date fit today.
from pagebot import newFS, Gradient, Shadow
from pagebot.style import getRootStyle, LEFT, TOP, A4Letter
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.document import Document
from pagebot.composer import Composer
from pagebot.typesetter import Typesetter

from pagebot.fonttoolbox.variablefontbuilder import getVariableFont, Font 
W, H = A4Letter
PADDING = 24

MD_PATH = 'slowFashionStories.md'
EXPORT_PATH = '_export/SlowFashion.pdf'
COVER_IMAGE_PATH1 = 'images/IMG_8914.jpg'

# Set some values of the default template (as already generated by the document).
# Make squential unique names for the flow boxes inside the templates
MAIN_FLOW = 'main' # ELement id of the text box on pages the hold the main text flow.
FLOWID1 = MAIN_FLOW+'1' 
FLOWID2 = MAIN_FLOW+'2'
FLOWID3 = MAIN_FLOW+'3'

ROOT_PATH = pagebot.getRootPath()
FONT_PATH = ROOT_PATH + '/Fonts/fontbureau/AmstelvarAlpha-VF.ttf'
#FONT_PATH = getMasterPath() + 'BitcountGrid-GX.ttf'

f = Font(FONT_PATH)
print f.axes

LIGHT = getVariableFont(FONT_PATH, dict(wght=0.5, wdth=0.6))
print LIGHT.path
LIGHT.save(ROOT_PATH + '/Fonts/_instances/PromiseInstance.otf')

BOOK_LIGHT = getVariableFont(FONT_PATH, dict(wght=1, wdth=1))
BOOK_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.25, wdth=0.8))
BOOK = getVariableFont(FONT_PATH, dict(wght=0.25, wdth=1))
BOOK_ITALIC = getVariableFont(FONT_PATH, dict(wght=0.25, wdth=1))
MEDIUM = getVariableFont(FONT_PATH, dict(wght=0.40, wdth=1))
SEMIBOLD = getVariableFont(FONT_PATH, dict(wght=0.40, wdth=1))
SEMIBOLD_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.40, wdth=0.5))
BOLD = getVariableFont(FONT_PATH, dict(wght=0.70, wdth=1))
BOLD_ITALIC = getVariableFont(FONT_PATH, dict(wght=0.7, wdth=1))

shadow = Shadow(offset=(6, -6), blur=10, color=(0.2, 0.2, 0.2, 0.5))

def makeCoverTemplate(imagePath, w, h):
    bleed = 0
    textColor = 1
    # Cover
    coverTemplate = Template(w=w, h=h, padding=PADDING) # Cover template of the magazine.
    newImage(imagePath, parent=coverTemplate, 
        conditions=[Fit2WidthSides(), Bottom2BottomSide()])
    # Title of the magazine cover.
    #LIGHT = getVariableFont(FONT_PATH, dict(wght=0.7, wdth=0.34))

    coverTitle = newFS('Fashion', 
        style=dict(font=LIGHT.installedName, fontSize=180, shadow=shadow, textFill=textColor, tracking=-3))
    newText(coverTitle, parent=coverTemplate, conditions=[Fit2Width(), Top2TopSide()], shadow=shadow)
    
    # Make actual date in top-right with magazine title. Draw a bit transparant on background photo.
    dt = datetime.now()
    d = dt.strftime("%B %Y")
    fs = newFS(d, style=dict(font=MEDIUM.installedName, fontSize=18, 
        textColor=(1, 1, 1, 0.8), tracking=0.5))
    newText(fs, parent=coverTemplate, conditions=[Float2Top(), Fit2Width()])

    # Titles could come automatic from chapters in the magazine.
    fs = newFS('$6.95',  style=dict(font=BOOK.installedName, fontSize=12, 
        textFill=textColor, tracking=0.5, leading=12 ))
    newText(fs, parent=coverTemplate, conditions=[Float2Top(), Left2Left()])
  
    makeCoverTitles(coverTemplate)
    
    return coverTemplate

def makeCoverTitles(coverTemplate):
    # Titles could come automatic from chapters in the magazine.
    fs = newFS('Skirts &\nScarves', style=dict(font=BOOK_CONDENSED.installedName, 
        fontSize=54, fill=1, tracking=0.5, leading=48))
    newText(fs, parent=coverTemplate, conditions=[Left2Left(), Float2Top()])
    """
    # Titles could come automatic from chapters in the magazine.
    fs = newFS('Ideal style:\n', style=dict(font=MEDIUM.installedName, fontSize=32, 
        fill=1, tracking=0.5, leading=34))
    fs += newFS('The almost nothing', style=dict(font=BOOK.installedName, 
        fontSize=32, fill=1, tracking=0.5, leading=34))
    coverTemplate.text(fs, (22, 420))
        
    # Titles could come automatic from chapters in the magazine.
    fs = FormattedString('Findings\non the island', font=BOOK_LIGHT.installedName, 
        fontSize=60, fill=1, tracking=0.5, leading=52 )
    newText(fs, parent=coverTemplate, style=dict(shadowOffset=(4, -4), shadowBlur=20, 
        shadowFill=(0,0,0,0.6))
      
    # Titles could come automatic from chapters in the magazine.
    c = 1 #(0.2, 0.2, 1, 0.9)
    fs = FormattedString('Exclusive:\n', font=MEDIUM, fontSize=32, fill=c, tracking=0.5,
        lineHeight=34)
    fs += FormattedString('Interview with Pepper+Tom ', font=BOOK, fontSize=32, fill=c, tracking=0.5,
        lineHeight=34)
    coverTemplate.text(fs, (22, 760))
        
    # Titles could come automatic from chapters in the magazine.
    fs = FormattedString('Slow', font=MEDIUM, fontSize=70, fill=(1, 1, 1, 0.15), tracking=0.5,
        lineHeight=52 )
    coverTemplate.text(fs, (95, 65))
    """
    
def makeTemplate1():
    # Template 16
    template = Template() # Create template of main size. Front page only.
    # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True
    """
    # Create empty image place holders. To be filled by running content on the page.
    template.cContainer(2, -0.7, 5, 4)  # Empty image element, cx, cy, cw, ch
    template.cContainer(0, 5, 2, 3)
    # Create linked text boxes. Note the "nextPage" to keep on the same page or to next.
    template.cTextBox('', 0, 0, 2, 5, eId=FLOWID1, nextBox=FLOWID2, nextPage=0, fill=BOX_COLOR)
    template.cTextBox('', 2, 3, 2, 5, eId=FLOWID2, nextBox=FLOWID3, nextPage=0, fill=BOX_COLOR)
    template.cTextBox('', 4, 3, 2, 5, eId=FLOWID3, nextBox=FLOWID1, nextPage=1, fill=BOX_COLOR)
    # Create page number box. Pattern pageNumberMarker is replaced by actual page number.
    template.text(rs['pageIdMarker'], (template.css('w',0)-template.css('mr',0), 20), style=rs, font=BOOK, fontSize=12, fill=BOX_COLOR, align='right')
    """
    return template
 
def makeTemplate2():
    # Template 2
    template = Template() # Create second template. This is for the main pages.
    # Show grid columns and margins if rootStyle.showGrid or rootStyle.showGridColumns are True
    """
    template.cContainer(4, 0, 2, 3)  # Empty image element, cx, cy, cw, ch
    template.cContainer(0, 5, 2, 3)
    template.cContainer(2, 2, 2, 2)
    template.cContainer(2, 0, 2, 2)
    template.cContainer(4, 6, 2, 2)
    template.cTextBox('', 0, 0, 2, 5, eId=FLOWID1, nextBox=FLOWID2, nextPage=0, fill=BOX_COLOR)
    template.cTextBox('', 2, 4, 2, 4, eId=FLOWID2, nextBox=FLOWID3, nextPage=0, fill=BOX_COLOR)
    template.cTextBox('', 4, 3, 2, 3, eId=FLOWID3, nextBox=FLOWID1, nextPage=1, fill=BOX_COLOR)
    # Create page number box. Pattern pageNumberMarker is replaced by actual page number.
    template.text(rs['pageIdMarker'], (template.css('w',0) - template.css('mr',0), 20), style=rs, font=BOOK, fontSize=12, fill=BOX_COLOR, align='right')
    """
    return template
           
# -----------------------------------------------------------------         
def makeDocument():
    u"""Demo page composer."""

    coverTemplate1 = makeCoverTemplate(COVER_IMAGE_PATH1, W, H)
    template1 = makeTemplate1() 
    template2 = makeTemplate2()
       
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template2.
    # Oversized document (docW, docH) is defined in the rootStyle.
    doc = Document(title=EXPORT_PATH, w=W, h=H, pages=3, originTop=False,
        template=template1) 
 
    view = doc.getView()
    view.padding = 40
    view.showPagePadding = True
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPagePadding = True
    view.showElementOrigin = True
    view.showElementDimensions = False
    
    # Cache some values from the root style that we need multiple time to create the tag styles.
    """
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
    doc.newStyle(name='h1', fontSize=3.85*fontSize, font=SEMIBOLD_CONDENSED, textFill=(1, 0, 0), 
        leading=2.5*leading, tracking=H1_TRACK, postfix='\n')
    doc.newStyle(name='h2', fontSize=1.5*fontSize, font=SEMIBOLD, textStroke=None,
        fill=(0, 0, 1), leading=1*leading, rLeading=0, tracking=H2_TRACK, 
        prefix='', postfix='\n')
    doc.newStyle(name='h3', fontSize=1.1*fontSize, font=MEDIUM, textFill=(1, 0, 0), textStroke=None,
        leading=leading, rLeading=0, rNeedsBelow=2*rLeading, tracking=H3_TRACK,
        prefix='\n', postfix='\n')
    doc.newStyle(name='h4', fontSize=1.1*fontSize, font=BOOK, textFill=(0, 1, 0), textStroke=None,
        leading=leading, rLeading=0, rNeedsBelow=2*rLeading, tracking=H3_TRACK,
        paragraphTopSpacing=U, paragraphBottomSpacing=U, prefix='\n', postfix='\n')
    
    # Spaced paragraphs.
    doc.newStyle(name='p', fontSize=fontSize, font=BOOK, textFill=0.1, prefix='', postfix='\n',
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
    """
    # Change template of page 1
    page0 = doc[0]
    page0.applyTemplate(coverTemplate1)

    #page2 = doc[1] # Default is template1, as defined in Document creation.
    
    # Show thumbnail of entire paga4 on cover. 
    # TODO: Needs to be masked still.
    # TODO: Scale should not be attribute of style, but part of placement instead.
    #page3.style['scaleX'] = page3.style['scaleY'] = 0.1
    #page1.place(page3, 500, 48)# sx, sy)
    """
    # Create main Galley for this page, for pasting the sequence of elements.    
    g = Galley() 
    t = Typesetter(g)
    t.typesetFile(MD_PATH)
    
    # Fill the main flow of text boxes with the ML-->XHTML formatted text. 
    c = Composer(doc)
    c.compose(g, page2, FLOWID1)
    """
    doc.solve()
    
    return doc

d = makeDocument()
d.export(EXPORT_PATH) 


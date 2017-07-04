#    Take text of 3-4 paragraphs (headline, body text, caption)
#    Make 1-2 formatted strings from that (with newFS)
#    Make 2 rect elements, with a color
#    Organize those 3-4 elements on a responsive page.
  
import pagebot  
from pagebot import newFS
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.style import A5, TOP
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont, Font 

W, H = int(A5[0]), int(A5[1])

MAX_PAGES = 10
ARTICLE_CNT = 10

ROOT_PATH = pagebot.getRootPath()
FONT_PATH = ROOT_PATH + '/Fonts/fontbureau/AmstelvarAlpha-VF.ttf'
#FONT_PATH = getMasterPath() + 'BitcountGrid-GX.ttf'

f = Font(FONT_PATH)
print f.axes

# TODO: Check axis conversions!
h1Font = getVariableFont(FONT_PATH, dict(wght=0.8, wdth=0, opsz=0.5))
h2Font = getVariableFont(FONT_PATH, dict(wght=0.6, wdth=0, opsz=0.5))
h3Font = getVariableFont(FONT_PATH, dict(wght=0.6, wdth=0, opsz=0.5))
pFont = getVariableFont(FONT_PATH, dict(wght=0.5, wdth=0, opsz=0.5))


doc = Document(w=W, h=H, originTop=False, autoPages=1)
doc.newStyle(name='h1', fontSize=30, font=h1Font.installedName, textFill=(1, 0, 0), 
        rLeading=1.3, rParagraphTopSpacing=1.3, hyphenation=True)
doc.newStyle(name='h2', fontSize=22, font=h2Font.installedName, textFill=0, 
        rLeading=1.3, rParagraphTopSpacing=0.8, hyphenation=True)
doc.newStyle(name='h3', fontSize=16, font=h3Font.installedName, textFill=0, rLeading=1.2, rParagraphTopSpacing=0.8, rParagraphBottomSpacing=0.5,
indent=-30)
doc.newStyle(name='p', fontSize=10, font=pFont.installedName, textFill=0, 
        leading=12, rParagraphTopSpacing=0.5)
        
def getExtendedBlurb(doc):
    blurb = Blurb()
    fs = newFS(blurb.getBlurb('news_headline', noTags=True)+'\n', style=doc.styles['h1'])
    for n in range(ARTICLE_CNT):
        fs += newFS(blurb.getBlurb('design_headline', noTags=True)+'\n', style=doc.styles['h2'])
        fs += newFS(blurb.getBlurb('design_headline', noTags=True)+'\n', style=doc.styles['h3'])
        fs += newFS(blurb.getBlurb('article', noTags=True)+'\n', style=doc.styles['p'])
        fs += newFS(blurb.getBlurb('design_headline', noTags=True)+'\n', style=doc.styles['h3'])
        fs += newFS(blurb.getBlurb('article', noTags=True)+'\n', style=doc.styles['p'])
    return fs
    
extendedBlurb = getExtendedBlurb(doc)

view = doc.getView()
view.showPagePadding = False
view.showElementOrigin = False
view.showFlowConnections = False
view.showTextOverflowMarker = False # We manually handle the overflow.

page = doc[0]
page.padding = int(page.h/12), int(page.w/12)
pn = 0

overflowText = extendedBlurb 

for n in range(MAX_PAGES):
    newRect(parent=page, z=10, fill=(0.8, 0.8, 0.8), 
        conditions=[Left2LeftSide(), Bottom2Top(), Fit2TopSide(), Fit2WidthSides()])
    newRect(parent=page, z=10, x=10, y=10, fill=(0.7, 0.7, 0.7, 0.5), conditions=[Left2LeftSide(), 
        Top2Bottom(), Fit2BottomSide(), Fit2WidthSides()])

    cId2 = 'colum2'
    fontSize = 10

    tb = newTextBox(overflowText, name=cId2, parent=page, ml=page.gw, mt=16, mb=16, x=24, y=20, fill=0, fontSize=fontSize,
        w=page.pw*2/3,conditions=[Float2Right(), Float2Top(), Fit2Bottom()]
    )
    #print he.x, he.y 
    page.solve()
    if not tb.isOverflow():
        break
    overflowText = tb.getOverflow()
    
    pn += 1
    doc.newPage()
    # TODO: This should work: get the last page in a doc.
    page = doc[pn]
    page.padding = int(page.h/12), int(page.w/12)
        
    #print he.x, he.y 

doc.export('_export/TextAssignment.pdf')


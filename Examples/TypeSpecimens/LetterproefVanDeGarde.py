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
#     LetterproefVanDeGarde.py
#
#     This scripts generates a look-alike revival type specimen with an interpretation
#     of the "Letterproef Van De Garde" Monotype letterpress type specimen, dated 1967.
#     The full name of the printer is "Koninklijke Drukkerij Van de Garde Zaltbommel"
#     Instead of the range of type faces the printer had, a selection of system fonts
#     is shown instead. If you want to use your own typefaces to show up, there is a little
#     coding exercise. 
#
#     As NL-based hot-metal, the measures in the origal book are augustin, but the layout
#     measures often seem to be whole measures of centimeters.
#     For convenience of calculation augustins are treated as points (font size, etc.)
#     and the other measures are calculated as multiplication factor of MM
#
#     This script is intentionally structures as a linear building of pages, without the
#     use of page functions or templates, in order to illustrate the sequentials building
#     of the content. 
#     As real application it would be more generic to add a second layer of abstractions,
#     that defines the types of pages as templates and uses parameter values and data
#     to make insert the content in the template elements.
#
import copy

import pagebot # Import to know the path of non-Python resources.
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.fonttoolbox.objects.font import findInstalledFonts, getFontByName

from pagebot.toolbox.transformer import int2Color    
from pagebot.style import CENTER, NO_COLOR, TOP, BOTTOM, MIDDLE, INLINE, ONLINE, OUTLINE, RIGHT, LEFT, MM, INCH
# Document is the main instance holding all information about the document together (pages, views, etc.)
from pagebot.document import Document
# Import all element classes that can be placed on a page.
from pagebot.elements import *
# Import all layout condition classes
from pagebot.conditions import *
# Import other than default view class, showing double pages spread
from pagebot.elements.views.spreadview import SpreadView
# Generic function to create new FormattedString, extended version of DrawBot FormattedString() call.
from pagebot import newFS

PageWidth, PageHeight = 180*MM, 247*MM # Original size of Letterproef (type specimen)
PADDING = PageWidth/18 # Padding based on size (= in book layout called margin) of the page.
pt = 22*MM
pb = 36*MM
pl = pr = 16*MM # Although the various types of specimen page have their own margin, this it the overall page padding.
pagePadding = (pt, pr, pb, pl)
G = 12 # Gutter
#SYSTEM_FAMILY_NAMES = ('Verdana',)
#SYSTEM_FAMILY_NAMES = ('Georgia',)
SYSTEM_FAMILY_NAMES = ('Proforma', 'Productus')
MY_FAMILY_NAMES = ('Proforma', 'Productus')

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/LetterproefVanDeGarde.png' 
COVER_IMAGE_PATH = 'images/VanDeGardeOriginalCover.png'

def findFont(styleNames, italic=False):
    u"""Find available fonts and guess closest styles for regular, medium and bold."""
    # Any TypeNetwork TYPETR Productus or Proforma installed in the system?
    # Some hard wired foundry name here. This could be improved. Maybe we can add a public
    # "Meta-info about typefaces somewhere in PageBot, so foundries and designers can add their own
    # data there.
    FAMILY_NAMES = MY_FAMILY_NAMES
    fontNames = findInstalledFonts(FAMILY_NAMES)
    foundryName = 'TN | TYPETR' # TODO: Get from font is available
    if not fontNames: # Not installed, find something else that is expected to exist in OSX:
        foundryName = 'Apple OSX Font'
        FAMILY_NAMES = SYSTEM_FAMILY_NAMES
        for pattern in FAMILY_NAMES:
            fontNames = findInstalledFonts(pattern)
            if fontNames:
                break
    print fontNames
    # Find matching styles. 
    for styleName in styleNames:
        for fontName in fontNames:
            if styleName is None:
                if fontName in FAMILY_NAMES: # Some fonts are named by plain family name for the Regular.
                    return foundryName, fontName
                continue
            if styleName in fontName:
                return foundryName, fontName
    return None, None # Nothing found.

def italicName(fontName):
    if not '-' in fontName:
        return fontName + '-Italic'
    return fontName + 'Italic'
    
def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""
    
    foundryName, bookName = findFont((None, 'Book', 'Regular')) # Find these styles in order.
    _, mediumName = findFont(('Medium', 'Book', 'Regular'))
    mediumName = mediumName or bookName # In case medium weight does not exist.
    _, boldName = findFont(('Bold', 'Medium'))

    bookItalicName = italicName(bookName)
    mediumItalicName = italicName(mediumName)
    boldItalicName = italicName(boldName)

    # Get the fonts, so we can dig in the information.
    bookFont = getFontByName(bookName, install=False)
    mediumFont = getFontByName(mediumName, install=False)
    boldFont = getFontByName(boldName, install=False)
    
    bookItalicFont = getFontByName(bookItalicName, install=False)
    mediumItalicFont = getFontByName(mediumItalicName, install=False)
    boldItalicFont = getFontByName(boldItalicName, install=False)
       
    # Some parameters from the original book
    paperColor = int2Color(0xF4EbC9) # Approximation of paper color of original specimen.
    redColor = int2Color(0xAC1E2B) # Red color used in the original specimen
    
    RedBoxY = 118*MM # Vertical position of the Red Box, on Bodoni chapter.
    columnX = 80*MM # Original 80MM, by we don't adjust, so optically a bit more.
    columnW = 60*MM
    leftPadding = rightPadding = 52*MM # Exception page padding for columns
    
    blurb = Blurb() # BLurb generator
    
    doc = Document(w=PageWidth, h=PageHeight, originTop=False, startPage=1, autoPages=10)
    # Get default view from the document and set the viewing parameters.
    view = SpreadView(parent=doc)
    view.style['fill'] = 1
    # TODO: There is a bug that makes view page size grow, if there are multiple pages and padding > 0
    # TODO: Add optional showing of mid-page line gradient, to suggest bended book pages.
    view.padding = 0 # 20*MM # To show cropmarks and such, make >=20*MM or INCH.
    view.showPageCropMarks = False # Won't show if there is not padding in the view.
    view.showPageRegistrationMarks = False
    view.showPageFrame = True
    view.showPageNameInfo = False
    view.showElementOrigin = False
    view.showElementDimensions = False #ShowDimensions
    view.showElementInfo = False
    view.showTextOverflowMarker = False # Don't show marker in case Filibuster blurb is too long.
 
    labelFont = boldFont
    padding = (3*MM, 3*MM, 3*MM, 3*MM)
    fontNameSize = 16
    aboutSize = 10
    glyphSetSize = 11
    glyphSetLeading = 5*MM
    captionSize = 7
    pageNumberSize = 12
    glyphTracking = 0.2 # Tracking of glyphset samples
    rt = 0.02 # Relative tracking
    capHeight = labelFont.info.capHeight / labelFont.info.unitsPerEm * fontNameSize

    border = dict(line=INLINE, dash=None, stroke=redColor, strokeWidth=1)

    # -----------------------------------------------------------------------------------
    # Cover from image scan.
    pn = 1
    page = doc[pn]   
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    # Add image of cover scan.
    # TODO: Make other positions and scaling work on image element.
    newImage(path=COVER_IMAGE_PATH, parent=page, conditions=[Fit2Sides()])
    page.solve()

    # -----------------------------------------------------------------------------------
    # Empty left page.
    pn += 1
    page = doc[pn]   
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)
                    
    # -----------------------------------------------------------------------------------
    # Full red page with white chapter title.
    pn += 1
    page = doc[pn]   
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    # Fill full page with red color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=redColor)
    
    fs = newFS('BOEKLETTER', style=dict(font=boldName, xTextAlign=RIGHT, textFill=paperColor, fontSize=24, rTracking=0.1))#, xTextAlign=RIGHT))
    newTextBox(fs, parent=page, y=page.h-176*MM, conditions=[Left2Left(), Fit2Right(), Fit2Bottom()])
    page.solve()
        
    # -----------------------------------------------------------------------------------
    # Empty left page.
    pn += 1
    page = doc[pn]   
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)
            
    # -----------------------------------------------------------------------------------
    # Title page of family.
    pn += 1   
    page = doc[pn] # Get the single front page from the document.    
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding

    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)
                
    fs = newFS(labelFont.info.familyName.upper(), style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = textSize(fs)
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(fs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], conditions=[Right2RightSide()], 
        fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    tbName.solve() # Make it go to right side of page.
    
    fs = newFS(foundryName.upper(), style=dict(font=boldName, textFill=0, fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = textSize(fs)
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbFoundry = newTextBox(fs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1],
        fill=None, padding=padding, borders=border)
    tbFoundry.top = page.h-RedBoxY
    tbFoundry.right = tbName.left   
    
    # Make blurb text about design and typography.
    aboutText = blurb.getBlurb('article_summary', noTags=True)
    fs = newFS(aboutText, style=dict(font=bookName, textFill=0, fontSize=aboutSize, tracking=0, rTracking=rt, rLeading=1.3,
        hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbAbout = newTextBox(fs, parent=page, x=columnX, w=columnW, conditions=[Fit2Bottom()])
    tbAbout.top = tbFoundry.bottom - 8*MM
    
    # -----------------------------------------------------------------------------------
    # Page 2 of a family chapter. Glyph overview and 3 columns.
    
    pn += 1
    page = doc[pn]
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding

    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)

    # Glyph set 
    
    caps = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ\n'
    lc = caps.lower()
    figures = u'1234567890\n'
    capAccents = u'ÁÀÄÂÉÈËÊÇÍÌÏÎÓÒÖÔØÚÙÜÛÑ\n'
    lcAccents = capAccents.lower()
    punctuations = u',.;:?![]()-–—“”‘’'
    
    fs = newFS(caps, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
        tracking=0, rTracking=glyphTracking))
    fs += newFS(lc, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
        tracking=0, rTracking=glyphTracking))

    if bookName != bookItalicName:
        fs += newFS(caps, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
            tracking=0, rTracking=glyphTracking))
        fs += newFS(lc, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
            tracking=0, rTracking=glyphTracking))

    fs += newFS(figures, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
        tracking=0, rTracking=glyphTracking))
    if bookName != bookItalicName:
        fs += newFS(figures, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
            tracking=0, rTracking=glyphTracking))

    fs += newFS(capAccents, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
        tracking=0, rTracking=glyphTracking))
    fs += newFS(lcAccents, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
        tracking=0, rTracking=glyphTracking))

    if bookName != bookItalicName:
        fs += newFS(capAccents, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
            tracking=0, rTracking=glyphTracking))
        fs += newFS(lcAccents, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
            tracking=0, rTracking=glyphTracking))

    fs += newFS(punctuations, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
        tracking=0, rTracking=glyphTracking))
    if bookName != bookItalicName:
        fs += newFS(punctuations + '\n', style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, leading=glyphSetLeading,
            tracking=0, rTracking=glyphTracking))
    else:
        fs += '\n'
        
    if bookName != boldName:
        fs += newFS(caps+lc+figures+capAccents+lcAccents+punctuations, style=dict(font=boldName, textFill=0, 
            fontSize=glyphSetSize, leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))

    tbGlyphSet = newTextBox(fs, parent=page, w=112*MM, x=leftPadding, conditions=[Top2Top()]) 

    fs = newFS(labelFont.info.familyName.upper(), style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = textSize(fs)
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(fs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], conditions=[Left2LeftSide()], 
        fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    tbName.solve() # Make it go to right side of page.

    fs = newFS(foundryName.upper(), style=dict(font=boldName, textFill=0, fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = textSize(fs)
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbFoundry = newTextBox(fs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1],
        fill=None, padding=padding, borders=border)
    tbFoundry.top = page.h-RedBoxY
    tbFoundry.left = tbName.right   

    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=6.5, tracking=0, rTracking=rt, leading=6.5,
        hyphenation='en'))
    # TODO: Last line of text blocks in original is bold.
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbSpec6 = newTextBox(fs, parent=page, x=leftPadding, w=50*MM, h=30*MM)
    tbSpec6.top = tbFoundry.bottom - 8*MM

    fs = newFS('6 1/2 set\nop 6 pt gegoten (links)', style=dict(font=bookName, fontSize=captionSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=0.05, leading=8, openTypeFeatures=dict(frac=True)))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbCaption6 = newTextBox(fs, parent=page, x=page.pl, w=leftPadding - page.pl - 3*MM, h=30*MM)
    tbCaption6.top = tbSpec6.top
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=6.5, tracking=0, rTracking=rt, leading=7,
        hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbSpec7 = newTextBox(fs, parent=page, x=leftPadding, w=50*MM, h=35*MM)
    tbSpec7.top = tbSpec6.bottom - 5*MM

    fs = newFS('op 7 pt gegoten (links)', style=dict(font=bookName, fontSize=captionSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=0.05, leading=8))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbCaption7 = newTextBox(fs, parent=page, x=page.pl, w=leftPadding - page.pl - 3*MM, h=30*MM)
    tbCaption7.top = tbSpec7.top # TODO: Align with first baseline, instead of box top.
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=6.5, tracking=0, rTracking=rt, leading=8,
        hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbSpec8 = newTextBox(fs, parent=page, h=tbSpec6.top - tbSpec7.bottom)
    tbSpec8.top = tbSpec6.top
    tbSpec8.left = tbSpec6.right + 5*MM
    tbSpec8.w = page.w - page.pr - tbSpec8.left

    fs = newFS('op 8 pt gegoten (rechts)', style=dict(font=bookName, fontSize=captionSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=0.05, leading=8))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbCaption8 = newTextBox(fs, parent=page, x=page.pl, w=leftPadding - page.pl - 3*MM)
    tbCaption8.bottom = tbSpec8.bottom # TODO: Align with the position of the lowest base line.
    
    # TODO: Calculate the right amount
    fs = newFS('Corps 6 – per 100 aug.: romein 417, cursief 444, vet 426 letters', 
        style=dict(font=bookName, fontSize=captionSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=rt, leading=8))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbCaptionTotal = newTextBox(fs, parent=page, x=page.pl, w=page.w - page.pl - page.pr)
    tbCaptionTotal.top = tbSpec8.bottom - MM
    
    # Page number
    fs = newFS(`pn`, 
        style=dict(font=bookName, fontSize=pageNumberSize, 
        textFill=redColor, xTextAlign=LEFT, rTracking=rt, leading=8))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbPageNumber = newTextBox(fs, parent=page, x=leftPadding, w=10*MM)
    tbPageNumber.bottom = 20*MM
            
    # -----------------------------------------------------------------------------------
    # Page 3, 3 columns.
    
    pn += 1
    page = doc[pn]
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
            
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)

    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=8.5, tracking=0, rTracking=rt, leading=8,
        hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbText1 = newTextBox(fs, parent=page, h=110*MM, w=50*MM, conditions=[Top2Top(), Left2Left()])
    page.solve()
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=8.5, tracking=0, rTracking=rt, leading=9,
        hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    x = tbText1.right + 5*MM
    tbText2 = newTextBox(fs, parent=page, x=x, y=tbText1.y, h=tbText1.h, w=page.w - x - rightPadding)
    page.solve()
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=8.5, tracking=0, rTracking=rt, leading=10,
        hyphenation='en'))
    x = tbText1.left
    tbText3 = newTextBox(fs, parent=page, x=x, h=64*MM, w=page.w - x - rightPadding, mt=10*MM, conditions=[Float2TopLeft()])
    
    # TODO: Add red captions here.

    # Red label on the left
    fs = newFS(labelFont.info.styleName.upper(), style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = textSize(fs)
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(fs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], conditions=[Right2RightSide()], 
        fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    
    # Page number
    fs = newFS(`pn`, 
        style=dict(font=bookName, fontSize=pageNumberSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=rt, leading=8))
    tbPageNumber = newTextBox(fs, parent=page, x=page.w - rightPadding - 10*MM, w=10*MM)
    tbPageNumber.bottom = 20*MM
                
    # -----------------------------------------------------------------------------------
    # Page 4, 3 columns.
    
    pn += 1
    page = doc[pn]
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
            
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)
    x = leftPadding
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=10.5, tracking=0, rTracking=rt, leading=10,
        hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbText1 = newTextBox(fs, parent=page, x=x, h=55*MM, w=page.w - x - page.pl, conditions=[Top2Top()])
    page.solve()
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=10.5, tracking=0, rTracking=rt, leading=11,
        hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    newTextBox(fs, parent=page, mt=5*MM, x=x, h=60*MM, w=page.w - x - page.pl, conditions=[Float2Top()])
    page.solve()
        
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=10.5, tracking=0, rTracking=rt, leading=12,
        hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    newTextBox(fs, parent=page, mt=5*MM, x=x, h=65*MM, w=page.w - x - page.pl, conditions=[Float2Top()])
    page.solve()
        
    # TODO: Add red captions here.

    # Red label on the right
    fs = newFS('10.5pt', style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = textSize(fs)
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(fs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], conditions=[Left2LeftSide()], 
        fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    
    # Page number, even on left side.
    fs = newFS(`pn`, 
        style=dict(font=bookName, fontSize=pageNumberSize, 
        textFill=redColor, xTextAlign=LEFT, rTracking=rt, leading=8))
    tbPageNumber = newTextBox(fs, parent=page, x=leftPadding, w=10*MM)
    tbPageNumber.bottom = 20*MM
                
    # -----------------------------------------------------------------------------------
    # Page 5, 2 columns.
    
    pn += 1
    page = doc[pn]
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
            
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)

    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=12.5, tracking=0, rTracking=rt, leading=12,
        hyphenation='en'))
    newTextBox(fs, parent=page, x=x, h=64*MM, w=page.w - page.pl - rightPadding, mt=10*MM, conditions=[Top2Top(), Left2Left()])
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    fs = newFS(specText, style=dict(font=bookName, textFill=0, fontSize=12.5, tracking=0, rTracking=rt, leading=13,
        hyphenation='en'))
    newTextBox(fs, parent=page, x=x, h=64*MM, w=page.w - page.pl - rightPadding, mt=10*MM, conditions=[Float2TopLeft()])
    
    # TODO: Add red captions here.

    # Red label on the left
    fs = newFS(labelFont.info.styleName.upper(), style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = textSize(fs)
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(fs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], conditions=[Right2RightSide()], 
        fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    
    # Page number
    fs = newFS(`pn`, 
        style=dict(font=bookName, fontSize=pageNumberSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=rt, leading=8))
    tbPageNumber = newTextBox(fs, parent=page, x=page.w - rightPadding - 10*MM, w=10*MM)
    tbPageNumber.bottom = 20*MM

    # Solve remaining layout and size conditions.
       
    score = doc.solve()
    if score.fails:
        print 'Condition fails', score.fails 
    return doc # Answer the doc for further doing.


d = makeDocument()
d.export(EXPORT_PATH, view=SpreadView.viewId) 


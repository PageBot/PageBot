# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     pagebotdoc.py
#
#     Generic Type Specimen Publiction. Use straight, if the default behavior
#     and templates are hood enough. Inherit the redefine functions otherwise.
#     Example of an inherited publications is FBFamilySpecimen.py
#
from pagebot import newFS

from pagebot.fonttoolbox.objects.family import Family, guessFamilies
from pagebot.fonttoolbox.objects.font import Font, getFontPathOfFont

from pagebot.publications.publication import Publication
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT, NO_COLOR
# Document is the main instance holding all information about the document together 
# (pages, styles, etc.)
from pagebot.document import Document
# Page and Template instances are holding all elements of a page together.
from pagebot.elements.page import Page, Template
      
class PageBotDoc(Publication):
    
    MIN_STYLES = 4 # Don't show, if families have fewer amount of style.
    
    FONT_CLASS = Font
    FAMILY_CLASS = Family
    
    def __init__(self):
        Publication.__init__(self)


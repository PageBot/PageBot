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
#     book.py
#
from pagebot import newFS
from pagebot.publications.publication import Publication
# Page and Template instances are holding all elements of a page together.
from pagebot.elements.pbpage import Template

 
class Book(Publication):
    """Create a default book, with cover, title pages, table of content,
    chapters and index. Layout and content options defined by external parameters.
    Inheriting from Document with the following optional attribures:
    rootStyle=None, styles=None, views=None, name=None, class_=None, title=None, 
    autoPages=1, pageTemplate=None,  originTop=True, startPage=0, w=None, h=None, 
    exportPaths=None, **kwargs)"""

    def initialize(self):
        pass
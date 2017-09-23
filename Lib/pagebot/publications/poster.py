# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     poster.py
#
from pagebot.publications.publication import Publication

class Poster(Publication):
    """Create a default poster, with layout and content options defined by external parameters.
    Inheriting from Document with the following optional attribures:
    rootStyle=None, styles=None, views=None, name=None, class_=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, w=None, h=None, 
    exportPaths=None, **kwargs)"""

    def initialize(self, **kwargs):
        pass
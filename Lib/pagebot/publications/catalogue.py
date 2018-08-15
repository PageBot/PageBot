# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     catalogue.py
#
from pagebot.publications.publication import Publication

class Catalogue(Publication):
    """Create a default catalogue, with layout and content options defined by external parameters.
    Inheriting from Document with the following optional attribures:
    rootStyle=None, styles=None, views=None, name=None, cssClass=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, w=None, h=None, 
    exportPaths=None, **kwargs)"""

    def initialize(self, **kwargs):
        pass

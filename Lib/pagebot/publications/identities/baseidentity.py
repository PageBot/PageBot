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
#     identity.py
#
from pagebot.publications.publication import Publication
from pagebot.constants import *

class BaseIdentity(Publication):
    """Create a default identity, with layout and content options defined by external parameters.
    Inheriting from Document with the following optional attribures:
    rootStyle=None, styles=None, views=None, name=None, cssClass=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, w=None, h=None, 
    exportPaths=None, **kwargs)"""

    # Default paper sizes that are likely to be used for 
    # identities main page size. For a set of identity publications
    # ad number of more page sizes should be selected.
    PAGE_SIZES = {
    	'A2': A2,
        'A3': A3,
        'A4': A4,
        'A5': A5,
        'B4': B4,
        'B5': B5,
        'HalfLetter': HalfLetter,
        'Letter': Letter,
        'Legal': Legal,
        'JuniorLegal': JuniorLegal,
        'Tabloid': Tabloid,
        'Ledger': Ledger,
        'Statement': Statement,
        'Executive': Executive,
        'Folio': Folio,
        'Quarto': Quarto,
        'Size10x14': Size10x14,
        'A4Letter': A4Letter,
        'A4Oversized': A4Oversized,
        'A3Oversized': A3Oversized,
    }
    DEFAULT_PAGE_SIZE_NAME = 'A2'
    DEFAULT_PAGE_SIZE = PAGE_SIZES[DEFAULT_PAGE_SIZE_NAME]

    def initialize(self, **kwargs):
        pass

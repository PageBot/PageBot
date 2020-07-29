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
#     book.py
#
from pagebot.conditions import *
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.constants import *

class InstagramPost(Publication):
    """Create a default instagram post
    """

    DEFAULT_COVERBACKGROUND = (0.3, 0.6, 0.3)

    # Default paper sizes that are likely to be used for
    # books in portrait ratio.
    PAGE_SIZES = {
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
    }
    DEFAULT_PAGE_SIZE_NAME = 'A5'
    DEFAULT_PAGE_SIZE = PAGE_SIZES[DEFAULT_PAGE_SIZE_NAME]

    def addTemplate(self, name, template):
        pass

    def initialize(self, coverBackgroundFill=None, **kwargs):
        """Initialize the generic book templates. """

        # TODO: Solve for left/right templates.

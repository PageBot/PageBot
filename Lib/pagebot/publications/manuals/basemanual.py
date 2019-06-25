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
#     basemanual.py
#
from pagebot.conditions import *
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.constants import *

class BaseManual(Publication):
    """Create a default ad, optimized to export as PDF as well as website.

    Subclassed from Element-->Publication with the following optional attributes:
    rootStyle=None, styles=None, views=None, name=None, cssClass=None, title=None,
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0,
    w=None, h=None, exportPaths=None, **kwargs)

    >>> from pagebot.constants import A4
    >>> br = Brochure()
    >>> br.export('_export/Brochure.pdf')
    """

    DEFAULT_COVERBACKGROUND = (0.3, 0.6, 0.3)
    # Default paper sizes that are likely to be used for magazines in portrait ratio
    PAGE_SIZES = {
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

    def initialize(self, coverBackgroundFill=None, **kwargs):
        u"""Initialize the generic manual templates. """

        padding = self.css('pt'), self.css('pr'), self.css('pb'), self.css('pl')
        w, h = self.w, self.h
        gridY = [(None, 0)] # Default is full height of columns, not horizontal division.

        if coverBackgroundFill is None:
            coverBackgroundFill = self.DEFAULT_COVERBACKGROUND
        """
        if score.fails:
            print('Score', score)
            for failed in score.fails:
                print('\t', failed)
        """
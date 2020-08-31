# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     instagram/__init__.py
#
from pagebot.publications.instagram.basepost import InstagramPost

INSTAGRAM_CLASSES = {
	'InstagramPost': InstagramPost,
}

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

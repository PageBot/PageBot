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
#     Supporting Indesign, xxyxyz.org/indesign
# -----------------------------------------------------------------------------
#
#     idmlstring.py
#

from pagebot.contexts.strings.babelstring import BabelString

class IdmlString(BabelString):
    pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

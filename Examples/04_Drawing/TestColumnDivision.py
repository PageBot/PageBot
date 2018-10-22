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
#     TestColumnDivision.py
#
#     TODO: Adjust example to latest (relative) units additions.
#

import sys
from pagebot import getContext

context = getContext()

class E:
    def css(self, n, v):
        if n == 'gw':
            return 20
        if n == 'cw':
            return 60

def w2cw(w, e):
    gutterW = e.css('gw', 0)
    cw = e.css('cw', 0)
    if cw + gutterW:
        return (w + gutterW) / (cw + gutterW)
    return 0 # Undefined, not info about column width and gutter

def cw2w(cw, e):
    if cw is None:
        w = 0
    else:
        gutterW = e.css('gw', 0)
        w = cw * (e.css('cw', 0) + gutterW) - gutterW  # Overwrite style from here.
    return w


if __name__ == '__main__':
    e = E()

    print(w2cw(60, e))
    print(cw2w(1, e))

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
#     DB_TestColumnDivision.py
#
from __future__ import division

import sys
from pagebot.contexts.platform import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

class E(object):
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
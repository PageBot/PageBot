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
#     svgbuilder.py
#
#     https://svgwrite.readthedocs.io
#

# Allowed to fail, other context types might be supported.
try:
    import svgwrite
    svgBuilder = svgwrite

    # Identifier to make builder hook name. Views will try to call e.build_svg()
    svgBuilder.PB_ID = 'svg'

except ImportError:
    print('Cannot import svgwrite')
    svgBuilder = None

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

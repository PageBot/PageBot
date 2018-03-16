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
#     DB_TestFormattedStrings.py
#
from pagebot.contexts.platform import defaultContext as context

import sys
from pagebot.contexts.platform import defaultContext as context
if not context.isDrawBot:
    sys.exit('Example only runs on DrawBot.')

def run():
    aa = context.newString('Book Cover', style=dict(font='Georgia', fontSize=40))
    print textSize(aa)

    # Create formatted tring.
    bs = context.newString('') # Make BabelString, containing a DrawBot FormattedString
    aa = bs.s
    aa.font('Georgia')
    aa.fontSize(14)
    aa += '123'
    aa.fontSize(40)
    aa.lineHeight(1.3)
    aa += ('Book Cover')
    print textSize(aa)

    aa = context.newString('')
    aa.font('Georgia')
    aa.fontSize(40)
    aa += 'Book Cover'
    print textSize(aa)
    print aa.fontAscender()
    print aa.fontDescender()
    print aa.fontAscender() - aa.fontDescender()

    context.stroke(0)
    context.fill(None)
    context.rect(100, 100, 200, 200)
    context.text(aa, (100, 100))

if __name__ == '__main__':
    bs = context.newString('Book Cover', style=dict(font='Georgia', fontSize=40))
    print context.textSize(bs)
    run()


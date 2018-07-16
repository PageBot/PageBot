# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
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
#     DB_TestFormattedStrings.py
#
import sys
from pagebot.contexts.platform import getContext
from pagebot.toolbox.units import pt
context = getContext()

if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

def run():
    aa = context.newString('Book Cover', style=dict(font='Georgia', fontSize=pt(40)))
    print(context.textSize(aa))

    # Make BabelString,
    # Create formatted string.
    bs = context.newString('')

    # Contains a DrawBot FormattedString.
    aa = bs.s
    print(type(aa))
    aa.font('Georgia')
    aa.fontSize(14)
    aa += 'bla'
    #aa += '123'

    '''
    aa.fontSize(40)
    aa.lineHeight(1.3)
    aa += ('Book Cover')
    print(textSize(aa))

    aa = context.newString('')
    aa.font('Georgia')
    aa.fontSize(40)
    aa += 'Book Cover'
    print(textSize(aa))
    print(aa.fontAscender())
    print(aa.fontDescender())
    print(aa.fontAscender() - aa.fontDescender())

    context.stroke(0)
    context.fill(None)
    context.rect(100, 100, 200, 200)
    context.text(aa, (100, 100))
    '''

if __name__ == '__main__':
    bs = context.newString('Book Cover', style=dict(font='Georgia', fontSize=pt(40)))
    #print(context.textSize(bs))
    run()
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
from pagebot.toolbox.color import blackColor, noColor
context = getContext()

if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

def run():
    # Make BabelString,
    bs = context.newString('Book Cover', style=dict(font='Georgia', fontSize=pt(50)))
    print('Text size book cover: (%f, %f)' % context.textSize(bs))

    # Empty string.
    bs = context.newString('')

    # Contains a DrawBot FormattedString.
    aa = bs.s
    aa.font('Georgia')
    aa.fontSize(14)
    aa += 'bla'
    aa += '123'
    aa.fontSize(40)
    aa.lineHeight(1.3)
    aa += ('Book Cover')
    print('Text size book cover: (%f, %f)' % textSize(aa))
    
    #aa = context.newString('bla')
    #aa.font('Georgia')
    #aa.fontSize(40)
    #aa += 'Book Cover'
    #print(context.textSize(aa))
    
    print('Ascender: %f' % aa.fontAscender())
    print('Descender: %f' % aa.fontDescender())
    print('Difference: %f' % (aa.fontAscender() - aa.fontDescender()))

    context.stroke(blackColor)
    context.fill(noColor)
    context.rect(pt(100), pt(100), pt(200), pt(200))
    print(aa)
    context.fill(blackColor)
    context.fontSize(pt(80))
    context.text('bla', (100, 100))
    
    # FIXME
    context.text(bs, (100, 100))

if __name__ == '__main__':
    run()
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
#     DB_TestFormattedStrings.py
#
import sys
from pagebot import getContext
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import blackColor, noColor, color

context = getContext()

def run():
    # Make BabelString,
    bs = context.newString('Book Cover', style=dict(font='Georgia', fontSize=pt(50)))
    print('Text size book cover: (%f, %f)' % context.textSize(bs))

    # Empty string.
    bs = context.newString('')

    # Contains a DrawBot FormattedString.
    aa = bs.s

    print(type(aa))
    aa.append("123", font="Helvetica", fontSize=100, fill=color(1, 0, 0))
    aa.fontSize(80)
    aa.append("Book Cover", font="Georgia", fill=color(0, 1, 0))
    print(aa)
    print('Text size: (%f, %f)' % textSize(aa))

    print('Ascender: %f' % aa.fontAscender())
    print('Descender: %f' % aa.fontDescender())
    print('Difference: %f' % (aa.fontAscender() - aa.fontDescender()))

    context.stroke(blackColor)
    context.fill(noColor)
    w, h = textSize(aa)
    context.rect(pt(100), pt(100), pt(w), pt(h))
    context.fill(blackColor)
    context.fontSize(pt(80))
    context.text(bs, (100, 100))

if __name__ == '__main__':
    run()

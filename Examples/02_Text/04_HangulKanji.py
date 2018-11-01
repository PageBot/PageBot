#!/usr/bin/evn python
# encoding: utf-8
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
#     HangulKanji.py

from pagebot import getContext
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import color

context = getContext()
FontSize = 30
W, H = 1000, 1000

def run():
    s = """글자가 일상이 된다 산돌커뮤니케이션 ABCD123 Latin すべての文化集団は，独自の言語，文字，書記システムを持つ．それゆえ，個々の書記システムをサイバースペースに移転することは. ABCD123 Latin included"""
    context.newPage(pt(W), pt(H))
    fsr = context.newString(s, style=dict(font='Verdana', fontSize=FontSize))
    fsb = context.newString(s, style=dict(font='Verdana', fontSize=FontSize))
    fsbRed = context.newString(s, style=dict(font='Verdana',
                                       fill=color(1, 0, 0),
                                       fontSize=FontSize))

    context.textBox(fsr, (100, 600, 820, 350))
    context.textBox(fsb, (100, 300, 820, 350))
    context.textBox(fsbRed, (100, 0, 820, 350))
    context.textBox(fsr, (100, 0, 820, 350))

if __name__ == '__main__':
    context.Variable([
        #dict(name='ElementOrigin', ui='CheckBox',
        #     args=dict(value=False)),
        dict(name='FontSize', ui='Slider',
             args=dict(minValue=30, value=50, maxValue=120)),
    ], globals())

    run()
    context.saveImage('_export/TestKanjiFormattedString.pdf')

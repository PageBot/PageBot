# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     TestKanjiFormattedString.py

FontSize = 30
W, H = 1000, 1000
def run():
    s = u"""글자가 일상이 된다 산돌커뮤니케이션 ABCD123 Latin すべての文化集団は，独自の言語，文字，書記システムを持つ．それゆえ，個々の書記システムをサイバースペースに移転することは. ABCD123 Latin included"""
    newPage(W, H)
    fsr = FormattedString(s, font='Generic-Regular', fontSize=FontSize)
    fsb = FormattedString(s, font='Generic-Regular_Bold', fontSize=FontSize)
    fsbRed = FormattedString(s, font='Generic-Regular_Bold', fill=(1, 0, 0), fontSize=FontSize)
    textBox(fsr, (100, 600, 820, 350))
    textBox(fsb, (100, 300, 820, 350))

    textBox(fsbRed, (100, 0, 820, 350))
    textBox(fsr, (100, 0, 820, 350))
          
if __name__ == '__main__':    

    Variable([
        #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
        dict(name='FontSize', ui='Slider', args=dict(minValue=30, value=50, maxValue=120)),
    ], globals())

    run()
    saveImage('_export/TestKanjiFormattedString.pdf')
    #saveImage('TestKanjiFormattedString.pdf')


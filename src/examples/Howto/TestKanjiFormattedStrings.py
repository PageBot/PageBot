# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     TestKanjiFormattedString.py

def run():
    s = u"""すべての文化集団は，独自の言語，文字，書記システムを持つ．それゆえ，個々の書記システムをサイバースペースに移転することは，文化的資産の継承という意味で，情報通信技術にとって非常に重要な責務といえよう．ABCD123 Latin included"""
    fsr = FormattedString(s, font='F5MultiLanguageFontVar-Regular', fontSize=40)
    fsb = FormattedString(s, font='F5MultiLanguageFontVar-Regular_Bold', fontSize=40)
    fsbRed = FormattedString(s, font='F5MultiLanguageFontVar-Regular_Bold', fill=(1, 0, 0), fontSize=40)
    textBox(fsr, (100, 600, 820, 350))
    textBox(fsb, (100, 300, 820, 350))

    textBox(fsbRed, (100, 0, 820, 350))
    textBox(fsr, (100, 0, 820, 350))

      
if __name__ == '__main__':    
    run()
    saveImage('_export/TestKanjiFormattedString.pdf')


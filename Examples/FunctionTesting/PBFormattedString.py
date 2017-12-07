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
#     PBFormattedString.py
#
#     Can be used to experiment with the DrawBot FormattedString class.
#
from pagebot.builders.drawbotbuilder import drawBotBuilder as b
from pagebot.elements.views.strings import newFsString
if b is None:
    print 'Platform does not support DrawBot.'
else:
    fs = FormattedString('')

    class PBFormattedString(fs.__class__):
        pass
    
    f = PBFormattedString('AAA', font='Verdana', fontSize=300, fill=(1, 0, 0))
    text(f, (100 ,100))


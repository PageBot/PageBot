# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     PBFormattedString.py
#
#     Can be used to experiment with the DrawBot FormattedString class.
#
from drawBot import DummyContext


fs = FormattedString('')

class PBFormattedString(fs.__class__):
    pass
    
f = PBFormattedString('AAA', font='Verdana', fontSize=300, fill=(1, 0, 0))
text(f, (100 ,100))


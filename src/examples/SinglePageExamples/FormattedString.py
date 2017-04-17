# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     FormattedString.py
#
from drawBot import DummyContext

def text(txt, x, y=None):
        """
        Draw a text at a provided position.

        .. showcode:: /../examples/text.py
        """
        if isinstance(txt, (str, unicode)):
            try:
                txt = txt.decode("utf-8")
            except UnicodeEncodeError:
                pass
        if y is None:
            x, y = x
        else:
            warnings.warn("position must a tuple: text('%s', (%s, %s))" % (txt, x, y))
        _dummyContext = DummyContext()
        attrString = _dummyContext.attributedString(txt)
        w, h = attrString.size()
        setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
        path = Quartz.CGPathCreateMutable()
        Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(x, y, w*2, h))
        box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        ctLines = CoreText.CTFrameGetLines(box)
        origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)
        if origins:
            x -= origins[-1][0]
            y -= origins[-1][1]
        textBox(txt, (x, y-h, w*2, h*2))


fs = FormattedString('')

class PBFormattedString(fs.__class__):
    pass
    
f = PBFormattedString('AAA', font='Verdana', fontSize=300, fill=(1, 0, 0))
text(f, (100 ,100))


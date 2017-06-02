fs = FormattedString()
fs += "b"
fs.lineHeight(74)
fs.font("Times")
fs.fontSize(38)

fs += "hello world "

fs.font("Helvetica")
fs.fontSize(10)
fs.lineHeight(12)
fs += "hi agian " * 10

r = (10, 10, 200, 200)
textBox(fs, r)

fill(None)
stroke(1, 0, 0)
rect(*r)
#####

import CoreText
import Quartz

def textBoxBaseLines(txt, box):
    x, y, w, h = box
    attrString = txt.getNSObject()
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    path = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*box))
    box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    ctLines = CoreText.CTFrameGetLines(box)
    origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)
    return [(x + o.x, y + o.y) for o in origins]
    
positions = textBoxBaseLines(fs, r)

s = 2
for x, y in positions:
    oval(x-s, y-s, s*2, s*2)
    
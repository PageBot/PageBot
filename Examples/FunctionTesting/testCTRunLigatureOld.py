import CoreText
import Quartz

def ctRunThing(fs):
    w, h = textSize(fs)
    box = 0, 0, w, h
    attrString = fs.getNSObject()
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    path = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*box))
    ctBox = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    ctLines = CoreText.CTFrameGetLines(ctBox)
    ctRuns = CoreText.CTLineGetGlyphRuns(ctLines[0])
    stringIndices = CoreText.CTRunGetStringIndicesPtr(ctRuns[0])
    return stringIndices
    
fs1 = FormattedString('Ligature fifl', font='Proforma-Bold', fontSize=100, openTypeFeatures=dict(liga=False))
text(fs1, (100, 300))
print 'fs1:', ctRunThing(fs1)

fs2 = FormattedString('Ligature fifl', font='Proforma-Bold', fontSize=100, openTypeFeatures=dict(liga=True))
text(fs2, (100, 100))
print 'fs2:', ctRunThing(fs2)

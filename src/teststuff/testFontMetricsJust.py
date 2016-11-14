from AppKit import NSFont
from CoreText import CTFontDescriptorCreateWithNameAndSize, CTFontDescriptorCopyAttribute, kCTFontURLAttribute
from fontTools.ttLib import TTFont


def getFontPathOfFont(fontName):
    font = NSFont.fontWithName_size_(fontName, 25)
    fontRef = CTFontDescriptorCreateWithNameAndSize(font.fontName(), font.pointSize())
    url = CTFontDescriptorCopyAttribute(fontRef, kCTFontURLAttribute)
    return url.path()



size(1500, 800)
#fontName = ""
#fontPath = getFontPathOfFont(fontName)
fontPath = '../fonts/PromisePageBot-GX.ttf'
ttf = TTFont(fontPath)
unitsPerEm = ttf["head"].unitsPerEm
hhea = ttf["hhea"]
os2 = ttf["OS/2"]


font(fontPath)
pointSize = 300
fontSize(pointSize)

s = "Hlxopg"
w, h = textSize(s)
translate((width() - w)/2, 300)

text(s, (0, 0))

fill(None)
stroke(0)
for y in [fontDescender(), 0, fontXHeight(), fontCapHeight(), fontAscender()]:
    line((0, y), (w, y))

stroke(1, 0, 0)
for y in [hhea.descent, 0, hhea.ascent, ]:
    y = y * pointSize / unitsPerEm
    line((-50, y), (-100, y))

stroke(0, 0, 1)
for y in [os2.sTypoDescender, 0, os2.sTypoAscender, os2.sxHeight, os2.sCapHeight]:
    y = y * pointSize / unitsPerEm
    line((-50, y), (0, y))


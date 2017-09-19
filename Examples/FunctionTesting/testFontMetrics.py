import pagebot
from pagebot.fonttoolbox.objects.font import Font

fontPath = pagebot.getFontPath() + "fontbureau/AmstelvarAlpha-VF.ttf"
f = Font(fontPath)
spacer = FormattedString('-----\n ', lineHeight=1, font=f.installedName, fontSize=12)
fontSize(400)

s = FormattedString('Hlxg', font=f.installedName, fill=(1, 0, 0),
    fontSize=300, lineHeight=320, baselineShift=200)

M = 20
fill(0.9)
rect(M, M, 1000-2*M, 800-2*M)


Y = 1000 - M
BASE = f.info.ascender + f.info.descender + f.info.lineGap
print BASE
YS = (BASE,)
for y in YS:
    stroke(0)
    strokeWidth(0.5)
    line((0, y), (1000, y))

fill(0)
stroke(None)
textBox(s, (M, M, 1000-2*M, 400-2*M))


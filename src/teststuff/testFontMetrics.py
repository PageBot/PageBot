import pagebot.fonttoolbox.fontmetrics  
reload(pagebot.fonttoolbox.fontmetrics )
from pagebot.fonttoolbox.fontmetrics import getFontMetrics

fontName = 'PromisePageBot-Bold'
fontPath = '../fonts/PromisePageBot-GX.ttf'
#if not fontName in installedFonts():
installFont(fontPath)
metrics = getFontMetrics(fontPath)
font(fontName)
spacer = FormattedString('-----\n ', lineHeight=1, font=fontName, fontSize=12)
fontSize(400)

s = FormattedString('Hlxg', font=fontName, fill=(1, 0, 0),
    fontSize=300, lineHeight=320, baselineShift=200)
print metrics

M = 20
fill(0.9)
rect(M, M, 1000-2*M, 800-2*M)


Y = 1000 - M
BASE = metrics['ascender'] + metrics['descender'] + metrics['lineGap']
print BASE
YS = (BASE,)
for y in YS:
    stroke(0)
    strokeWidth(0.5)
    line((0, y), (1000, y))

fill(0)
stroke(None)
textBox(s, (M, M, 1000-2*M, 800-2*M))


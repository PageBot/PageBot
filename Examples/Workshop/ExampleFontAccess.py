import pagebot
from pagebot.fonttoolbox.objects.font import Font

ROOT_PATH = pagebot.getRootPath()
FONT_PATH = ROOT_PATH + '/Fonts/_private/PromisePageBot-GX.ttf'
#FONT_PATH = getMasterPath() + 'BitcountGrid-GX.ttf'

FONT_PATH = ROOT_PATH + '/Fonts/fontbureau/AmstelvarAlpha-VF.ttf'

f = Font(FONT_PATH)
print f.axes

print f.info.weightClass, f.info.unitsPerEm

print f.ttFont['fvar'].axes

g = f.keys()
g = f['a']
print g.name, g.width


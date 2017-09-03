#for fontName in installedFonts():
#    if 'Skia' in fontName:
#        print fontName

from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont, drawGlyphPath, getVarLocation

f = Font('/Library/Fonts/Skia.ttf')

wghtMin, wghtDef, wghtMax = f.axes['wght']
wdthMin, wdthDef, wdthMax = f.axes['wdth']

#wghtMin, wghtDef, wghtMax = (-1, 0, 1)
#wdthMin, wdthDef, wdthMax = (-1, 0, 1)

print 'wght', wghtMin, wghtDef, wghtMax
print 'wdth', wdthMin, wdthDef, wdthMax


NORMAL = getVariableFont(f, dict(wght=wghtDef, wdth=wdthDef), styleName='Normal', normalize=False)
LIGHT = getVariableFont(f, dict(wght=wghtMin, wdth=wdthDef), styleName='Light', normalize=False)
BOLD = getVariableFont(f, dict(wght=wghtMax, wdth=wdthDef), styleName='Bold', normalize=False)
COND = getVariableFont(f, dict(wght=wghtDef, wdth=wdthMin), styleName='Cond', normalize=False)
WIDE = getVariableFont(f, dict(wght=wghtDef, wdth=wdthMax), styleName='Wide', normalize=False)


fs = FormattedString('Q', fontSize=250, font=NORMAL.installedName)
text(fs, (350, 400))
fs = FormattedString('Q', fontSize=250, font=LIGHT.installedName)
text(fs, (50, 400))
fs = FormattedString('Q', fontSize=250, font=BOLD.installedName)
text(fs, (650, 400))
fs = FormattedString('Q', fontSize=250, font=COND.installedName)
text(fs, (350, 700))
fs = FormattedString('Q', fontSize=250, font=WIDE.installedName)
text(fs, (350, 100))
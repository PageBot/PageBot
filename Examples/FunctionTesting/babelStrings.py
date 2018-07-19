from pagebot import getRootPath
from pagebot.contexts.platform import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.style import CENTER
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import Color

c = getContext()
W =H = 500

c.newPage(pt(W), pt(H))
            
# Formattted string using append.
print(' * Testing with append')
bs = c.newString('')

# Contains a DrawBot FormattedString.
aa = bs.s
aa.append("123", font="Helvetica", fontSize=100, fill=(1, 0, 1))
print(aa._font)
print(aa._fontSize)
print(aa._fill)
#c.text(bs, (pt(100), pt(100)))
            
# Formatted string without append.
print(' * Testing without append')
bs = c.newString('bla', style=dict(font='Helvetica', fontSize=pt(100), textFill=Color(1, 1, 0)))
print('style: %s' % bs.style)
aa = bs.s
print(aa._font)
print(aa._fontSize)
c.setTextFillColor(aa, Color(1, 1, 0))
print(aa._fill) 
text(aa, (100, 200))
c.text(bs, (pt(100), pt(200)))
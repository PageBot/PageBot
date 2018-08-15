from pagebot import getRootPath
from pagebot.contexts.platform import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.style import CENTER
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import color, Color

c = getContext()
W =H = 500

c.newPage(pt(W), pt(H))
            
# Formattted string using append.
print(' * Testing with append')
bs = c.newString('')

# Contains a DrawBot FormattedString.
aa = bs.s
aa.append("123", font="Helvetica", fontSize=100, fill=color(1, 0, 1).rgb)
print(aa._font)
print(aa._fontSize)
print(aa._fill)
#c.text(bs, (pt(100), pt(100)))
            
# Formatted string without append.
style = dict(font='Helvetica', fontSize=pt(100), textFill=color(1, 1, 0))
print(' * Testing without append')
bs = c.newString('bla', style=style)
print('style: %s' % bs.style)
aa = bs.s
print(aa._font)
print(aa._fontSize)
c.fill(Color(1, 1, 0).rgb)
print(aa._fill) 
text(aa, (100, 200))
c.text(bs, (pt(100), pt(200)))
from pagebot import getRootPath
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.constants import CENTER
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import color, Color

c = getContext()
W =H = 500

def testBabelStrings():
    c.newPage(pt(W), pt(H))
    style = dict(font='Helvetica', fontSize=pt(100), textFill=color(1, 1, 0))

    # Formattted string using append.
    print(' * Testing with append')
    bs = c.newString('bla') # NOTE: style isn't initiated, bug later on.
    print(bs.s._font)
    print(bs.s._fontSize)
    print(bs.s._fill)
    c.text(bs, (10, 10))

    # Contains a DrawBot FormattedString.
    aa = bs.s
    aa.append("123", font="Helvetica", fontSize=100, fill=color(1, 0, 1).rgb)
    print(aa._font)
    print(aa._fontSize)
    print(aa._fill)
    c.text(bs, (pt(20), pt(20))) # FIXME: no output, `bs` not initiated with style arg.

    # Formattted string using append.
    print(' * Testing with append')
    bs = c.newString('bla', style=style)
    print(bs.s._font)
    print(bs.s._fontSize)
    print(bs.s._fill)

    # Contains a DrawBot FormattedString.
    aa = bs.s
    aa.append("123", font="Helvetica", fontSize=100, fill=color(1, 0, 1).rgb)
    print(aa._font)
    print(aa._fontSize)
    print(aa._fill)
    c.text(bs, (pt(200), pt(100)))

    # Formatted string without append.
    print(' * Testing without append')
    bs = c.newString('bla', style=style)
    print('style: %s' % bs.style)
    aa = bs.s
    print(aa._font)
    print(aa._fontSize)
    c.fill(Color(1, 1, 0).rgb)
    print(aa._fill)
    text(aa, (100, 200)) # DrawBot
    c.text(bs, (pt(300), pt(200))) # PageBot

testBabelStrings()

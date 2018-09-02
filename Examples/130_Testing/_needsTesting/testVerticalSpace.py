
h = 'Headline\n'
t = """Waar in de traditie van werken met opmaakprogrammatuur zoals Quark XPress en InDesign altijd een menselijke beslissing de definitieve opmaak van een pagina bepaalt, zijn er steeds meer situaties waarin dat geen optie is. Doordat steeds meer pagina’s worden gegenereerd met inhoud die uit een database komt – of van een online source – en waar de selectie van de informatie direct wordt bepaald door eigenschappen van de lezer, van de pagina’s automatisch worden berekend. """ * 2

M = 20
leading = 24

def drawBaselines():
    stroke(0)
    strokeWidth(0.5)
    fill(None)
    for n in range(M, 1220, leading):
        line((0, n), (1600, n))


def drawBox(fs, x, y, w, h):
    stroke(1, 0, 0)
    fill(None)
    rect(x, y, w, h)
    fill(0)
    stroke(None)
    return textBox(fs, (x, y, w, h))

S1 = 80
FONT = 'Georgia'

fsFont1 = FormattedString(' ', fontSize=S1, font=FONT)
print(S1, 'xHeight', fsFont1.fontXHeight())
print(S1, 'capHeight', fsFont1.fontCapHeight())
print(S1, 'leading', fsFont1.fontLeading())
print(S1, 'lineHeight', fsFont1.fontLineHeight())
print(S1, 'ascender', fsFont1.fontAscender())
print(S1, 'descender', fsFont1.fontDescender())
print(S1, 'ascender + descender', fsFont1.fontAscender() + fsFont1.fontDescender())
print(S1, 'fontSize - fontAscender + fontDescender', S1 - fsFont1.fontAscender() +  fsFont1.fontDescender())
print(S1, 'fontSize - fontLineHeight', S1 - fsFont1.fontLineHeight())

S2 = leading*0.8
"""
fsFont = FormattedString(' ', fontSize=S1, font=FONT)
print(S2, 'xHeight', fsFont.fontXHeight())
print(S2, 'capHeight', fsFont.fontCapHeight())
print(S2, 'leading', fsFont.fontLeading())
print(S2, 'lineHeight', fsFont.fontLineHeight())
print(S2, 'ascender', fsFont.fontAscender())
print(S2, 'descender', fsFont.fontDescender())
print(S2, 'ascender + descender', fsFont.fontAscender() + fsFont.fontDescender())
print(S2, 'fontSize - fontAscender + fontDescender', S2 - fsFont.fontAscender() + fsFont.fontDescender())
print(S2, 'fontSize - fontLineHeight', S2 - fsFont.fontLineHeight())
"""
S3 = 28

def shiftBase(fontSize):
    fs = FormattedString(' ', fontSize=fontSize, font=FONT)
    return (fontSize-fs.fontLineHeight())# % leading

fs = FormattedString(h, font=FONT, fontSize=S1, lineHeight=leading, paragraphTopSpacing=0,
    paragraphBottomSpacing=leading, baselineShift=shiftBase(S1))
print(shiftBase(S1))
print(shiftBase(S2))
print(shiftBase(S3))
fs += FormattedString(t+'\n', font=FONT, fontSize=S2, lineHeight=leading,
    baselineShift=shiftBase(S2))
fs += FormattedString(h, font=FONT, fontSize=S3, lineHeight=2*leading,
    paragraphBottomSpacing=1*leading,
    paragraphTopSpacing=leading, baselineShift=shiftBase(S3))
fs += FormattedString(t, font=FONT, fontSize=S2, lineHeight=leading, baselineShift=shiftBase(S2))
fs += FormattedString(t, font=FONT, fontSize=S2, lineHeight=leading, baselineShift=shiftBase(S2))

fs = drawBox(fs, M, M, 450, 800)
fs = drawBox(fs, M+480, M, 450, 800)
drawBaselines()

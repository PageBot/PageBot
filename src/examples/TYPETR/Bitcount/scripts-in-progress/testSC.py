# set a font
font("Bitcount Mono Single")
# set the font size
fontSize(50)
# draw a string
text("aa1465", (100, 100))
# enable some OpenType features
openTypeFeatures(lnum=True, smcp=True, c2sc=False)
# draw the same string
text("AAaa1465", (100, 200))
# enable some OpenType features
openTypeFeatures(lnum=True, smcp=False, c2sc=True)
# draw the same string
text("AAaa1465", (100, 300))
# enable some OpenType features
openTypeFeatures(lnum=True, smcp=True, c2sc=False)
fs = FormattedString('AAaa1465', fontSize=50, font="Bitcount Mono Single")
# draw the same string
text(fs, (100, 400))
# enable some OpenType features
openTypeFeatures(lnum=True, smcp=False, c2sc=True)
fs = FormattedString('AAaa1465', fontSize=50, font="Bitcount Mono Single")
# draw the same string
text(fs, (100, 500))

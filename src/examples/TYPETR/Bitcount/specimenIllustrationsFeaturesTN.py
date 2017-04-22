#
#    Typetr logo animation
#

bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName:
        print fontName
        bitcountNames.append(fontName)

PIX = 10

"""
Feature | Description | Grid Single | Grid Double | Mono Single | Mono Double | Prop Single | Prop Double
--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- | --- |
**c2sc** | Cap->sc 			| X | X | X | X | X | X
**smcp** | lc->sc 		| X | X | X | X | X | X
**frac** | Fractions 		| - | - | - | - | X | X
**liga** | Ligatures 		| X | X | X | X | X | X
**ss01** | Ascenders+ 		| - | - | X | X | X | X
**ss02** | Capitals+ 		| - | - | X | X | X | X
**ss03** | Descenders+ 		| - | - | X | X | X | X
**ss04** | Contrast px 		| X | - | X | - | X | -
**ss05** | No-Contrast px 	| - | X | - | X | - | X
**ss06** | Forced xHght 	| X | - | - | - | - | -
**ss07** | Condensed 		| X | - | X | - | X | -
**ss08** | Italic 			| X | X | X | X | X | X
**ss09** | Alternative g 	| - | - | X | X | X | X
**onum** | Lowercase figs 	| X | X | X | X | X | X
**zero** | Slash zero 		| X | X | X | X | X | X
"""
  
pixel = 10
labelFont = 'BitcountPropDouble-RegularCircle'

html = ''

features = dict(ss01=True, ss02=True, ss03=True)

for index, fontName in enumerate(sorted(bitcountNames)):
    s1 = u'ABÇDÉFGHI'
    s2 = u'åbçdéfghi'
    W, H = pixel*(len(s1)*6+2), pixel*(3*10+4)
    if 'Prop' in fontName:
        s1 = u'ABÇDÉFGH'
        s2 = u'åbçdéfghij'
    s3 = '(01234@?)'

    newPage(W, H)
    fs1 = FormattedString(s1, font=fontName, fontSize=pixel*10, openTypeFeatures=features)
    text(fs1, (pixel*1.5, 23*pixel))
    fs2 = FormattedString(s2, font=fontName, fontSize=pixel*10, openTypeFeatures=features)
    text(fs2, (pixel*1.5, 13*pixel))
    fs3 = FormattedString(s3, font=fontName, fontSize=pixel*10, openTypeFeatures=features)
    text(fs3, (pixel*1.5, 3*pixel))
    fn = fontName.replace('-', '')
    fn = fn.replace('Bitcount', 'Bitcount ')
    fn = fn.replace('Grid', 'Grid ')
    fn = fn.replace('Mono', 'Mono ')
    fn = fn.replace('Prop', 'Prop ')
    fn = fn.replace('Single', 'Single ')
    fn = fn.replace('Double', 'Double ')
    fn = fn.replace('Light', 'Light ')
    fn = fn.replace('Book', 'Book ')
    fn = fn.replace('Regular', 'Regular ')
    fn = fn.replace('Medium', 'Medium ')
    fn = fn.replace('Bold', 'Bold ')
    fn = fn.replace('Square', 'Square ')
    fn = fn.replace('Circle', 'Circle ')
    fn = fn.replace('Plus', 'Plus ')
    fn = fn.replace('Line', 'Line ')
    fs4 = FormattedString(fn, font=labelFont, fontSize=1.5*pixel,
        tracking=0, openTypeFeatures=features)
    text(fs4, (pixel*1.5, H-2*pixel))
    html += '<figure><img id="BitcountSpecimen%s" src="/ZZZ/uploaded/BitcountSpecimen-%d.png"><caption>...</caption></figure>\n' % (index, index+1)

saveImage('../images/BitcountSpecimenFeatures.png', 1)
f = open('../images/BitcountSpecimen.html', 'w')
f.write(html)
f.close()

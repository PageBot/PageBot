from pagebot import getFormattedString
from pagebot.fonttoolbox.variationbuilder import generateInstance

FONT_PATH = '../fonts/'

FONT_LOCATIONS = {
    #'Promise-BoldCondensed': {"wght": 750, "wdth": 500, },
    #'Promise-LightCondensed': {"wght": 0, "wdth": 500},
    'PromisePageBot-Light': {"wght": 0, "wdth": 1000},
    'PromisePageBot-Book': {"wght": 250, "wdth": 1000},
    'PromisePageBot-Regular': {"wght": 400, "wdth": 1000},    
    'PromisePageBot-Medium': {"wght": 600, "wdth": 1000},    
    'PromisePageBot-Semibold': {"wght": 750, "wdth": 1000},    
    'PromisePageBot-Bold': {"wght": 1000, "wdth": 1000},
}
FONTS = {}
# Install the test V-font
if not 'Promise-Bold' in installedFonts():
    installFont(FONT_PATH + 'PromisePageBot-GX.ttf')
for name, location in FONT_LOCATIONS.items():
    fontName, fontPath = generateInstance(FONT_PATH + 'PromisePageBot-GX.ttf', 
    location, targetDirectory=FONT_PATH + 'instances')
    FONTS[name] = fontName#fontPath # Instead of fontName, no need to uninstall.
LIGHT = FONTS['PromisePageBot-Light']
BOOK = FONTS['PromisePageBot-Book']
BOOK_ITALIC = FONTS['PromisePageBot-Book']
MEDIUM = FONTS['PromisePageBot-Medium']
SEMIBOLD = FONTS['PromisePageBot-Semibold']
BOLD = FONTS['PromisePageBot-Bold']

tt = """Waar in de traditie van werken met opmaakprogrammatuur zoals Quark XPress en InDesign altijd een menselijke beslissing de definitieve opmaak van een pagina bepaalt, zijn er steeds meer situaties waarin dat geen optie is. Doordat steeds meer pagina’s worden gegenereerd met inhoud die uit een database komt – of van een online source – en waar de selectie van de informatie direct wordt bepaald door eigenschappen van de lezer, van de pagina’s automatisch worden berekend."""

fs = FormattedString('')
fs.lineHeight(28)
fs.fontSize(24)
fs.font('Georgia')
fs += tt+' '+tt
print '$$$$$', fs.fontAscender(), fs.fontDescender(), fs.fontAscender()-fs.fontDescender(), fs.fontLeading(), fs.fontLineHeight()

textBox(fs, (20, 20, 400, 900))

stroke(0)
fill(None)
for n in range(20, 920, 28):
    line((0, n), (600, n))
    
fs = FormattedString('')
fs.lineHeight(28)
fs.fontSize(24)
fs.font(BOOK)
fs += tt+' '+tt
print '$$$$$', fs.fontAscender(), fs.fontDescender(), fs.fontAscender()-fs.fontDescender(), fs.fontLeading(), fs.fontLineHeight()

textBox(fs, (500, 20, 400, 900))

stroke(0)
strokeWidth(0.5)
fill(None)
for n in range(20, 920, 28):
    line((0, n), (900, n))
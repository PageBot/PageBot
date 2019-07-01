#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     constants.py
#
#     Holds the (style) constants of PageBot.
#

from pagebot.toolbox.units import pt, px, em, mm, inch, EM_FONT_SIZE

# General indicators

FIT = 'fit' # Special fontsize that makes text fitting on element width.

ONLINE = 'online' # Positions of borders
INLINE = 'inline'
OUTLINE = 'outline'

LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'
MIDDLE = 'middle'
JUSTIFIED = 'justified'
TOP = 'top'
BOTTOM = 'bottom'
FRONT = 'front' # Align in front, z-axis, nearest to view, perpendicular to the screen.
BACK = 'back' # Align in back, z-axis, nearest to view, perpendicular to the screen.
DISPLAY_BLOCK = 'block' # Add \n to the end of a style block. Similar to CSS behavior of <div>
DISPLAY_INLINE = 'inline' # Inline style, similar to CSS behavior of <span>

# These sizes are all portrait. For Landscape simply reverse to (H, W) usage.
# All measure are defined in Unit instances, to make conversion easier.
#
# ISO A Sizes
#
A0 = mm(841, 1189) # Millimeters real Mm unit instance.
A1 = mm(594, 841)
A2 = mm(420, 594)
A3 = mm(297, 420)
A4 = mm(210, 297)
A5 = mm(148, 210)
A6 = mm(105, 148)
A7 = mm(74,  105)
A8 = mm(52,  74)
A9 = mm(37,  52)
A10 = mm(26, 37)

A2Square = A2[0], A2[0] # Square of A2 (portrait, short side)
A3Square = A3[0], A3[0] # Square of A3 (portrait, short side)
A4Square = A4[0], A4[0] # Square of A4 (portrait, short side)
A5Square = A5[0], A5[0] # Square of A5 (portrait, short side)

A4Rounded = pt(595, 842) # Rounded to points pt(595, 842) to fit exact column measures

#
# ISO B Sizes
#
B0 = mm(1000,1414)
B1 = mm(707, 1000)
B2 = mm(500, 707)
B3 = mm(353, 500)
B4 = mm(250, 353)
B5 = mm(176, 250)
B6 = mm(125, 176)
B7 = mm(88,  125)
B8 = mm(62,  88)
B9 = mm(44,  62)
B10 = mm(31, 44)
#
# ISO C Envelop Sizes
#
C0 = mm(917, 1297)
C1 = mm(648, 917)
C2 = mm(458, 648)
C3 = mm(324, 458)
C4 = mm(229, 324)
C5 = mm(162, 229)
C6 = mm(114, 162)
C7 = mm(81,  114)
C8 = mm(57,  81)
C9 = mm(40,  57)
C10 = mm(28, 40)

# American Sizes as non-rounded values
HalfLetter = inch(8.5, 5.5)
Letter = inch(8.5, 11)
Legal = inch(8.5, 14)
JuniorLegal = inch(5, 8)
Tabloid = inch(11, 17)
# Other rounded definintions compatible to DrawBot predefines
#Screen = getContext().screenSize() # Current screen size. TODO: fix this
Ledger = pt(1224, 792)
Statement = pt(396, 612)
Executive = pt(540, 720)
Folio = pt(612, 936)
Quarto = pt(610, 780)
Size10x14 = pt(720, 1008)


# Hybrid sizes
# International generic fit for stationary
A4Letter = A4[0], Letter[1] # 210mm width and 11" height will always fit printer and fax.
# Oversized (depending on requirement of printer, including 36pt view padding for crop marks
A4Oversized = A4[0]+inch(1), A4[1]+inch(1)
A3Oversized = A3[0]+inch(1), A3[1]+inch(1)

# International Postcard Size
IntPostcardMax = mm(235, 120)
IntPostcardMin = mm(140, 90)
AnsichtCard = pt(A6[1].rounded, A6[0].rounded) # Landscape Rounded A6

# US Postal Postcard Size
USPostcardMax = inch(6, 4.25)
USPostcardMin = inch(5, 3.5)

# Business card, https://nl.wikipedia.org/wiki/Visitekaartje
ISO216 = A8
BusinessCard = ISOCreditCard = mm(85.60, 53.98)
# USA, Canada
BusinessCardUS = inch(3.5, 2)
# Germany, France, Italy, Spain, UK, Netherlands, Portugal, Iceland IS
BusinessCardEurope = mm(85, 55)
# Poland PL, Czech Republic CZ, Slovakia SK, Hungary HU, Croatia HR, Bosnia and Herzegovina BA,
# Serbia, Montenegro, Albania AL, Macedonia MK, Bulgaria BG, Romania RO, Moldova MD, Ukraine UA,
# Belarus BY, Lithuania LT, Latvia LV, Estonia EE, Finland FI, Georgia GE, Armenia AM, Azerbaijan AZ,
# Sri Lanka LK, South Korea KR, South Africa ZA, Namibia NA, Israel IL,
# Mexico MX, Brazil BR, Argentina AR, Venezuela VE, Russia RU, Kazakhstan KZ, Uzbekistan UZ
BusinessCardEastEurope = BusinessCardWorld = mm(90, 50)
# Iran IR
BusinessCardIran = mm(85, 48)
# Australia, New Zealand, India IN, Taiwan TW, Vietnam VN, Thailand TH, Cambodia KH, Laos LA,
# Myanmar (Burma) MM, Bangladesh BD, Bhutan BT, Nepal NP, Colombia CO,
# Norway NO, Sweden SE, Denmark DK, Greece GR
BusinessCardAustralia = mm(90, 55)
# Turkey TR
BusinessCardTurkey = mm(85, 50)
# Egypt EG
BusinessCardTurkey = mm(87), mm(57)
# China CN, Hong Kong HK, Singapore SG, Mongolia MN, Malaysia MY
BusinessCardChina = mm(90, 54)
BusinessCardJapan = mm(91, 55)

# Popular Online Business Card Printers
# Vistaprint
BusinessCardVistaprint = mm(87, 49)
# Moo Cards
BusinessCardMoo = mm(84, 55)
BusinessCardMooMini = mm(70, 28)
# Zazzle Cards
BusinessCardZazzle = inch(3.5, 2)
BusinessCardZazzleChubby = inch(3.5, 2.5)
BusinessCardZazzleSkinny = inch(3.5, 1)

# Newspapers
Tabloid = inch(11, 16.9)
Broadsheet = inch(23.5, 29.5)
Berliner = inch(12.4, 18.5)

# Instagram
InstagramHires = px(2048, 2048)
Instagram = px(1080, 1080)
InstagramLegacy = px(640, 640) # Standard before July 6, 2015
InstagramLandscape = px(1080, 566)
InstagramPortrait = px(1080, 1350)

# Standard size of online printing sites.
# TODO: Add more online services and adapt other parameters/preferences for these PDF's

# www.blurb.com
BlurbPhotobookSmallSquare = inch(7, 7)
BlurbPhotobookPortrait = inch(8, 10)
BlurbPhotobookLandcape = inch(10, 8)
BlurbPhotobookLargeFormat = inch(13, 11)
BlurbPhotobookLargeSquare = inch(12, 12)
BlurbBookSmall = inch(5, 8)
BlurbBookMiddle = inch(6, 9)
BlurbBookLarge = inch(8, 10)
BlurbMagazine = inch(8.5, 11) # Premium & economy

# https://www.newspaperclub.com/create/artwork-guidelines
# Recommended minimum margins: mm(10)
NewsPaperClub_BroadSheet = mm(350, 500)
NewsPaperClub_BroadSheet_Spread = mm(2*350, 500)
# Recommended minimum margins: mm(15)
NewsPaperClub_Tabloid = mm(289, 380)
NewsPaperClub_Tabloid_Spread = mm(2*289, 380)
# Recommended bleed: mm(5)
NewsPaperClub_Mini = mm(180, 260)
NewsPaperClub_Mini_Spread = mm(2*180, 260)

# www.overnightprints.com
OpBookletSmall = inch(5.5, 8.5)
OpBooklet = inch(8.5, 11)

# www.bookbaby.com
# thebookpatch.com

# Standard view port sizes.
# http://mediag.com/news/popular-screen-resolutions-designing-for-all/

# Apple
iPhoneeX = pt(375, 812) # Pixelsize: 1125 x 2436
iPhone8Plus = pt(414, 736) # 1080 x 1920
iPhone8 = pt(375, 667) # 750 x 1334
iPhone7Plus = pt(414, 736) # 1080 x 1920
iPhone7 = pt(375, 667) # 750 x 1334
iPhone6Plus = iPhone6SPlus = pt(414, 736) # 1080 x 1920
iPhone6 = pt(375, 667) # 750 x 1334
iPHone5 = pt(320, 568) # 640 x 1136
iPodTouch = pt(320, 568) # 640 x 1136
iPadPro = pt(1024, 1366) # 2048 x 2732
iPadThirdGeneration = iPadFourthGeneration = pt(768, 1024) # 1536 x 2048
iPadAir1 = iPadAir2 = pt(768, 1024) # 1536 x 2048
iPadMini = pt(768, 1024) #  768 x 1024
iPadMini2 = iPadMini3 = pt(768, 1024) # 1536 x 2048

# Android
Nexus6P = pt(411, 731) # 1440 x 2560
Nexus5X = pt(411, 731) # 1080 x 1920
GooglePixel = pt(411, 731) # 1080 x 1920
GooglePixelXL = pt(411, 731) # 1440 x 2560
GooglePixel2 = pt(411, 731) # 1080 x 1920
GooglePixel2XL = pt(411, 731) # 1440 x 2560
SamsungGalaxyNote5 = pt(480, 853) # 1440 x 2560
LGG5 = pt(480, 853) # 1440 x 2560
OnePlus3 = pt(480, 853) # 1080 x 1920
SamsungGalaxyS9 = pt(360, 740) # 1440 x 2960
SamsungGalaxyS9Plus = pt(360, 740) # 1440 x 2960
SamsungGalaxyS8 = pt(360, 740) # 1440 x 2960
SamsungGalaxyS8Plus = pt(360, 740) # 1440 x 2960
SamsungGalaxyS7 = pt(360, 640) # 1440 x 2560
SamsungGalaxyS7Edge = pt(360, 640) # 1440 x 2560
Nexus7 = pt(600, 960) # 1200 x 1920
Nexus9 = pt(768, 1024) # 1536 x 2048
SamsungGalaxyTab10 = pt(800, 1280) # 800 x 1280
ChromebookPixel = pt(1280, 850) # 2560 x 1700

# Types of Quire formats, how to compose pages from folding sheets.
# Gutter between the pages is defined by the page.margin values.
QUIRE_SINGLE = (1, 1) # Single page
QUIRE_SPREAD = (2, 1) # Spread of 2 connected pages
QUIRE_2x2 = (2, 2) # is a Quire of 4 pages, e.g. to be cut as separate sheets
QUIRE_8x4 = (8, 4) # is a Quire of 32 separate pages, e.g. to be cut as 32 business cards.
QUIRE_LEPARELLO3 = (3, 1) # is a leparello of 3 connected pages.
QUIRE_LEPARELLO4 = (4, 1) # is a leparello of 4 connected pages.
QUIRE_FOLIO = (QUIRE_SPREAD, 2) # 2°, a Quire of 2 spreads
QUIRE_QUARTO = (QUIRE_FOLIO, 2) # 4°
QUIRE_OCTAVO = (QUIRE_QUARTO, 2) # 8°, folding into 16 pages

# Color bar parameter for view.showColorBars = set()
# http://the-print-guide.blogspot.com/2010/07/color-bar.html
# http://www.sdg-net.co.jp/products/x-rite/products_detail/pdf/Creating_the_Perfect_Colorbar.pdf
# http://www.eci.org/en/downloads
# Markers for view color bar building.
COLORBAR_TOP = TOP # Indicate that selection of color bars should run on top
COLORBAR_BOTTOM = BOTTOM # Indicate that selection of color bars should run on bottom
COLORBAR_LEFT = LEFT # Indicate that selection of color bars should run on left
COLORBAR_RIGHT = RIGHT # Indicate that selection of color bars should run on right

# Predefined color bars
COLORBAR_SOLID_INK = 'SolidInk'
COLORBAR_TWOCOLOR_OVERPRINT = 'TwoColorOverprint'
COLORBAR_SLUR_DOUBLING = 'SlurDoubling'
COLORBAR_GRAY_BALANCE = 'GrayBalance'
COLORBAR_BROWN_BALANCE = 'BrownBalance'
COLORBAR_DOT_GAIN = 'DotGain'
COLORBAR_SPOT_COLOR = 'SpotColor'

# Color bar files
ECI_GrayConL = 'color/ECI_GrayConL_FOGRA52_v3.pdf'
ECI_GrayConM = 'color/ECI_GrayConM_FOGRA52_v3.pdf'
ECI_GrayConM_i1 = 'color/ECI_GrayConM_i1_FOGRA52_v3.pdf'
ECI_GrayConS = 'color/ECI_GrayConS_FOGRA52_v3.pdf'
DEFAULT_COLOR_BARS = (ECI_GrayConL, COLORBAR_LEFT)

# Default initialize point as long as elements don't have a defined position.
# Actual location depends on value of e.originTop flag.
# If document.originTop == True (or page.originTop == True),
# origin is on top-left of the page. Y-positive direction is down.
# If document.originTop == False (or page.originTop == False),
# origin is on bottom-left of the page. Y-positive direction is up.
ORIGIN = pt(0, 0, 0) # Default origin if location is omitted.

# Min/max values for element sizes. Makes sure that elements dimensions for
# (w,h) never get 0.
XXXL = 2**32 # Arbitrary large size that is not system dependent, such as sys.maxsize is.

# For document, using imaginary depth for layers and shadow
DEFAULT_DOC_WIDTH, DEFAULT_DOC_HEIGHT, DEFAULT_DOC_DEPTH = pt(1000, 1000, 100)
# For elements, using imaginary depth for layers and shadow
DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_DEPTH = pt(100, 100, 100)
# Default size for windows, e.g. created with VanillaContext
DEFAULT_WINX, DEFAULT_WINY, DEFAULT_WINW, DEFAULT_WINH = pt(50, 50, DEFAULT_WIDTH, DEFAULT_HEIGHT)

# Default page size: Rounded A4 width, Letter 11" height, and pt(100) deep.
W, H, D = A4Letter[0], A4Letter[1], DEFAULT_DEPTH

DEFAULT_FRAME_DURATION = 1 # Default duration of a gif frame.

# Language codes from ISO Language Code Table:
#
#   http://www.lingoes.net/en/translator/langcode.htm
#
# Used with DrawBot-FormattedString hyphenation. TODO test if all codes really
# have an effect, add all to LANGUAGES dictionary.
LANGUAGE_EN     = 'en'      # English
LANGUAGE_NL     = 'nl'      # Dutch
LANGUAGE_NL_BE  = 'nl-BE'   # Belgium
LANGUAGE_NL_NL  = 'nl-NL'   # Netherlands
LANGUAGE_DK     = 'dk'      # Danish
LANGUAGE_PT_BR  = 'pt-BR'   # Portuguese (Brazil)

DEFAULT_LANGUAGE = LANGUAGE_EN

LANGUAGE_AF     = 'af'      # Afrikaans
LANGUAGE_AF_ZA  = 'af-ZA'   # Afrikaans (South Africa)
LANGUAGE_AR     = 'ar'      # Arabic
LANGUAGE_AR_AE  = 'ar-AE'   # Arabic (U.A.E.)
LANGUAGE_AR_BH  = 'ar-BH'   # Arabic (Bahrain)
LANGUAGE_AR_DZ  = 'ar-DZ'   # Arabic (Algeria)
LANGUAGE_AR_EG  = 'ar-EG'   # Arabic (Egypt)
LANGUAGE_AR_IQ  = 'ar-IQ'   # Arabic (Iraq)
LANGUAGE_AR_JO  = 'ar-JO'   # Arabic (Jordan)
LANGUAGE_AR_KW  = 'ar-KW'   # Arabic (Kuwait)
LANGUAGE_AR_LB  = 'ar-LB'   # Arabic (Lebanon)
LANGUAGE_AR_LY  = 'ar-LY'   # Arabic (Libya)
LANGUAGE_AR_MA  = 'ar-MA'   # Arabic (Morocco)
LANGUAGE_AR_OM  = 'ar-OM'   # Arabic (Oman)
LANGUAGE_AR_QA  = 'ar-QA'   # Arabic (Qatar)
LANGUAGE_AR_SA  = 'ar-SA'   # Arabic (Saudi Arabia)
LANGUAGE_AR_SY  = 'ar-SY'   # Arabic (Syria)
LANGUAGE_AR_TN  = 'ar-TN'   # Arabic (Tunisia)
LANGUAGE_AR_YE  = 'ar-YE'   # Arabic (Yemen)
LANGUAGE_AZ     = 'az'      # Azeri (Latin)
LANGUAGE_AZ_AZ  = 'az-AZ'   # Azeri (Latin/Cyrillic) (Azerbaijan)
LANGUAGE_BE     = 'be'      # Belarusian

# UPDATE
LANGUAGE_BE_BY  = 'be-BY'   # Belarusian (Belarus)
LANGUAGE_BG     = 'bg'      # Bulgarian
LANGUAGE_BG_BG  = 'bg-BG'   # Bulgarian (Bulgaria)
LANGUAGE_BS_BA  = 'bs-BA'   # Bosnian (Bosnia and Herzegovina)
LANGUAGE_CA     = 'ca'      # Catalan
LANGUAGE_CA_ES  = 'ca-ES'   # Catalan (Spain)
LANGUAGE_CS     = 'cs'      # Czech
LANGUAGE_CS_CZ  = 'cs-CZ'   # Czech (Czech Republic)
LANGUAGE_CY     = 'cy'      # Welsh
LANGUAGE_CY_GB  = 'cy-GB'   # Welsh (United Kingdom)
LANGUAGE_DA     = 'da'      # Danish
LANGUAGE_DA_DK  = 'da-DK'   # Danish (Denmark)
LANGUAGE_DE     = 'de'      # German
LANGUAGE_DA_AT  = 'de-AT'   # German (Austria)
LANGUAGE_DE_CH  = 'de-CH'   # German (Switzerland)
LANGUAGE_DE_DE  = 'de-DE'   # German (Germany)
LANGUAGE_DE_LI  = 'de-LI'   # German (Liechtenstein)
LANGUAGE_DE_LU  = 'de-LU'   # German (Luxembourg)
LANGUAGE_DV     = 'dv'      # Divehi
LANGUAGE_DV_MV  = 'dv-MV'   # Divehi (Maldives)
LANGUAGE_EL     = 'el'      # Greek
LANGUAGE_EL_GR  = 'el-GR'   # Greek (Greece)
LANGUAGE_EN_AU  = 'en-AU'   # English (Australia)
LANGUAGE_EN_BZ  = 'en-BZ'   # English (Belize)
LANGUAGE_EN_CA  = 'en-CA'   # English (Canada)
LANGUAGE_EN_CB  = 'en-CB'   # English (Caribbean)
LANGUAGE_EN_GB  = 'en-GB'   # English (United Kingdom)
LANGUAGE_EN_IE  = 'en-IE'   # English (Ireland)
LANGUAGE_EN_JM  = 'en-JM'   # English (Jamaica)
LANGUAGE_EN_NZ  = 'en-NZ'   # English (New Zealand)
LANGUAGE_EN_PH  = 'en-PH'   # English (Republic of the Philippines)
LANGUAGE_EN_TT  = 'en-TT'   # English (Trinidad and Tobago)
LANGUAGE_EN_US  = 'en-US'   # English (United States)
LANGUAGE_EN_ZA  = 'en-ZA'   # English (South Africa)
LANGUAGE_EN_ZW  = 'en-ZW'   # English (Zimbabwe)
LANGUAGE_EO     = 'eo'      # Esperanto
LANGUAGE_ES     = 'es'      # Spanish
LANGUAGE_ES_AR  = 'es-AR'   # Spanish (Argentina)
LANGUAGE_ES_BO  = 'es-BO'   # Spanish (Bolivia)
LANGUAGE_ES_CL  = 'es-CL'   # Spanish (Chile)
LANGUAGE_ES_CO  = 'es-CO'   # Spanish (Colombia)
LANGUAGE_ES_CR  = 'es-CR'   # Spanish (Costa Rica)
LANGUAGE_ES_DO  = 'es-DO'   # Spanish (Dominican Republic)
LANGUAGE_ES_EC  = 'es-EC'   # Spanish (Ecuador)
# Same code for Spanish Castilian and Spain
LANGUAGE_ES_ES  = 'es-ES'   # Spanish (Castilian)
LANGUAGE_ES_ES  = 'es-ES'   # Spanish (Spain)
LANGUAGE_ES_GT  = 'es-GT'   # Spanish (Guatemala)
LANGUAGE_ES_HN  = 'es-HN'   # Spanish (Honduras)
LANGUAGE_ES_MX  = 'es-MX'   # Spanish (Mexico)
LANGUAGE_ES_NI  = 'es-NI'   # Spanish (Nicaragua)
LANGUAGE_ES_PA  = 'es-PA'   # Spanish (Panama)
LANGUAGE_ES_PE  = 'es-PE'   # Spanish (Peru)
LANGUAGE_ES_PR  = 'es-PR'   # Spanish (Puerto Rico)
LANGUAGE_ES_PY  = 'es-PY'   # Spanish (Paraguay)
LANGUAGE_ES_SV  = 'es-SV'   # Spanish (El Salvador)
LANGUAGE_ES_UY  = 'es-UY'   # Spanish (Uruguay)
LANGUAGE_ES_VE  = 'es-VE'   # Spanish (Venezuela)
LANGUAGE_ET     = 'et'      # Estonian
LANGUAGE_ET_EE  = 'et-EE'   # Estonian (Estonia)
LANGUAGE_EU     = 'eu'      # Basque
LANGUAGE_EU_ES  = 'eu-ES'   # Basque (Spain)
LANGUAGE_FA     = 'fa'      # Farsi
LANGUAGE_FA_IR  = 'fa-IR'   # Farsi (Iran)
LANGUAGE_FI     = 'fi'      # Finnish
LANGUAGE_FI_FI  = 'fi-FI'   # Finnish (Finland)
LANGUAGE_FO     = 'fo'      # Faroese
LANGUAGE_FO_FO  = 'fo-FO'   # Faroese (Faroe Islands)
LANGUAGE_FR     = 'fr'      # French
LANGUAGE_FR_BE  = 'fr-BE'   # French (Belgium)
LANGUAGE_FR_CA  = 'fr-CA'   # French (Canada)
LANGUAGE_FR_CH  = 'fr-CH'   # French (Switzerland)
LANGUAGE_FR_FR  = 'fr-FR'   # French (France)
LANGUAGE_FR_LU  = 'fr-LU'   # French (Luxembourg)
LANGUAGE_FR_MC  = 'fr-MC'   # French (Principality of Monaco)
LANGUAGE_GL     = 'gl'      # Galician
LANGUAGE_GL_ES  = 'gl-ES'   # Galician (Spain)
LANGUAGE_GU     = 'gu'      # Gujarati
LANGUAGE_GU_IN  = 'gu-IN'   # Gujarati (India)
LANGUAGE_HE     = 'he'      # Hebrew
LANGUAGE_HE_IL  = 'he-IL'   # Hebrew (Israel)
LANGUAGE_HI     = 'hi'      # Hindi
LANGUAGE_HI_IN  = 'hi-IN'   # Hindi (India)
LANGUAGE_HR     = 'hr'      # Croatian
LANGUAGE_HR_BA  = 'hr-BA'   # Croatian (Bosnia and Herzegovina)
LANGUAGE_HR_HR  = 'hr-HR'   # Croatian (Croatia)
LANGUAGE_HU     = 'hu'      # Hungarian
LANGUAGE_HU_HU  = 'hu-HU'   # Hungarian (Hungary)
LANGUAGE_HY     = 'hy'      # Armenian
LANGUAGE_HY_AM  = 'hy-AM'   # Armenian (Armenia)
LANGUAGE_ID     = 'id'      # Indonesian
LANGUAGE_ID_ID  = 'id-ID'   # Indonesian (Indonesia)
LANGUAGE_IS     = 'is'      # Icelandic
LANGUAGE_IS_IS  = 'is-IS'   # Icelandic (Iceland)
LANGUAGE_IT     = 'it'      # Italian
LANGUAGE_IT_CH  = 'it-CH'   # Italian (Switzerland)
LANGUAGE_IT_IT  = 'it-IT'   # Italian (Italy)
LANGUAGE_JA     = 'ja'      # Japanese
LANGUAGE_JA_JP  = 'ja-JP'   # Japanese (Japan)
LANGUAGE_KA     = 'ka'      # Georgian
LANGUAGE_KA_GE  = 'ka-GE'   # Georgian (Georgia)
LANGUAGE_KK     = 'kk'      # Kazakh
LANGUAGE_KK_KZ  = 'kk-KZ'   # Kazakh (Kazakhstan)
LANGUAGE_KN     = 'kn'      # Kannada
LANGUAGE_KN_IN  = 'kn-IN'   # Kannada (India)
LANGUAGE_KO     = 'ko'      # Korean
LANGUAGE_KO_KR  = 'ko-KR'   # Korean (Korea)
LANGUAGE_KOK    = 'kok'     # Konkani
LANGUAGE_KOK_IN = 'kok-IN'  # Konkani (India)
LANGUAGE_KY     = 'ky'      # Kyrgyz
LANGUAGE_KY_KG  = 'ky-KG'   # Kyrgyz (Kyrgyzstan)
LANGUAGE_LT     = 'lt'      # Lithuanian
LANGUAGE_LT_LT  = 'lt-LT'   # Lithuanian (Lithuania)
LANGUAGE_LV     = 'lv'      # Latvian
LANGUAGE_LV_LV  = 'lv-LV'   # Latvian (Latvia)
LANGUAGE_MI     = 'mi'      # Maori
LANGUAGE_MI_NZ  = 'mi-NZ'   # Maori (New Zealand)
LANGUAGE_MK     = 'mk'      # FYRO Macedonian
LANGUAGE_MK_MK  = 'mk-MK'   # FYRO Macedonian (Former Yugoslav Republic of Macedonia)
LANGUAGE_MN     = 'mn'      # Mongolian
LANGUAGE_MN_MN  = 'mn-MN'   # Mongolian (Mongolia)
LANGUAGE_MR     = 'mr'      # Marathi
LANGUAGE_MR_IN  = 'mr-IN'   # Marathi (India)
LANGUAGE_MS     = 'ms'      # Malay
LANGUAGE_MS_BN  = 'ms-BN'   # Malay (Brunei Darussalam)
LANGUAGE_MS_MY  = 'ms-MY'   # Malay (Malaysia)
LANGUAGE_MT     = 'mt'      # Maltese
LANGUAGE_MT_MT  = 'mt-MT'   # Maltese (Malta)
# (Bokm?l)
LANGUAGE_NB     = 'nb'      # Norwegian (Bokm?l)
LANGUAGE_NB_NO  = 'nb-NO'   # Norwegian (Bokm?l) (Norway)
LANGUAGE_NN_NO  = 'nn-NO'   # Norwegian (Nynorsk) (Norway)
LANGUAGE_NS     = 'ns'      # Northern Sotho
LANGUAGE_NS_ZA  = 'ns-ZA'   # Northern Sotho (South Africa)
LANGUAGE_PA     = 'pa'      # Punjabi
LANGUAGE_PA_IN  = 'pa-IN'   # Punjabi (India)
LANGUAGE_PL     = 'pl'      # Polish
LANGUAGE_PL_PL  = 'pl-PL'   # Polish (Poland)
LANGUAGE_PS     = 'ps'      # Pashto
LANGUAGE_PS_AR  = 'ps-AR'   # Pashto (Afghanistan)
LANGUAGE_PT     = 'pt'      # Portuguese
LANGUAGE_PT_BR  = 'pt-BR'   # Portuguese (Brazil)
LANGUAGE_PT_PT  = 'pt-PT'   # Portuguese (Portugal)
LANGUAGE_QU     = 'qu'      # Quechua
LANGUAGE_QU_BO  = 'qu-BO'   # Quechua (Bolivia)
LANGUAGE_QU_EC  = 'qu-EC'   # Quechua (Ecuador)
LANGUAGE_QU_PE  = 'qu-PE'   # Quechua (Peru)
LANGUAGE_RO     = 'ro'      # Romanian
LANGUAGE_RO_RO  = 'ro-RO'   # Romanian (Romania)
LANGUAGE_RU     = 'ru'      # Russian
LANGUAGE_RU_RU  = 'ru-RU'   # Russian (Russia)
LANGUAGE_SA     = 'sa'      # Sanskrit
LANGUAGE_SA_IN  = 'sa-IN'   # Sanskrit (India)
LANGUAGE_SE     = 'se'      # Sami (Northern)
# Same Code se-FI se-NO se-SE
LANGUAGE_SE_FI  = 'se-FI'   # Sami (Northern) (Finland)
LANGUAGE_SE_FI  = 'se-FI'   # Sami (Skolt) (Finland)
LANGUAGE_SE_FI  = 'se-FI'   # Sami (Inari) (Finland)
LANGUAGE_SE_NO  = 'se-NO'   # Sami (Northern) (Norway)
LANGUAGE_SE_NO  = 'se-NO'   # Sami (Lule) (Norway)
LANGUAGE_SE_NO  = 'se-NO'   # Sami (Southern) (Norway)
LANGUAGE_SE_SE  = 'se-SE'   # Sami (Northern) (Sweden)
LANGUAGE_SE_SE  = 'se-SE'   # Sami (Lule) (Sweden)
LANGUAGE_SE_SE  = 'se-SE'   # Sami (Southern) (Sweden)
LANGUAGE_SK     = 'sk'      # Slovak
LANGUAGE_SK_SK  = 'sk-SK'   # Slovak (Slovakia)
LANGUAGE_SL     = 'sl'      # Slovenian
LANGUAGE_SL_SI  = 'sl-SI'   # Slovenian (Slovenia)
LANGUAGE_SQ     = 'sq'      # Albanian
LANGUAGE_SQ_AL  = 'sq-AL'   # Albanian (Albania)
# Same code sr-BA sr-SP
LANGUAGE_SR_BA  = 'sr-BA'   # Serbian (Latin) (Bosnia and Herzegovina)
LANGUAGE_SR_BA  = 'sr-BA'   # Serbian (Cyrillic) (Bosnia and Herzegovina)
LANGUAGE_SR_SP  = 'sr-SP'   # Serbian (Latin) (Serbia and Montenegro)
LANGUAGE_SR_SP  = 'sr-SP'   # Serbian (Cyrillic) (Serbia and Montenegro)
LANGUAGE_SV     = 'sv'      # Swedish
LANGUAGE_SV_FI  = 'sv-FI'   # Swedish (Finland)
LANGUAGE_SV_SE  = 'sv-SE'   # Swedish (Sweden)
LANGUAGE_SW     = 'sw'      # Swahili
LANGUAGE_SW_KE  = 'sw-KE'   # Swahili (Kenya)
LANGUAGE_SYR    = 'syr'     # Syriac
LANGUAGE_SYR_SY = 'syr-SY'  # Syriac (Syria)
LANGUAGE_TA     = 'ta'      # Tamil
LANGUAGE_TA_IN  = 'ta-IN'   # Tamil (India)
LANGUAGE_TE     = 'te'      # Telugu
LANGUAGE_TE_IN  = 'te-IN'   # Telugu (India)
LANGUAGE_TH     = 'th'      # Thai
LANGUAGE_TH_TH  = 'th-TH'   # Thai (Thailand)
LANGUAGE_TL     = 'tl'      # Tagalog
LANGUAGE_TL_PH  = 'tl-PH'   # Tagalog (Philippines)
LANGUAGE_TN     = 'tn'      # Tswana
LANGUAGE_TN_ZA  = 'tn-ZA'   # Tswana (South Africa)
LANGUAGE_TR     = 'tr'      # Turkish
LANGUAGE_TR_TR  = 'tr-TR'   # Turkish (Turkey)
LANGUAGE_TT     = 'tt'      # Tatar
LANGUAGE_TT_RU  = 'tt-RU'   # Tatar (Russia)
LANGUAGE_TS     = 'ts'      # Tsonga
LANGUAGE_UK     = 'uk'      # Ukrainian
LANGUAGE_UK_UA  = 'uk-UA'   # Ukrainian (Ukraine)
LANGUAGE_UR     = 'ur'      # Urdu
LANGUAGE_UR_PK  = 'ur-PK'   # Urdu (Islamic Republic of Pakistan)
LANGUAGE_UZ     = 'uz'      # Uzbek (Latin)
# Same code uz-UZ
LANGUAGE_UZ_UZ  = 'uz-UZ'   # Uzbek (Latin) (Uzbekistan)
LANGUAGE_UZ_UZ  = 'uz-UZ'   # Uzbek (Cyrillic) (Uzbekistan)
LANGUAGE_VI     = 'vi'      # Vietnamese
LANGUAGE_VI_VN  = 'vi-VN'   # Vietnamese (Viet Nam)
LANGUAGE_XH     = 'xh'      # Xhosa
LANGUAGE_XH_ZA  = 'xh-ZA'   # Xhosa (South Africa)
LANGUAGE_ZH     = 'zh'      # Chinese
LANGUAGE_ZH_CN  = 'zh-CN'   # Chinese (S)
LANGUAGE_ZH_HK  = 'zh-HK'   # Chinese (Hong Kong)
LANGUAGE_ZH_MO  = 'zh-MO'   # Chinese (Macau)
LANGUAGE_ZH_SG  = 'zh-SG'   # Chinese (Singapore)
LANGUAGE_ZH_TW  = 'zh-TW'   # Chinese (T)
LANGUAGE_ZU     = 'zu'      # Zulu
LANGUAGE_ZU_ZA  = 'zu-ZA'   # Zulu (South Africa)

# Standard external urls for Javascript import and others.
URL_JQUERY = 'https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'
#URL_MEDIA = 'http://code.google.com/p/css3-mediaqueries.js'
URL_D3 = 'https://d3js.org/d3.v5.min.js'

# DEFAULT_FONT_PATH comes from import pagebot.paths
DEFAULT_FONT_SIZE = pt(EM_FONT_SIZE)
DEFAULT_LEADING = em(1.4, base=DEFAULT_FONT_SIZE)
DEFAULT_FALLBACK_FONT_PATH = 'Verdana' # We know for sure this one is there.

# Default element names
DEFAULT_GALLEY_NAME = 'Galley' # Used for page.galley default content storage while no layou defined.

# Types of grid set can be used in the view.showGrid set.
GRID_SQR = 'GridSquare' # Type of grid, drawing as rectangles on columns and rows crossings.
GRID_COL = 'GridColumns' # Show grid as columns, ignoring rows.
GRID_ROW = 'GridRows' # Show grid as row, ignoring columns.
GRID_SQR_BG = 'GridSquareBackground' # Draw grid at background
GRID_COL_BG = 'GridColumnBackground' # Drag grid as columns at background
GRID_ROW_BG = 'GridRowBackground' # Drag grid as row
DEFAULT_GRID = {GRID_COL, GRID_ROW} # If full grid should be shown on top of all elements.
DEFAULT_GRID_BG = {GRID_COL_BG, GRID_ROW_BG} # If full grid should be shown at the back of all elements.
GRID_OPTIONS = {GRID_SQR, GRID_COL, GRID_ROW, GRID_SQR_BG, GRID_COL_BG, GRID_ROW_BG}

DEFAULT_ROWS = 2 # Default amount of columns if underfined.
DEFAULT_COLS = 2

DEFAULT_BASELINE_COLOR = 0.7
DEFAULT_BASELINE_WIDTH = pt(0.5)

BASE_LINE = 'Baseline' # Show baseline grid as lines
BASE_LINE_BG = 'BaselineBackground' # Show baseline grid as lines on background
BASE_INDEX_LEFT = 'BaseIndexLeft' # Show baseline grid index numbers on left side
BASE_INDEX_RIGHT = 'BaseIndexRight' # Show baseline grid index numbers on right side
BASE_Y_LEFT = 'BaseYLeft' # Show baseline grid line marker as y-position on left side
BASE_Y_RIGHT = 'BaseYRight' # Show baseline grid line marker as y-position on right side
BASE_INSIDE = 'BaseInside' # Show grid index or y-position on inside of element border.
DEFAULT_BASELINE = {BASE_LINE_BG, BASE_INDEX_LEFT}
BASE_OPTIONS = {BASE_LINE, BASE_LINE_BG, BASE_INDEX_LEFT, BASE_INDEX_RIGHT, BASE_Y_LEFT,
    BASE_Y_RIGHT, BASE_INSIDE}
BASE_TOP = 'BaselineTop' # Use first baseline position as vertical position of origin (for TextBox)
BASE_BOTTOM = 'BaselineBottom' # Use last baseline position as vertical position of origin (for TextBox)
# Types of alignments
XALIGNS = {None, LEFT, RIGHT, CENTER, JUSTIFIED}
YALIGNS = {None, TOP, BOTTOM, MIDDLE, CENTER, BASE_TOP, BASE_BOTTOM} # "middle" is PageBot. "center" is CSS.
ZALIGNS = {None, FRONT, MIDDLE, BACK}

# Flags where to draw crop marks on folds.
TOP_FOLD = TOP+'Fold'
BOTTOM_FOLD = BOTTOM+'Fold'
LEFT_FOLD = LEFT+'Fold'
RIGHT_FOLD = RIGHT+'Fold'
# Flags to indicate where crop marks and registration marks should be placed, their size and position
# e.showCropMarks = False
DEFAULT_CROPMARKS = {TOP, RIGHT, BOTTOM, LEFT, TOP_FOLD, BOTTOM_FOLD, TOP_FOLD, LEFT_FOLD, RIGHT_FOLD}
# See constants for the options to direct the side, position and size of the registration marks.
# e.showRegistrationMarks = False
DEFAULT_REGISTRATIONMARKS = {TOP, RIGHT, BOTTOM, LEFT}

DEFAULT_MININFOPADDING = pt(36) # Default min-info padding of view, before side information collapses.

VIEW_PRINT = 'Print' # View settings flags to True for print (such as crop marks and registration marks)
VIEW_PRINT2 = 'Print2' # Extended view settings flags to True for print (such as color bars)
VIEW_DEBUG = 'Debug' # View settings flags to True that are useful for debugging a document
VIEW_DEBUG2 = 'Debug2' # Extended view settings flags to True that are useful for debugging a document
VIEW_FLOW = 'Flow' # View settings that show text flow markers.
VIEW_NONE = None # View settings are all off.

INTERPOLATING_TIME_KEYS = ('x', 'y', 'z', 'w', 'h', 'd', 'g', 'fill', 'stroke', 'strokeWidth',
    'textFill', 'location')

# Native PageBot data files.
FILETYPE_JSON = 'json'
FILETYPE_PAGEBOT = 'pbt'
FILETYPE_ZIP = 'zip'
# Image formats (standard in DrawBot)
# See also http://www.drawbot.com/content/canvas/saveImage.html
FILETYPE_PDF = 'pdf'
FILETYPE_JPG = 'jpg'
FILETYPE_JPEG = 'jpeg'
FILETYPE_PNG = 'png'
FILETYPE_SVG = 'svg'
FILETYPE_IDML = 'idml'
FILETYPE_TIF = 'tif'
FILETYPE_TIFF = 'tiff'
FILETYPE_GIF = 'gif'
FILETYPE_BMP = 'bmp'
FILETYPE_ICNS = 'icns'
# Movie formats
FILETYPE_MOV = 'mov'
FILETYPE_MP4 = 'mp4'
# Other formats
FILETYPE_SKETCH = 'sketch' # File format of SketchApp
# Application format
FILETYPE_APP = 'app'
# Font formats
FILETYPE_UFO = 'ufo'
FILETYPE_TTF = 'ttf'
FILETYPE_OTF = 'otf'
# Text formats
FILETYPE_TXT = 'txt'
FILETYPE_MD = 'md' # Markdown file extension

DEFAULT_FILETYPE = FILETYPE_PDF

# Commonly used groups of file types.
IMAGE_TYPES = (FILETYPE_PDF, FILETYPE_JPG, FILETYPE_JPEG, FILETYPE_PNG, FILETYPE_SVG,
    FILETYPE_GIF, FILETYPE_TIF, FILETYPE_TIFF, FILETYPE_BMP, FILETYPE_ICNS)
MOVIE_TYPES = (FILETYPE_MOV, FILETYPE_MP4)
FONT_TYPES = (FILETYPE_UFO, FILETYPE_TTF, FILETYPE_OTF)
TEXT_TYPES = (FILETYPE_TXT, FILETYPE_MD)

# Max image size of scaled cache (used mulitplied by resolution per image type DEFAULT_RESOLUTION_FACTORS
MAX_IMAGE_WIDTH = pt(800)

# Default factors to save images (e.g. thumbnails) larger than used (w, h) size
DEFAULT_RESOLUTION_FACTORS = {
    FILETYPE_PDF: 1, # Not used online, keep size as used.
    FILETYPE_JPG: 1, # Optional 2 oversize scale factor, e.g. for Retina screens?
    FILETYPE_JPEG: 1, # Optional 2 oversize scale factor, e.g. for Retina screens?
    FILETYPE_PNG: 1, # Optional 2 oversize scale factor, e.g. for Retina screens?
    FILETYPE_SVG: 1, # Object-base is in principle resolution independent.
    FILETYPE_GIF: 1, # Optional 2 oversize scale factor, e.g. for Retina screens?
    FILETYPE_TIF: 1, # Not used online, keep size as used.
    FILETYPE_TIFF:1,
}
CACHE_EXTENSIONS = {
    FILETYPE_PDF: FILETYPE_JPG,
    FILETYPE_JPG: FILETYPE_JPG,
    FILETYPE_JPEG: FILETYPE_JPG,
    FILETYPE_PNG: FILETYPE_PNG,
    FILETYPE_SVG: FILETYPE_JPG,
    FILETYPE_GIF: FILETYPE_JPG,
    FILETYPE_TIF: FILETYPE_JPG,
    FILETYPE_TIFF: FILETYPE_JPG,
}
# Standard font style names, with the matching abbreviations they can have in
# font style As reference TYPETR Upgrade is mentioned. In normalized keys, all
# CamelCase is flattened. Works together with
# toolbox.transformer.path2StyleNameParts()

DEFAULT_MARKER_FONT = 'Arial'

FONT_SIZE_MATCHES = {
    'Micro': ('Micro', 100),
    'Readingedge': ('Readingedge', 'ReadingEdge', 'RE', 150),
    'Agate': ('Agate', 200),
    'Caption': ('Caption', 300),
    'Text': ('Text', 400),
    '': ('Default', 500),
    'Deck': ('Deck', 600),
    'Subhead': ('Subhead', 700,),
    'Display': ('Display', 800,),
    'Banner': ('Banner', 900,)
}

FONT_WEIGHT_MATCHES = { # Alternative names
    'Hairline': ('Hairline', 'HairLine', 'Hair', 'Hl'),
    'Thin': ('Thin', 'Thn', 'Thi'),
    'Ultralight':  ('Ultralight', 'UltraLight', 'ULight', 'ULght', 'ULt'),
    'Light': ('Light', 'Lght', 'Lig', 'Lt'),
    'Semilight': ('Semilight', 'SemiLight', 'SLight', 'SLght', 'SLt'),
    'Book': ('Book', 'Bk'),
    'Semibook': ('Semibook', 'SemiBook', 'SBook', 'SBk'),
    'Regular': ('Regular', 'Standard', 'Normal', 'Reg', 'Roman', 'Lean', 'Rom'),
    'Semimedium': ('Semimedium', 'SemiMedium', 'SMedium', 'SMed', 'SMd' ),
    'Medium': ('Medium', 'Med', 'Md'),
    'Semibold': ('Semibold', 'SemiBold', 'Demibold', 'Demibld', 'Sbd', 'Sembold', 'SBold', 'Sem', 'Demi', 'Dem'),
    'Bold': ('Bold', 'Bol', 'Bd'),
    'Extrabold': ('Extrabold', 'XBold', 'XBd'),
    'Heavy': ('Heavy', 'Hvy'),
    'Black': ('Black', 'Blck', 'Blk', 'Bla', 'Fat'),
    'Extrablack': ('Extrablack', 'XBlack', 'XBlck', 'XBlk'),
    'Ultrablack': ('Ultrablack', 'UBlack', 'UBlck', 'UBlk'),
}
FONT_WEIGHT_RANGES = { # OS/2 standard values and alternative ranges
    'Hairline': range(0, 261), # Upgrade 260
    'Thin': range(260, 275), # Upgrade 270 + list(range(275, 295)), # Upgrade 280
    'Ultralight': range(275, 295),
    'Light': range(295, 320), # Upgrade 300
    'Semilight': range(320, 350), # Upgrade 350
    'Book': range(350, 395), # Upgrade 390
    'Semibook': range(395, 400), # Upgrade 395
    'Regular': range(400, 450), # Upgrade 400
    'Semimedium': range(450, 550), # Upgrade 450
    'Medium': range(450, 550), # Upgrade 500
    'Semibold': range(550, 650), # Upgrade 600
    'Bold': range(650, 725), # Upgrade 700
    'Extrabold': range(725, 755), # 750
    'Heavy': range(755, 780), # 760
    'Black': range(780, 825), # Upgrade 800
    'Extrablack': range(825, 875), # Upgrade 850
    'Ultrablack': range(857, 1000), # Upgrade 900
}
FONT_WIDTH_MATCHES = { # Match on exact alternative
    'Skyline': ('Skyline', 'SkyLine', 1, 100),
    'Ultracompressed': ('Ultracompressed', 'UCompressed', 'Ucompressed', 'Ucomp', 'UComp', 120),
    'Extracompressed': ('Extracompressed', 'XCompressed', 'Xcompressed', 'Xcomp', 'XComp', 140),
    'Compressed': ('Compressed', 'Compr', 'Comp', 'Cmp', 2, 200),
    'Ultracondensed': ('Ultracondensed', 'UCondensed', 'UCond', 250),
    'Extracondensed': ('Extracondensed', 'XCondensed', 'XCond', 3, 300),
    'Condensed': ('Condensed', 'Cond', 'Cnd', 'Cn', 4, 400),
    'Narrow': ('Narrow', 'Nrrw', 'Narr', 'Nar', 440),
    'Normal': ('Normal', 'Nrm', 'Norm', 'Nrml', 'Nor', 5, 500),
    'Wide': ('Wide', 'Wd', 6, 600),
    'Extended': ('Extended', 'Expanded', 'Expd', 'Exp', 'Ext', 'Extnd', 7, 700),
    'Extraextended': ('Extraextended', 'Xextended', 'XExtended', 'XExp', 'XExt', 8, 800),
    'Ultraextended': ('Ultraextended', 'Uextended', 'UExtended', 'XExt', 'UExt', 9, 900),
}
FONT_WIDTH_RANGES = {
    'Skyline': range(11, 110), # 100, Reseve 1-10
    'Ultracompressed': range(110, 130), # 120
    'Extracompressed': range(130, 150), # 140
    'Compressed': range(150, 220), # 200
    'Ultracondensed': range(220, 270), # 250,
    'Extracondensed': range(270, 350), # 300,
    'Condensed': range(350, 420), # 400
    'Narrow': range(420, 450), # 440,
    'Normal':  range(450, 550), # 500
    'Wide': range(550, 650), # 600
    'Extended': range(650, 750), # 700
    'Extraextended': range(750, 850), # 800
    'Ultraextended': range(850, 999), # 900
}

FONT_ITALIC_MATCHES = {
    'Italic': ('Italic', 'Ita', 'It'),
}
# Expand for the number entries:
for d in (FONT_SIZE_MATCHES, FONT_WEIGHT_MATCHES, FONT_WIDTH_MATCHES):
    for key, values in list(d.items()):
        for value in values:
            if isinstance(value, int):
                d[value] = values
# TODO: Add FONT_WEIGHT_RANGES and FONT_WIDTH_RANGES as keys

# CSS EASE parameters, defining the CSS transforamtion speed
# See https://easings.net/
#   -webkit-transition: all 600ms easing’s Bezier curve;
#    transition:         all 600ms easing’s Bezier curve; }
#
CSS_EASE = 'ease'
CSS_LINEAR = 'linear'
CSS_EASE_IN = 'ease-in'
CSS_EASE_OUT = 'ease-out'

CSS_EASE_INTOUT = 'ease-in-out'
CSS_EASE_INQUAD = 'easeInQuad'
CSS_EASE_INCUBIC = 'easeInCubic'
CSS_EASE_INQUART = 'easeInQuart'
CSS_EASE_INQUINT = 'easeInQuint'
CSS_EASE_INSINE = 'easeInSine'
CSS_EASE_INEXPO = 'easeInExpo'
CSS_EASE_INCIRC = 'easeInCirc'
CSS_EASE_INBACK = 'easeInBack'

CSS_EASE_OUTQUAD = 'easeOutQuad'
CSS_EASE_OUTCUBIC = 'easeOutCubic'
CSS_EASE_OUTQUART = 'easeOutQuart'
CSS_EASE_OUTQUINT = 'easeOutQuint'
CSS_EASE_OUTSINE = 'easeOutSine'
CSS_EASE_OUTEXPO = 'easeOutExpo'
CSS_EASE_OUTCIRC = 'easeOutCirc'
CSS_EASE_OUTBACK = 'easeOutBack'

CSS_EASE_INOUTQUAD = 'easeInOutQuad'
CSS_EASE_INOUTCUBIC = 'easeInOutCubic'
CSS_EASE_INOUTQUART = 'easeInOutQuart'
CSS_EASE_INOUTQUINT = 'easeInOutQuint'
CSS_EASE_INOUTSINE = 'easeInOutSine'
CSS_EASE_INOUTEXPO = 'easeInOutExpo'
CSS_EASE_INOUTCIRC = 'easeInOutCirc'
CSS_EASE_INOUTBACK= 'easeInOutBack'

# Note that any conversion between RAL (paint) and RGB can only be a
# approximation. Material colors by definition have a different range of
# possible colors than RGB.
RAL_NAMERGB = {
    # http://rgb.to/ral/1000
    # http://www.pats.ch/formulaire/unites/unites11.aspx
    # Numbers are recalculated as floats 0..1
    # {1024: ('ochre yellow', (0.7098039215686275, 0.5490196078431373, 0.30980392156862746)), ...}
    1000: ('green beige', (204, 204, 153)), # cccc99
    1001: ('beige', (10, 170, 90)), # d2aa5a
    1002: ('sand yellow', (208, 168, 24)), # d0a818
    1003: ('signal yellow', (255, 204, 0)), # ffcc00
    1004: ('golden yellow', (224, 176, 0)), # e0b000
    1005: ('honey yellow', (201, 135, 33)), # c98721
    1006: ('maize yellow', (227, 167, 41)), # e3a729
    1007: ('daffodil yellow', (221, 159, 35)), # dd9f23
    1011: ('brown beige', (173, 121, 41)), # ad7a29
    1012: ('lemon yellow', (227, 184, 56)), # e3b838
    1013: ('oyster white', (255, 245, 227)), # fff5e3
    1014: ('ivory', (240, 214, 171)), # f0d6ab
    1015: ('light ivory', (251, 235, 204)), # fcebcc
    1016: ('sulfur yellow', (255, 245, 66)), # fff541
    1017: ('saffron yellow', (255, 171, 89)), # ffab59
    1018: ('zinc yellow', (255, 214, 77)), # ffd64d
    1019: ('grey beige', (163, 140, 121)), # a38c7a
    1020: ('olive yellow', (156, 143, 97)), # 9c8f61
    1021: ('rape yellow', (251, 189, 31)), # fcbd1f
    1023: ('traffic yellow', (251, 189, 31)), # fcbd1f
    1024: ('ochre yellow', (181, 140, 79)), # b58c4f
    1026: ('luminous yellow', (255, 255, 10)), # ffff0a
    1027: ('curry', (153, 117, 33)), # 997521
    1028: ('melon yellow', (255, 140, 26)), # ff8c1a
    1032: ('broom yellow', (227, 163, 41)), # e3a329
    1033: ('dahlia yellow', (255, 148, 54)), # ff9436
    1034: ('pastel yellow', (247, 153, 91)), # f7995c
    2000: ('yellow orange', (224, 94, 31)), # e05e1f
    2001: ('red orange', (186, 46, 33)), # ba2e21
    2002: ('vermilion', (204, 36, 28)), # cc241c
    2003: ('pastel orange', (255, 99, 54)), # ff6336
    2004: ('pure orange', (241, 59, 28)), # f23b1c
    2005: ('luminous orange', (251, 28, 20)), # fc1c14
    2007: ('luminous bright orange', (255, 117, 33)), # ff7521
    2008: ('bright red orange', (250, 79, 41)), # fa4f29
    2009: ('traffic orange', (235, 59, 28)), # eb3b1c
    2010: ('signal orange', (211, 69, 41)), # d44529
    2011: ('deep orange', (237, 91, 0)), # ed5c00
    2012: ('salmon orange', (221, 81, 71)), # de5247
    3000: ('flame red', (171, 31, 28)), # ab1f1c
    3001: ('signal red', (163, 23, 26)), # a3171a
    3002: ('carmine red', (163, 26, 26)), # a31a1a
    3003: ('ruby red', (138, 18, 20)), # 8a1214
    3004: ('purple red', (105, 15, 20)), # 690f14
    3005: ('wine red', (79, 18, 26)), # 4f121a
    3007: ('black red', (46, 18, 26)), # 2e121a
    3009: ('oxide red', (94, 33, 33)), # 5e2121
    3011: ('brown red', (120, 20, 23)), # 781417
    3012: ('beige red', (204, 130, 115)), # cc8273
    3013: ('tomato red', (150, 31, 28)), # 961f1c
    3014: ('antique pink', (217, 101, 117)), # d96675
    3015: ('light pink', (231, 156, 181)), # e89cb5
    3016: ('coral red', (166, 36, 38)), # a62426
    3017: ('rose', (209, 54, 84)), # d13654
    3018: ('strawberry red', (207, 41, 66)), # cf2941
    3020: ('traffic red', (199, 23, 18)), # c71711
    3022: ('salmon pink', (217, 89, 79)), # d9594f
    3024: ('luminous red', (251, 10, 28)), # fc0a1c
    3026: ('luminous bright red', (251, 20, 20)), # fc1414
    3027: ('raspberry red', (181, 18, 51)), # b51233
    3031: ('orient red', (166, 28, 46)), # a61c2e
    4001: ('red lilac', (130, 64, 48)), # 824030
    4002: ('red violet', (143, 38, 64)), # 8f2640
    4003: ('heather violet', (201, 56, 140)), # c9388c
    4004: ('claret violet', (91, 8, 43)), # 5c082b
    4005: ('blue lilac', (99, 61, 156)), # 633d9c
    4006: ('traffic purple', (145, 15, 101)), # 910f66
    4007: ('purple violet', (56, 10, 46)), # 380a2e
    4008: ('signal violet', (125, 31, 121)), # 7d1f7a
    4009: ('pastel violet', (158, 115, 148)), # 9e7394
    4010: ('telemagenta', (191, 23, 115)), # bf1773
    5000: ('violet blue', (23, 51, 107)), # 17336b
    5001: ('green blue', (10, 51, 84)), # 0a3354
    5002: ('ultramarine blue', (0, 15, 117)), # 000f75
    5003: ('sapphire blue', (0, 23, 69)), # 001745
    5004: ('black blue', (3, 13, 31)), # 030d1f
    5005: ('signal blue', (0, 46, 121)), # 002e7a
    5007: ('brillant blue', (38, 79, 135)), # 264f87
    5008: ('gray blue', (26, 41, 56)), # 1a2938
    5009: ('azure blue', (23, 69, 111)), # 174570
    5011: ('steel blue', (0, 43, 111)), # 002b70
    5012: ('light blue', (41, 115, 184)), # 2973b8
    5013: ('cobalt blue', (0, 18, 69)), # 001245
    5014: ('pigeon blue', (77, 105, 153)), # 4d6999
    5015: ('sky blue', (23, 97, 171)), # 1761ab
    5017: ('traffic blue', (0, 59, 128)), # 003b80
    5018: ('turquoise blue', (56, 148, 130)), # 389481
    5019: ('capri blue', (10, 66, 120)), # 0a4278
    5020: ('steel blue', (5, 51, 51)), # 053333
    5021: ('water blue', (26, 121, 99)), # 1a7a63
    5022: ('night blue', (0, 8, 79)), # 00084f
    5023: ('distant blue', (46, 81, 143)), # 2e528f
    5024: ('pastel blue', (87, 140, 171)), # 578cab
    6000: ('patina green', (51, 120, 84)), # 337854
    6001: ('emerald green', (38, 101, 81)), # 266651
    6002: ('leaf green', (38, 87, 33)), # 265721
    6003: ('olive green', (61, 69, 46)), # 3d452e
    6004: ('blue green', (13, 59, 46)), # 0d3b2e
    6005: ('moss green', (10, 56, 31)), # 0a381f
    6006: ('grey olive', (41, 43, 46)), # 292b2e
    6007: ('bottle green', (28, 38, 23)), # 1c2617
    6008: ('brown green', (33, 33, 26)), # 21211a
    6009: ('fir green', (23, 41, 28)), # 17291c
    6010: ('grass green', (54, 105, 38)), # 366926
    6011: ('reseda green', (94, 125, 79)), # 5e7d4f
    6012: ('black green', (31, 46, 43)), # 1f2e2b
    6013: ('reed green', (117, 115, 79)), # 75734f
    6014: ('yellow olive', (51, 48, 38)), # 333026
    6015: ('black olive', (41, 43, 38)), # 292b26
    6016: ('turquoise green', (15, 111, 51)), # 0f7033
    6017: ('yellow green', (64, 130, 54)), # 408236
    6018: ('may green', (79, 168, 51)), # 4fa833
    6019: ('pastel green', (191, 227, 186)), # bfe3ba
    6020: ('chrome green', (38, 56, 41)), # 263829
    6021: ('pale green', (133, 166, 121)), # 85a67a
    6022: ('olive drab', (43, 38, 28)), # 2b261c
    6024: ('traffic green', (36, 145, 64)), # 249140
    6025: ('fern green', (74, 110, 51)), # 4a6e33
    6026: ('opal green', (10, 91, 51)), # 0a5c33
    6027: ('light green', (125, 204, 189)), # 7dccbd
    6028: ('pine green', (38, 74, 51)), # 264a33
    6029: ('mint green', (18, 120, 38)), # 127826
    6032: ('signal green', (41, 138, 64)), # 298a40
    6033: ('mint turquoise', (66, 140, 120)), # 428c78
    6034: ('pastel turquoise', (125, 189, 181)), # 7dbdb5
    7000: ('squirrel grey', (115, 133, 145)), # 738591
    7001: ('silver grey', (135, 148, 166)), # 8794a6
    7002: ('olive grey', (121, 117, 97)), # 7a7561
    7003: ('moss grey', (111, 111, 97)), # 707061
    7004: ('signal grey', (156, 156, 166)), # 9c9ca6
    7005: ('mouse grey', (97, 105, 105)), # 616969
    7006: ('beige grey', (107, 97, 87)), # 6b6157
    7008: ('khaki grey', (105, 84, 56)), # 695438
    7009: ('green grey', (77, 81, 74)), # 4d524a
    7010: ('tarpaulin grey', (74, 79, 74)), # 4a4f4a
    7011: ('iron grey', (64, 74, 84)), # 404a54
    7012: ('basalt grey', (74, 84, 89)), # 4a5459
    7013: ('brown grey', (71, 66, 56)), # 474238
    7015: ('slate grey', (61, 66, 81)), # 3d4251
    7016: ('anthracite grey', (38, 46, 56)), # 262e38
    7021: ('black grey', (26, 33, 41)), # 1a2129
    7022: ('umbra grey', (61, 61, 59)), # 3d3d3b
    7023: ('concrete grey', (121, 125, 117)), # 7a7d75
    7024: ('graphite grey', (48, 56, 69)), # 303845
    7026: ('granite grey', (38, 51, 56)), # 263338
    7030: ('stone grey', (145, 143, 135)), # 918f87
    7031: ('blue grey', (77, 91, 107)), # 4d5c6b
    7032: ('pebble grey', (189, 186, 171)), # bdbaab
    7033: ('cement grey', (121, 130, 117)), # 7a8275
    7034: ('yellow grey', (143, 135, 111)), # 8f8770
    7035: ('light grey', (211, 217, 219)), # d4d9db
    7036: ('platinum grey', (158, 150, 156)), # 9e969c
    7037: ('dusty grey', (121, 125, 128)), # 7a7d80
    7038: ('agate grey', (186, 189, 186)), # babdba
    7039: ('quartz grey', (97, 94, 89)), # 615e59
    7040: ('window grey', (158, 163, 176)), # 9ea3b0
    7042: ('verkehrsgrau a', (143, 150, 153)), # 8f9699
    7043: ('verkehrsgrau b', (64, 69, 69)), # 404545
    7044: ('silk grey', (194, 191, 184)), # c2bfb8
    7045: ('telegrau 1', (143, 148, 158)), # 8f949e
    7046: ('telegrau 1', (120, 130, 140)), # 78828c
    7047: ('telegrau 4', (217, 214, 219)), # d9d6db
    8000: ('green brown', (125, 91, 56)), # 7d5c38
    8001: ('ocher brown', (145, 81, 46)), # 91522e
    8002: ('signal brown', (110, 59, 58)), # 6e3b3a
    8003: ('clay brown', (115, 59, 36)), # 733b24
    8004: ('copper brown', (133, 56, 43)), # 85382b
    8007: ('fawn brown', (94, 51, 33)), # 5e3321
    8008: ('olive brown', (99, 61, 36)), # 633d24
    8011: ('nut brown', (71, 38, 28)), # 47261c
    8012: ('red brown', (84, 31, 31)), # 541f1f
    8014: ('sepia brown', (56, 38, 28)), # 38261c
    8015: ('chestnut brown', (77, 31, 28)), # 4d1f1c
    8016: ('mahogany brown', (61, 31, 28)), # 3d1f1c
    8017: ('chocolate brown', (46, 28, 28)), # 2e1c1c
    8019: ('grey brown', (43, 38, 41)), # 2b2629
    8022: ('black brown', (13, 8, 13)), # 0d080d
    8023: ('orange brown', (156, 69, 41)), # 9c4529
    8024: ('beige brown', (110, 64, 48)), # 6e4030
    8025: ('pale brown', (101, 74, 61)), # 664a3d
    8028: ('terra brown', (64, 46, 33)), # 402e21
    9001: ('cream', (251, 251, 240)), # fcfcf0
    9002: ('grey white', (240, 237, 230)), # f0ede6
    9003: ('signal white', (255, 255, 255)), # ffffff
    9004: ('signal black', (28, 28, 33)), # 1c1c21
    9005: ('jet black', (3, 5, 10)), # 03050a
    9006: ('white aluminium', (166, 171, 181)), # a6abb5
    9007: ('grey aluminium', (125, 121, 120)), # 7d7a78
    9010: ('pure white', (250, 255, 255)), # faffff
    9011: ('graphite black', (13, 18, 26)), # 0d121a
    9016: ('traffic white', (251, 255, 255)), # fcffff
    9017: ('traffic black', (20, 23, 28)), # 14171c
    9018: ('papyrus white', (219, 227, 221)), # dbe3de
}
NAME_RALRGB = {}
# { 'firgreen': (6009, (0.09019607843137255, 0.1607843137254902, 0.10980392156862745)),
#   'fir green': (6009, (0.09019607843137255, 0.1607843137254902, 0.10980392156862745)), ...}
for ral, (spacedName, (ri, gi, bi)) in RAL_NAMERGB.items():
    rgb = ri/255, gi/255, bi/255
    RAL_NAMERGB[ral] = spacedName, rgb # Overwrite with float numbers
    # Make name alterations also accessable (remove space and grey --> gray)
    ralRgb = ral, rgb
    NAME_RALRGB[spacedName] = ralRgb
    name = spacedName.replace(' ', '')
    NAME_RALRGB[name] = ralRgb
    spacedName = spacedName.replace('grey', 'gray')
    NAME_RALRGB[spacedName] = ralRgb
    name = name.replace('grey', 'gray')
    NAME_RALRGB[name] = ralRgb

CSS_COLOR_NAMES = {
    'aliceblue': 0xf0f8ff,
    'antiquewhite': 0xfaebd7,
    'aqua': 0x00ffff,
    'aquamarine': 0x7fffd4,
    'azure': 0xf0ffff,
    'beige': 0xf5f5dc,
    'bisque': 0xffe4c4,
    'black': 0x000000,
    'blanchedalmond': 0xffebcd,
    'blue': 0x0000ff,
    'blueviolet': 0x8a2be2,
    'brown': 0xa52a2a,
    'burlywood': 0xdeb887,
    'cadetblue': 0x5f9ea0,
    'chartreuse': 0x7fff00,
    'chocolate': 0xd2691e,
    'coral': 0xff7f50,
    'cornflowerblue': 0x6495ed,
    'cornsilk': 0xfff8dc,
    'crimson': 0xdc143c,
    'cyan': 0x00ffff,
    'darkblue': 0x00008b,
    'darkcyan': 0x008b8b,
    'darkgoldenrod': 0xb8860b,
    'darkgray': 0xa9a9a9,
    'darkgrey': 0xa9a9a9,
    'darkgreen': 0x006400,
    'darkkhaki': 0xbdb76b,
    'darkmagenta': 0x8b008b,
    'darkolivegreen': 0x556b2f,
    'darkorange': 0xff8c00,
    'darkorchid': 0x9932cc,
    'darkred': 0x8b0000,
    'darksalmon': 0xe9967a,
    'darkseagreen': 0x8fbc8f,
    'darkslateblue': 0x483d8b,
    'darkslategray': 0x2f4f4f,
    'darkslategrey': 0x2f4f4f,
    'darkturquoise': 0x00ced1,
    'darkviolet': 0x9400d3,
    'deeppink': 0xff1493,
    'deepskyblue': 0x00bfff,
    'dimgray': 0x696969,
    'dimgrey': 0x696969,
    'dodgerblue': 0x1e90ff,
    'firebrick': 0xb22222,
    'floralwhite': 0xfffaf0,
    'forestgreen': 0x228b22,
    'fuchsia': 0xff00ff,
    'gainsboro': 0xdcdcdc,
    'ghostwhite': 0xf8f8ff,
    'gold': 0xffd700,
    'goldenrod': 0xdaa520,
    'gray': 0x808080,
    'grey': 0x808080,
    'green': 0x008000,
    'greenyellow': 0xadff2f,
    'honeydew': 0xf0fff0,
    'hotpink': 0xff69b4,
    'indianred': 0xcd5c5c,
    'indigo': 0x4b0082,
    'ivory': 0xfffff0,
    'khaki': 0xf0e68c,
    'lavender': 0xe6e6fa,
    'lavenderblush': 0xfff0f5,
    'lawngreen': 0x7cfc00,
    'lemonchiffon': 0xfffacd,
    'lightblue': 0xadd8e6,
    'lightcoral': 0xf08080,
    'lightcyan': 0xe0ffff,
    'lightgoldenrodyellow': 0xfafad2,
    'lightgray': 0xd3d3d3,
    'lightgrey': 0xd3d3d3,
    'lightgreen': 0x90ee90,
    'lightpink': 0xffb6c1,
    'lightsalmon': 0xffa07a,
    'lightseagreen': 0x20b2aa,
    'lightskyblue': 0x87cefa,
    'lightslategray': 0x778899,
    'lightslategrey': 0x778899,
    'lightsteelblue': 0xb0c4de,
    'lightyellow': 0xffffe0,
    'lime': 0x00ff00,
    'limegreen': 0x32cd32,
    'linen': 0xfaf0e6,
    'magenta': 0xff00ff,
    'maroon': 0x800000,
    'mediumaquamarine': 0x66cdaa,
    'mediumblue': 0x0000cd,
    'mediumorchid': 0xba55d3,
    'mediumpurple': 0x9370db,
    'mediumseagreen': 0x3cb371,
    'mediumslateblue': 0x7b68ee,
    'mediumspringgreen': 0x00fa9a,
    'mediumturquoise': 0x48d1cc,
    'mediumvioletred': 0xc71585,
    'midnightblue': 0x191970,
    'mintcream': 0xf5fffa,
    'mistyrose': 0xffe4e1,
    'moccasin': 0xffe4b5,
    'navajowhite': 0xffdead,
    'navy': 0x000080,
    'oldlace': 0xfdf5e6,
    'olive': 0x808000,
    'olivedrab': 0x6b8e23,
    'orange': 0xffa500,
    'orangered': 0xff4500,
    'orchid': 0xda70d6,
    'palegoldenrod': 0xeee8aa,
    'palegreen': 0x98fb98,
    'paleturquoise': 0xafeeee,
    'palevioletred': 0xdb7093,
    'papayawhip': 0xffefd5,
    'peachpuff': 0xffdab9,
    'peru': 0xcd853f,
    'pink': 0xffc0cb,
    'plum': 0xdda0dd,
    'powderblue': 0xb0e0e6,
    'purple': 0x800080,
    'rebeccapurple': 0x663399,
    'red': 0xff0000,
    'rosybrown': 0xbc8f8f,
    'royalblue': 0x4169e1,
    'saddlebrown': 0x8b4513,
    'salmon': 0xfa8072,
    'sandybrown': 0xf4a460,
    'seagreen': 0x2e8b57,
    'seashell': 0xfff5ee,
    'sienna': 0xa0522d,
    'silver': 0xc0c0c0,
    'skyblue': 0x87ceeb,
    'slateblue': 0x6a5acd,
    'slategray': 0x708090,
    'slategrey': 0x708090,
    'snow': 0xfffafa,
    'springgreen': 0x00ff7f,
    'steelblue': 0x4682b4,
    'tan': 0xd2b48c,
    'teal': 0x008080,
    'thistle': 0xd8bfd8,
    'tomato': 0xff6347,
    'turquoise': 0x40e0d0,
    'violet': 0xee82ee,
    'wheat': 0xf5deb3,
    'white': 0xffffff,
    'whitesmoke': 0xf5f5f5,
    'yellow': 0xffff00,
    'yellowgreen': 0x9acd32,
}

SPOT_RGB = {
    # Numbers are recalculated as 0..1
    'black': (0, 0, 0),
    'blacku': (97, 93, 89),
    'blackc': (45, 41, 38),

    'coolgray11u': (122, 125, 129),
    'coolgray9u': (137, 139, 142),
    'coolgray6u': (164, 166, 168),

    'warmgray2c': (203, 196, 188),
    'warmgray4u': (180, 172, 166),
    'warmgray8u': (146, 137, 129),
    'warmgray10c': (121, 110, 101),
    'warmgray10u': (130, 124, 120),
    'warmgray11c': (110, 98, 89),
    'warmgray11u': (125, 119, 125),

    'processblackc': (39, 37, 31),
    'processblacku': (78, 74, 71),

    'processblue': (0, 133, 202),
    'reflexblue': (0, 20, 137),
    'rubinered': (206, 0, 88),
    'rhodamineredu': (228, 76, 154),
    'yellow': (254, 221, 0),

    'red032c': (239, 51, 64),
    'red032u': (246, 80, 88),

    0: (0, 0, 0), #000000

    100: (244, 237, 124), #F4ED7C
    101: (244, 237, 71), #F4ED47
    102: (249, 232, 20), #F9E814
    103: (198, 173, 15), #C6AD0F
    104: (173, 155, 12), #AD9B0C

    105: (130, 117, 15), #82750F
    106: (247, 232, 89), #F7E859
    107: (249, 229, 38), #F9E526
    108: (249, 221, 22), #F9DD16
    109: (249, 214, 22), #F9D616
    110: (216, 181, 17), #D8B511

    111: (170, 147, 10), #AA930A
    112: (153, 132, 10), #99840A
    113: (249, 229, 91), #F9E55B
    114: (249, 226, 76), #F9E24C
    115: (249, 224, 76), #F9E04C
    116: (252, 209, 22), #FCD116

    116.2: (247, 181, 12), #F7B50C
    117: (198, 160, 12), #C6A00C
    118: (170, 142, 10), #AA8E0A
    119: (137, 119, 25), #897719
    120: (249, 226, 127), #F9E27F
    1205: (247, 232, 170), #F7E8AA

    121: (249, 224, 112), #F9E070
    1215: (249, 224, 140), #F9E08C
    122: (252, 216, 86), #FCD856
    1225: (255, 204, 73), #FFCC49
    123: (255, 198, 30), #FFC61E
    1235: (252, 181, 20), #FCB514

    124: (224, 170, 15), #E0AA0F
    1245: (191, 145, 12), #BF910C
    125: (181, 140, 10), #B58C0A
    1255: (163, 127, 20), #A37F14
    126: (163, 130, 5), #A38205
    1265: (124, 99, 22), #7C6316

    127: (244, 226, 135), #F4E287
    128: (244, 219, 96), #F4DB60
    129: (242, 209, 61), #F2D13D
    130: (234, 175, 15), #EAAF0F
    130.2: (226, 145, 0), #E29100
    131: (198, 147, 10), #C6930A

    132: (158, 124, 10), #9E7C0A
    133: (112, 91, 10), #705B0A
    134: (255, 216, 127), #FFD87F
    1345: (255, 214, 145), #FFD691
    135: (252, 201, 99), #FCC963
    1355: (252, 206, 135), #FCCE87

    136: (252, 191, 73), #FCBF49
    1365: (252, 186, 94), #FCBA5E
    137: (252, 163, 17), #FCA311
    1375: (249, 155, 12), #F99B0C
    138: (216, 140, 2), #D88C02
    1385: (204, 122, 2), #CC7A02

    139: (175, 117, 5), #AF7505
    1395: (153, 96, 7), #996007
    140: (122, 91, 17), #7A5B11
    1405: (107, 71, 20), #6B4714
    141: (242, 206, 104), #F2CE68
    142: (242, 191, 73), #F2BF49

    143: (239, 178, 45), #EFB22D
    144: (226, 140, 5), #E28C05
    145: (198, 127, 7), #C67F07
    146: (158, 107, 5), #9E6B05
    147: (114, 94, 38), #725E26
    148: (255, 214, 155), #FFD69B

    1485: (255, 183, 119), #FFB777
    149: (252, 204, 147), #FCCC93
    1495: (255, 153, 63), #FF993F
    150: (252, 173, 86), #FCAD56
    1505: (244, 124, 0), #F47C00
    151: (247, 127, 0), #F77F00

    152: (221, 117, 0), #DD7500
    1525: (181, 84, 0), #B55400
    153: (188, 109, 10), #BC6D0A
    1535: (140, 68, 0), #8C4400
    154: (153, 89, 5), #995905
    1545: (71, 34, 0), #472200

    155: (244, 219, 170), #F4DBAA
    1555: (249, 191, 158), #F9BF9E
    156: (242, 198, 140), #F2C68C
    1565: (252, 165, 119), #FCA577
    157: (237, 160, 79), #EDA04F
    1575: (252, 135, 68), #FC8744

    158: (232, 117, 17), #E87511
    1585: (249, 107, 7), #F96B07
    159: (198, 96, 5), #C66005
    1595: (209, 91, 5), #D15B05
    160: (158, 84, 10), #9E540A
    1605: (160, 79, 17), #A04F11

    161: (99, 58, 17), #633A11
    1615: (132, 63, 15), #843F0F
    162: (249, 198, 170), #F9C6AA
    1625: (249, 165, 140), #F9A58C
    163: (252, 158, 112), #FC9E70
    1635: (249, 142, 109), #F98E6D

    164: (252, 127, 63), #FC7F3F
    1645: (249, 114, 66), #F97242
    165: (249, 99, 2), #F96302
    165.2: (234, 79, 0), #EA4F00
    1655: (249, 86, 2), #F95602
    166: (221, 89, 0), #DD5900

    1665: (221, 79, 5), #DD4F05
    167: (188, 79, 7), #BC4F07
    1675: (165, 63, 15), #A53F0F
    168: (109, 48, 17), #6D3011
    1685: (132, 53, 17), #843511
    169: (249, 186, 170), #F9BAAA

    170: (249, 137, 114), #F98972
    171: (249, 96, 58), #F9603A
    172: (247, 73, 2), #F74902
    173: (209, 68, 20), #D14414
    174: (147, 51, 17), #933311
    175: (109, 51, 33), #6D3321

    176: (249, 175, 173), #F9AFAD
    1765: (249, 158, 163), #F99EA3
    1767: (249, 178, 183), #F9B2B7
    177: (249, 130, 127), #F9827F
    1775: (249, 132, 142), #F9848E
    1777: (252, 102, 117), #FC6675

    178: (249, 94, 89), #F95E59
    1785: (252, 79, 89), #FC4F59
    1787: (244, 63, 79), #F43F4F
    1788: (239, 43, 45), #EF2B2D
    1788.2: (214, 33, 0), #D62100
    179: (226, 61, 40), #E23D28

    1795: (214, 40, 40), #D62828
    1797: (204, 45, 48), #CC2D30
    180: (193, 56, 40), #C13828
    1805: (175, 38, 38), #AF2626
    1807: (160, 48, 51), #A03033
    181: (124, 45, 35), #7C2D23

    1810: (124, 33, 30), #7C211E
    1815: (143, 86, 82), #8F5652
    1817: (91, 45, 40), #5B2D28
    182: (249, 191, 193), #F9BFC1
    183: (252, 140, 153), #FC8C99
    184: (252, 94, 114), #FC5E72
    185: (232, 17, 45), #E8112D

    185.2: (209, 22, 0), #D11600
    186: (206, 17, 38), #CE1126
    187: (175, 30, 45), #AF1E2D
    188: (124, 33, 40), #7C2128
    189: (255, 163, 178), #FFA3B2
    1895: (252, 191, 201), #FCBFC9

    190: (252, 117, 142), #FC758E
    1905: (252, 155, 178), #FC9BB2
    191: (244, 71, 107), #F4476B
    1915: (244, 84, 124), #F4547C
    192: (229, 5, 58), #E5053A
    1925: (224, 7, 71), #E00747

    193: (196, 0, 67), #C40043
    1935: (193, 5, 56), #C10538
    194: (153, 33, 53), #992135
    1945: (168, 12, 53), #A80C35
    1955: (147, 22, 56), #931638
    195: (117, 41, 54), #752936
    196: (250, 213, 225), #FAD5E1

    197: (246, 165, 190), #F6A5BE
    198: (239, 91, 132), #EF5B84
    199: (160, 39, 75), #A0274B

    200: (196, 30, 58), #C41E3A
    201: (163, 38, 56), #A32638
    202: (140, 38, 51), #8C2633
    203: (242, 175, 193), #F2AFC1
    204: (237, 122, 158), #ED7A9E

    205: (229, 76, 124), #E54C7C
    206: (211, 5, 71), #D30547
    207: (192, 0, 78), #C0004E
    208: (142, 35, 68), #8E2344
    209: (117, 38, 61), #75263D
    210: (255, 160, 191), #FFA0BF

    211: (255, 119, 168), #FF77A8
    212: (249, 79, 142), #F94F8E
    213: (234, 15, 107), #EA0F6B
    214: (204, 2, 86), #CC0256
    215: (165, 5, 68), #A50544
    216: (124, 30, 63), #7C1E3F

    217: (244, 191, 209), #F4BFD1
    218: (237, 114, 170), #ED72AA
    219: (226, 40, 130), #E22882
    220: (170, 0, 79), #AA004F
    221: (147, 0, 66), #930042
    222: (112, 25, 61), #70193D

    223: (249, 147, 196), #F993C4
    224: (244, 107, 175), #F46BAF
    225: (237, 40, 147), #ED2893
    226: (214, 2, 112), #D60270
    227: (173, 0, 91), #AD005B
    228: (140, 0, 76), #8C004C

    229: (109, 33, 63), #6D213F
    230: (255, 160, 204), #FFA0CC
    231: (252, 112, 186), #FC70BA
    232: (244, 63, 165), #F43FA5
    233: (206, 0, 124), #CE007C
    234: (170, 0, 102), #AA0066

    235: (142, 5, 84), #8E0554
    236: (249, 175, 211), #F9AFD3
    2365: (247, 196, 216), #F7C4D8
    237: (244, 132, 196), #F484C4
    2375: (234, 107, 191), #EA6BBF
    238: (237, 79, 175), #ED4FAF

    2385: (219, 40, 165), #DB28A5
    239: (224, 33, 158), #E0219E
    2395: (196, 0, 140), #C4008C
    240: (196, 15, 137), #C40F89
    2405: (168, 0, 122), #A8007A
    241: (173, 0, 117), #AD0075

    2415: (155, 0, 112), #9B0070
    242: (124, 28, 81), #7C1C51
    2425: (135, 0, 91), #87005B
    243: (242, 186, 216), #F2BAD8
    244: (237, 160, 211), #EDA0D3
    245: (232, 127, 201), #E87FC9

    246: (204, 0, 160), #CC00A0
    247: (183, 0, 142), #B7008E
    248: (163, 5, 127), #A3057F
    249: (127, 40, 96), #7F2860
    250: (237, 196, 221), #EDC4DD
    251: (226, 158, 214), #E29ED6

    252: (211, 107, 198), #D36BC6
    253: (175, 35, 165), #AF23A5
    254: (160, 45, 150), #A02D96
    255: (119, 45, 107), #772D6B
    256: (229, 196, 214), #E5C4D6
    2562: (216, 168, 216), #D8A8D8

    2563: (209, 160, 204), #D1A0CC
    2567: (191, 147, 204), #BF93CC
    257: (211, 165, 201), #D3A5C9
    2572: (198, 135, 209), #C687D1
    2573: (186, 124, 188), #BA7CBC
    2577: (170, 114, 191), #AA72BF

    258: (155, 79, 150), #9B4F96
    2582: (170, 71, 186), #AA47BA
    2583: (158, 79, 165), #9E4FA5
    2587: (142, 71, 173), #8E47AD
    259: (114, 22, 107), #72166B
    2592: (147, 15, 165), #930FA5

    2593: (135, 43, 147), #872B93
    2597: (102, 0, 140), #66008C
    260: (104, 30, 91), #681E5B
    2602: (130, 12, 142), #820C8E
    2603: (112, 20, 122), #70147A
    2607: (91, 2, 122), #5B027A

    261: (94, 33, 84), #5E2154
    2612: (112, 30, 114), #701E72
    2613: (102, 17, 109), #66116D
    2617: (86, 12, 112), #560C70
    262: (84, 35, 68), #542344
    2622: (96, 45, 89), #602D59

    2623: (91, 25, 94), #5B195E
    2627: (76, 20, 94), #4C145E
    263: (224, 206, 224), #E0CEE0
    2635: (201, 173, 216), #C9ADD8
    264: (198, 170, 219), #C6AADB
    2645: (181, 145, 209), #B591D1

    265: (150, 99, 196), #9663C4
    2655: (155, 109, 198), #9B6DC6
    266: (109, 40, 170), #6D28AA
    2665: (137, 79, 191), #894FBF
    267: (89, 17, 142), #59118E
    268: (79, 33, 112), #4F2170

    2685: (86, 0, 140), #56008C
    269: (68, 35, 89), #442359
    2695: (68, 35, 94), #44235E
    270: (186, 175, 211), #BAAFD3
    2705: (173, 158, 211), #AD9ED3
    2706: (209, 206, 221), #D1CEDD

    2707: (191, 209, 229), #BFD1E5
    2708: (175, 188, 219), #AFBCDB
    271: (158, 145, 198), #9E91C6
    2715: (147, 122, 204), #937ACC
    2716: (165, 160, 214), #A5A0D6
    2717: (165, 186, 224), #A5BAE0

    2718: (91, 119, 204), #5B77CC
    272: (137, 119, 186), #8977BA
    2725: (114, 81, 188), #7251BC
    2726: (102, 86, 188), #6656BC
    2727: (94, 104, 196), #5E68C4
    2728: (48, 68, 181), #3044B5

    273: (56, 25, 122), #38197A
    2735: (79, 0, 147), #4F0093
    2736: (73, 48, 173), #4930AD
    2738: (45, 0, 142), #2D008E
    274: (43, 17, 102), #2B1166
    2745: (63, 0, 119), #3F0077

    2746: (63, 40, 147), #3F2893
    2747: (28, 20, 107), #1C146B
    2748: (30, 28, 119), #1E1C77
    275: (38, 15, 84), #260F54
    2755: (53, 0, 109), #35006D
    2756: (51, 40, 117), #332875

    2757: (20, 22, 84), #141654
    2758: (25, 33, 104), #192168
    276: (43, 33, 71), #2B2147
    2765: (43, 12, 86), #2B0C56
    2766: (43, 38, 91), #2B265B
    2767: (20, 33, 61), #14213D

    2768: (17, 33, 81), #112151
    277: (181, 209, 232), #B5D1E8
    278: (153, 186, 221), #99BADD
    279: (102, 137, 204), #6689CC
    280: (0, 43, 127), #002B7F
    281: (0, 40, 104), #002868

    282: (0, 38, 84), #002654
    283: (155, 196, 226), #9BC4E2
    284: (117, 170, 219), #75AADB
    285: (58, 117, 196), #3A75C4
    286: (0, 56, 168), #0038A8
    287: (0, 56, 147), #003893

    288: (0, 51, 127), #00337F
    289: (0, 38, 73), #002649
    290: (196, 216, 226), #C4D8E2
    2905: (147, 198, 224), #93C6E0
    291: (168, 206, 226), #A8CEE2
    2915: (96, 175, 221), #60AFDD

    292: (117, 178, 221), #75B2DD
    2925: (0, 142, 214), #008ED6
    293: (0, 81, 186), #0051BA
    2935: (0, 91, 191), #005BBF
    294: (0, 63, 135), #003F87
    2945: (0, 84, 160), #0054A0

    295: (0, 56, 107), #00386B
    2955: (0, 61, 107), #003D6B
    296: (0, 45, 71), #002D47
    2965: (0, 51, 76), #00334C
    297: (130, 198, 226), #82C6E2
    2975: (186, 224, 226), #BAE0E2

    298: (81, 181, 224), #51B5E0
    2985: (81, 191, 226), #51BFE2
    299: (0, 163, 221), #00A3DD
    2995: (0, 165, 219), #00A5DB

    300: (0, 114, 198), #0072C6
    3005: (0, 132, 201), #0084C9
    301: (0, 91, 153), #005B99
    3015: (0, 112, 158), #00709E
    302: (0, 79, 109), #004F6D

    3025: (0, 84, 107), #00546B
    303: (0, 63, 84), #003F54
    3035: (0, 68, 84), #004454
    304: (165, 221, 226), #A5DDE2
    305: (112, 206, 226), #70CEE2
    306: (0, 188, 226), #00BCE2

    306.2: (0, 163, 209), #00A3D1
    307: (0, 122, 165), #007AA5
    308: (0, 96, 124), #00607C
    309: (0, 63, 73), #003F49
    310: (114, 209, 221), #72D1DD
    3105: (127, 214, 219), #7FD6DB

    311: (40, 196, 216), #28C4D8
    3115: (45, 198, 214), #2DC6D6
    312: (0, 173, 198), #00ADC6
    3125: (0, 183, 198), #00B7C6
    313: (0, 153, 181), #0099B5
    3135: (0, 155, 170), #009BAA

    314: (0, 130, 155), #00829B
    3145: (0, 132, 142), #00848E
    315: (0, 107, 119), #006B77
    3155: (0, 109, 117), #006D75
    316: (0, 73, 79), #00494F
    3165: (0, 86, 91), #00565B

    317: (201, 232, 221), #C9E8DD
    318: (147, 221, 219), #93DDDB
    319: (76, 206, 209), #4CCED1
    320: (0, 158, 160), #009EA0
    320.2: (0, 127, 130), #007F82
    321: (0, 135, 137), #008789

    322: (0, 114, 114), #007272
    323: (0, 102, 99), #006663
    324: (170, 221, 214), #AADDD6
    3242: (135, 221, 209), #87DDD1
    3245: (140, 224, 209), #8CE0D1
    3248: (122, 211, 193), #7AD3C1

    325: (86, 201, 193), #56C9C1
    3252: (86, 214, 201), #56D6C9
    3255: (71, 214, 193), #47D6C1
    3258: (53, 196, 175), #35C4AF
    326: (0, 178, 170), #00B2AA
    3262: (0, 193, 181), #00C1B5

    3265: (0, 198, 178), #00C6B2
    3268: (0, 175, 153), #00AF99
    327: (0, 140, 130), #008C82
    327.2: (0, 137, 119), #008977
    3272: (0, 170, 158), #00AA9E
    3275: (0, 178, 160), #00B2A0

    3278: (0, 155, 132), #009B84
    328: (0, 119, 112), #007770
    3282: (0, 140, 130), #008C82
    3285: (0, 153, 135), #009987
    3288: (0, 130, 112), #008270
    329: (0, 109, 102), #006D66

    3292: (0, 96, 86), #006056
    3295: (0, 130, 114), #008272
    3298: (0, 107, 91), #006B5B
    330: (0, 89, 81), #005951
    3302: (0, 73, 63), #00493F
    3305: (0, 79, 66), #004F42

    3308: (0, 68, 56), #004438
    331: (186, 234, 214), #BAEAD6
    332: (160, 229, 206), #A0E5CE
    333: (94, 221, 193), #5EDDC1
    334: (0, 153, 124), #00997C
    335: (0, 124, 102), #007C66

    336: (0, 104, 84), #006854
    337: (155, 219, 193), #9BDBC1
    3375: (142, 226, 188), #8EE2BC
    338: (122, 209, 181), #7AD1B5
    3385: (84, 216, 168), #54D8A8
    339: (0, 178, 140), #00B28C

    3395: (0, 201, 147), #00C993
    340: (0, 153, 119), #009977
    3405: (0, 178, 122), #00B27A
    341: (0, 122, 94), #007A5E
    3415: (0, 124, 89), #007C59
    342: (0, 107, 84), #006B54

    3425: (0, 104, 71), #006847
    343: (0, 86, 63), #00563F
    3435: (2, 73, 48), #024930
    344: (181, 226, 191), #B5E2BF
    345: (150, 216, 175), #96D8AF
    346: (112, 206, 155), #70CE9B

    347: (0, 158, 96), #009E60
    348: (0, 135, 81), #008751
    349: (0, 107, 63), #006B3F
    350: (35, 79, 51), #234F33
    351: (181, 232, 191), #B5E8BF
    352: (153, 229, 178), #99E5B2

    353: (132, 226, 168), #84E2A8
    354: (0, 183, 96), #00B760
    355: (0, 158, 73), #009E49
    356: (0, 122, 61), #007A3D
    357: (33, 91, 51), #215B33
    358: (170, 221, 150), #AADD96

    359: (160, 219, 142), #A0DB8E
    360: (96, 198, 89), #60C659
    361: (30, 181, 58), #1EB53A
    362: (51, 158, 53), #339E35
    363: (61, 142, 51), #3D8E33
    364: (58, 119, 40), #3A7728

    365: (211, 232, 163), #D3E8A3
    366: (196, 229, 142), #C4E58E
    367: (170, 221, 109), #AADD6D
    368: (91, 191, 33), #5BBF21
    3682: (0, 158, 15), #009E0F
    369: (86, 170, 28), #56AA1C

    370: (86, 142, 20), #568E14
    371: (86, 107, 33), #566B21
    372: (216, 237, 150), #D8ED96
    373: (206, 234, 130), #CEEA82
    374: (186, 232, 96), #BAE860
    375: (140, 214, 0), #8CD600

    375.2: (84, 188, 0), #54BC00
    376: (127, 186, 0), #7FBA00
    377: (112, 147, 2), #709302
    378: (86, 99, 20), #566314
    379: (224, 234, 104), #E0EA68
    380: (214, 229, 66), #D6E542

    381: (204, 226, 38), #CCE226
    382: (186, 216, 10), #BAD80A
    3822: (158, 196, 0), #9EC400
    383: (163, 175, 7), #A3AF07
    384: (147, 153, 5), #939905
    385: (112, 112, 20), #707014

    386: (232, 237, 96), #E8ED60
    387: (224, 237, 68), #E0ED44
    388: (214, 232, 15), #D6E80F
    389: (206, 224, 7), #CEE007
    390: (186, 196, 5), #BAC405
    391: (158, 158, 7), #9E9E07

    392: (132, 130, 5), #848205
    393: (242, 239, 135), #F2EF87
    3935: (242, 237, 109), #F2ED6D
    394: (234, 237, 53), #EAED35
    3945: (239, 234, 7), #EFEA07
    395: (229, 232, 17), #E5E811

    3955: (237, 226, 17), #EDE211
    396: (224, 226, 12), #E0E20C
    3965: (232, 221, 17), #E8DD11
    397: (193, 191, 10), #C1BF0A
    3975: (181, 168, 12), #B5A80C
    398: (175, 168, 10), #AFA80A

    3985: (153, 140, 10), #998C0A
    399: (153, 142, 7), #998E07
    3995: (109, 96, 2), #6D6002

    400: (209, 198, 181), #D1C6B5
    401: (193, 181, 165), #C1B5A5
    402: (175, 165, 147), #AFA593
    403: (153, 140, 124), #998C7C
    404: (130, 117, 102), #827566

    405: (107, 94, 79), #6B5E4F
    406: (206, 193, 181), #CEC1B5
    408: (168, 153, 140), #A8998C
    409: (153, 137, 124), #99897C
    410: (124, 109, 99), #7C6D63
    411: (102, 89, 76), #66594C

    412: (61, 48, 40), #3D3028
    413: (198, 193, 178), #C6C1B2
    414: (181, 175, 160), #B5AFA0
    415: (163, 158, 140), #A39E8C
    416: (142, 140, 122), #8E8C7A
    417: (119, 114, 99), #777263

    418: (96, 94, 79), #605E4F
    419: (40, 40, 33), #282821
    420: (209, 204, 191), #D1CCBF
    421: (191, 186, 175), #BFBAAF
    422: (175, 170, 163), #AFAAA3
    423: (150, 147, 142), #96938E

    424: (130, 127, 119), #827F77
    425: (96, 96, 91), #60605B
    426: (43, 43, 40), #2B2B28
    427: (221, 219, 209), #DDDBD1
    428: (209, 206, 198), #D1CEC6
    429: (173, 175, 170), #ADAFAA

    430: (145, 150, 147), #919693
    431: (102, 109, 112), #666D70
    432: (68, 79, 81), #444F51
    433: (48, 56, 58), #30383A
    433.2: (10, 12, 17), #0A0C11
    434: (224, 209, 198), #E0D1C6

    435: (211, 191, 183), #D3BFB7
    436: (188, 165, 158), #BCA59E
    437: (140, 112, 107), #8C706B
    438: (89, 63, 61), #593F3D
    439: (73, 53, 51), #493533
    440: (63, 48, 43), #3F302B

    441: (209, 209, 198), #D1D1C6
    442: (186, 191, 183), #BABFB7
    443: (163, 168, 163), #A3A8A3
    444: (137, 142, 140), #898E8C
    445: (86, 89, 89), #565959
    446: (73, 76, 73), #494C49

    447: (63, 63, 56), #3F3F38
    448: (84, 71, 45), #54472D
    4485: (96, 76, 17), #604C11
    449: (84, 71, 38), #544726
    4495: (135, 117, 48), #877530
    450: (96, 84, 43), #60542B

    4505: (160, 145, 81), #A09151
    451: (173, 160, 122), #ADA07A
    4515: (188, 173, 117), #BCAD75
    452: (196, 183, 150), #C4B796
    4525: (204, 191, 142), #CCBF8E
    453: (214, 204, 175), #D6CCAF

    4535: (219, 206, 165), #DBCEA5
    454: (226, 216, 191), #E2D8BF
    4545: (229, 219, 186), #E5DBBA
    455: (102, 86, 20), #665614
    456: (153, 135, 20), #998714
    457: (181, 155, 12), #B59B0C

    458: (221, 204, 107), #DDCC6B
    459: (226, 214, 124), #E2D67C
    460: (234, 221, 150), #EADD96
    461: (237, 229, 173), #EDE5AD
    462: (91, 71, 35), #5B4723
    4625: (71, 35, 17), #472311

    463: (117, 84, 38), #755426
    4635: (140, 89, 51), #8C5933
    464: (135, 96, 40), #876028
    464.2: (112, 66, 20), #704214
    4645: (178, 130, 96), #B28260
    465: (193, 168, 117), #C1A875

    4655: (196, 153, 119), #C49977
    466: (209, 191, 145), #D1BF91
    4665: (216, 181, 150), #D8B596
    467: (221, 204, 165), #DDCCA5
    4675: (229, 198, 170), #E5C6AA
    468: (226, 214, 181), #E2D6B5

    4685: (237, 211, 188), #EDD3BC
    469: (96, 51, 17), #603311
    4695: (81, 38, 28), #51261C
    470: (155, 79, 25), #9B4F19
    4705: (124, 81, 61), #7C513D
    471: (188, 94, 30), #BC5E1E

    471.2: (163, 68, 2), #A34402
    4715: (153, 112, 91), #99705B
    472: (234, 170, 122), #EAAA7A
    4725: (181, 145, 124), #B5917C
    473: (244, 196, 160), #F4C4A0
    4735: (204, 175, 155), #CCAF9B

    474: (244, 204, 170), #F4CCAA
    4745: (216, 191, 170), #D8BFAA
    475: (247, 211, 181), #F7D3B5
    4755: (226, 204, 186), #E2CCBA
    476: (89, 61, 43), #593D2B
    477: (99, 56, 38), #633826

    478: (122, 63, 40), #7A3F28
    479: (175, 137, 112), #AF8970
    480: (211, 183, 163), #D3B7A3
    481: (224, 204, 186), #E0CCBA
    482: (229, 211, 193), #E5D3C1
    483: (107, 48, 33), #6B3021

    484: (155, 48, 28), #9B301C
    485: (216, 30, 5), #D81E05
    4852: (204, 12, 0), #CC0C00
    486: (237, 158, 132), #ED9E84
    487: (239, 181, 160), #EFB5A0
    488: (242, 196, 175), #F2C4AF

    489: (242, 209, 191), #F2D1BF
    490: (91, 38, 38), #5B2626
    491: (117, 40, 40), #752828
    492: (145, 51, 56), #913338
    494: (242, 173, 178), #F2ADB2
    495: (244, 188, 191), #F4BCBF

    496: (247, 201, 198), #F7C9C6
    497: (81, 40, 38), #512826
    4975: (68, 30, 28), #441E1C
    498: (109, 51, 43), #6D332B
    4985: (132, 73, 73), #844949
    499: (122, 56, 45), #7A382D

    4995: (165, 107, 109), #A56B6D

    500: (206, 137, 140), #CE898C
    5005: (188, 135, 135), #BC8787
    501: (234, 178, 178), #EAB2B2
    5015: (216, 173, 168), #D8ADA8
    502: (242, 198, 196), #F2C6C4

    5025: (226, 188, 183), #E2BCB7
    503: (244, 209, 204), #F4D1CC
    5035: (237, 206, 198), #EDCEC6
    504: (81, 30, 38), #511E26
    505: (102, 30, 43), #661E2B
    506: (122, 38, 56), #7A2638

    507: (216, 137, 155), #D8899B
    508: (232, 165, 175), #E8A5AF
    509: (242, 186, 191), #F2BABF
    510: (244, 198, 201), #F4C6C9
    511: (96, 33, 68), #602144
    5115: (79, 33, 58), #4F213A

    512: (132, 33, 107), #84216B
    5125: (117, 71, 96), #754760
    513: (158, 35, 135), #9E2387
    5135: (147, 107, 127), #936B7F
    514: (216, 132, 188), #D884BC
    5145: (173, 135, 153), #AD8799

    515: (232, 163, 201), #E8A3C9
    5155: (204, 175, 183), #CCAFB7
    516: (242, 186, 211), #F2BAD3
    5165: (224, 201, 204), #E0C9CC
    517: (244, 204, 216), #F4CCD8
    5175: (232, 214, 209), #E8D6D1

    518: (81, 45, 68), #512D44
    5185: (71, 40, 53), #472835
    519: (99, 48, 94), #63305E
    5195: (89, 51, 68), #593344
    520: (112, 53, 114), #703572
    5205: (142, 104, 119), #8E6877

    521: (181, 140, 178), #B58CB2
    5215: (181, 147, 155), #B5939B
    522: (198, 163, 193), #C6A3C1
    5225: (204, 173, 175), #CCADAF
    523: (211, 183, 204), #D3B7CC
    5235: (221, 198, 196), #DDC6C4

    524: (226, 204, 211), #E2CCD3
    5245: (229, 211, 204), #E5D3CC
    525: (81, 38, 84), #512654
    5255: (53, 38, 79), #35264F
    526: (104, 33, 122), #68217A
    5265: (73, 61, 99), #493D63

    527: (122, 30, 153), #7A1E99
    5275: (96, 86, 119), #605677
    528: (175, 114, 193), #AF72C1
    5285: (140, 130, 153), #8C8299
    529: (206, 163, 211), #CEA3D3
    5295: (178, 168, 181), #B2A8B5

    530: (214, 175, 214), #D6AFD6
    5305: (204, 193, 198), #CCC1C6
    531: (229, 198, 219), #E5C6DB
    5315: (219, 211, 211), #DBD3D3
    532: (53, 56, 66), #353842
    533: (53, 63, 91), #353F5B

    534: (58, 73, 114), #3A4972
    535: (155, 163, 183), #9BA3B7
    536: (173, 178, 193), #ADB2C1
    537: (196, 198, 206), #C4C6CE
    538: (214, 211, 214), #D6D3D6
    539: (0, 48, 73), #003049

    5395: (2, 40, 58), #02283A
    540: (0, 51, 91), #00335B
    5405: (63, 96, 117), #3F6075
    541: (0, 63, 119), #003F77
    5415: (96, 124, 140), #607C8C
    542: (102, 147, 188), #6693BC

    5425: (132, 153, 165), #8499A5
    543: (147, 183, 209), #93B7D1
    5435: (175, 188, 191), #AFBCBF
    544: (183, 204, 219), #B7CCDB
    5445: (196, 204, 204), #C4CCCC
    545: (196, 211, 221), #C4D3DD

    5455: (214, 216, 211), #D6D8D3
    546: (12, 56, 68), #0C3844
    5463: (0, 53, 58), #00353A
    5467: (25, 56, 51), #193833
    547: (0, 63, 84), #003F54
    5473: (38, 104, 109), #26686D

    5477: (58, 86, 79), #3A564F
    548: (0, 68, 89), #004459
    5483: (96, 145, 145), #609191
    5487: (102, 124, 114), #667C72
    549: (94, 153, 170), #5E99AA
    5493: (140, 175, 173), #8CAFAD

    5497: (145, 163, 153), #91A399
    550: (135, 175, 191), #87AFBF
    5503: (170, 196, 191), #AAC4BF
    5507: (175, 186, 178), #AFBAB2
    551: (163, 193, 201), #A3C1C9
    5513: (206, 216, 209), #CED8D1

    5517: (201, 206, 196), #C9CEC4
    552: (196, 214, 214), #C4D6D6
    5523: (214, 221, 214), #D6DDD6
    5527: (206, 209, 198), #CED1C6
    553: (35, 68, 53), #234435
    5535: (33, 61, 48), #213D30

    554: (25, 94, 71), #195E47
    5545: (79, 109, 94), #4F6D5E
    555: (7, 109, 84), #076D54
    5555: (119, 145, 130), #779182
    556: (122, 168, 145), #7AA891
    5565: (150, 170, 153), #96AA99

    557: (163, 193, 173), #A3C1AD
    5575: (175, 191, 173), #AFBFAD
    558: (183, 206, 188), #B7CEBC
    5585: (196, 206, 191), #C4CEBF
    559: (198, 214, 196), #C6D6C4
    5595: (216, 219, 204), #D8DBCC

    560: (43, 76, 63), #2B4C3F
    5605: (35, 58, 45), #233A2D
    561: (38, 102, 89), #266659
    5615: (84, 104, 86), #546856
    562: (30, 122, 109), #1E7A6D
    5625: (114, 132, 112), #728470

    563: (127, 188, 170), #7FBCAA
    5635: (158, 170, 153), #9EAA99
    564: (5, 112, 94), #05705E
    5645: (188, 193, 178), #BCC1B2
    565: (188, 219, 204), #BCDBCC
    5655: (198, 204, 186), #C6CCBA

    566: (209, 226, 211), #D1E2D3
    5665: (214, 214, 198), #D6D6C6
    567: (38, 81, 66), #265142
    568: (0, 114, 99), #007263
    569: (0, 135, 114), #008772
    570: (127, 198, 178), #7FC6B2

    571: (170, 219, 198), #AADBC6
    572: (188, 226, 206), #BCE2CE
    573: (204, 229, 214), #CCE5D6
    574: (73, 89, 40), #495928
    5743: (63, 73, 38), #3F4926
    5747: (66, 71, 22), #424716

    575: (84, 119, 48), #547730
    5753: (94, 102, 58), #5E663A
    5757: (107, 112, 43), #6B702B
    576: (96, 142, 58), #608E3A
    5763: (119, 124, 79), #777C4F
    5767: (140, 145, 79), #8C914F

    577: (181, 204, 142), #B5CC8E
    5773: (155, 158, 114), #9B9E72
    5777: (170, 173, 117), #AAAD75
    578: (198, 214, 160), #C6D6A0
    5783: (181, 181, 142), #B5B58E
    5787: (198, 198, 153), #C6C699

    579: (201, 214, 163), #C9D6A3
    5793: (198, 198, 165), #C6C6A5
    5797: (211, 209, 170), #D3D1AA
    580: (216, 221, 181), #D8DDB5
    5803: (216, 214, 183), #D8D6B7
    5807: (224, 221, 188), #E0DDBC

    581: (96, 94, 17), #605E11
    5815: (73, 68, 17), #494411
    582: (135, 137, 5), #878905
    5825: (117, 112, 43), #75702B
    583: (170, 186, 10), #AABA0A
    5835: (158, 153, 89), #9E9959

    584: (206, 214, 73), #CED649
    5845: (178, 170, 112), #B2AA70
    585: (219, 224, 107), #DBE06B
    5855: (204, 198, 147), #CCC693
    586: (226, 229, 132), #E2E584
    5865: (214, 206, 163), #D6CEA3

    587: (232, 232, 155), #E8E89B
    5875: (224, 219, 181), #E0DBB5

    600: (244, 237, 175), #F4EDAF
    601: (242, 237, 158), #F2ED9E
    602: (242, 234, 135), #F2EA87
    603: (237, 232, 91), #EDE85B
    604: (232, 221, 33), #E8DD21

    605: (221, 206, 17), #DDCE11
    606: (211, 191, 17), #D3BF11
    607: (242, 234, 188), #F2EABC
    608: (239, 232, 173), #EFE8AD
    609: (234, 229, 150), #EAE596
    610: (226, 219, 114), #E2DB72

    611: (214, 206, 73), #D6CE49
    612: (196, 186, 0), #C4BA00
    613: (175, 160, 12), #AFA00C
    614: (234, 226, 183), #EAE2B7
    615: (226, 219, 170), #E2DBAA
    616: (221, 214, 155), #DDD69B

    617: (204, 196, 124), #CCC47C
    618: (181, 170, 89), #B5AA59
    619: (150, 140, 40), #968C28
    620: (132, 119, 17), #847711
    621: (216, 221, 206), #D8DDCE
    622: (193, 209, 191), #C1D1BF

    623: (165, 191, 170), #A5BFAA
    624: (127, 160, 140), #7FA08C
    625: (91, 135, 114), #5B8772
    626: (33, 84, 63), #21543F
    627: (12, 48, 38), #0C3026
    628: (204, 226, 221), #CCE2DD

    629: (178, 216, 216), #B2D8D8
    630: (140, 204, 211), #8CCCD3
    631: (84, 183, 198), #54B7C6
    632: (0, 160, 186), #00A0BA
    633: (0, 127, 153), #007F99
    634: (0, 102, 127), #00667F

    635: (186, 224, 224), #BAE0E0
    636: (153, 214, 221), #99D6DD
    637: (107, 201, 219), #6BC9DB
    638: (0, 181, 214), #00B5D6
    639: (0, 160, 196), #00A0C4
    640: (0, 140, 178), #008CB2

    641: (0, 122, 165), #007AA5
    642: (209, 216, 216), #D1D8D8
    643: (198, 209, 214), #C6D1D6
    644: (155, 175, 196), #9BAFC4
    645: (119, 150, 178), #7796B2
    646: (94, 130, 163), #5E82A3

    647: (38, 84, 124), #26547C
    648: (0, 48, 94), #00305E
    649: (214, 214, 216), #D6D6D8
    650: (191, 198, 209), #BFC6D1
    651: (155, 170, 191), #9BAABF
    652: (109, 135, 168), #6D87A8

    653: (51, 86, 135), #335687
    654: (15, 43, 91), #0F2B5B
    655: (12, 28, 71), #0C1C47
    656: (214, 219, 224), #D6DBE0
    657: (193, 201, 221), #C1C9DD
    658: (165, 175, 214), #A5AFD6

    659: (127, 140, 191), #7F8CBF
    660: (89, 96, 168), #5960A8
    661: (45, 51, 142), #2D338E
    662: (12, 25, 117), #0C1975
    663: (226, 211, 214), #E2D3D6
    664: (216, 204, 209), #D8CCD1

    665: (198, 181, 196), #C6B5C4
    666: (168, 147, 173), #A893AD
    667: (127, 102, 137), #7F6689
    668: (102, 73, 117), #664975
    669: (71, 43, 89), #472B59
    670: (242, 214, 216), #F2D6D8

    671: (239, 198, 211), #EFC6D3
    672: (234, 170, 196), #EAAAC4
    673: (224, 140, 178), #E08CB2
    674: (211, 107, 158), #D36B9E
    675: (188, 56, 119), #BC3877
    676: (160, 0, 84), #A00054

    677: (237, 214, 214), #EDD6D6
    678: (234, 204, 206), #EACCCE
    679: (229, 191, 198), #E5BFC6
    680: (211, 158, 175), #D39EAF
    681: (183, 114, 142), #B7728E
    682: (160, 81, 117), #A05175

    683: (127, 40, 79), #7F284F
    684: (239, 204, 206), #EFCCCE
    685: (234, 191, 196), #EABFC4
    686: (224, 170, 186), #E0AABA
    687: (201, 137, 158), #C9899E
    688: (178, 102, 132), #B26684

    689: (147, 66, 102), #934266
    690: (112, 35, 66), #702342
    691: (239, 209, 201), #EFD1C9
    692: (232, 191, 186), #E8BFBA
    693: (219, 168, 165), #DBA8A5
    694: (201, 140, 140), #C98C8C

    695: (178, 107, 112), #B26B70
    696: (142, 71, 73), #8E4749
    697: (127, 56, 58), #7F383A
    698: (247, 209, 204), #F7D1CC
    699: (247, 191, 191), #F7BFBF

    700: (242, 165, 170), #F2A5AA
    701: (232, 135, 142), #E8878E
    702: (214, 96, 109), #D6606D
    703: (183, 56, 68), #B73844
    704: (158, 40, 40), #9E2828

    705: (249, 221, 214), #F9DDD6
    706: (252, 201, 198), #FCC9C6
    707: (252, 173, 175), #FCADAF
    708: (249, 142, 153), #F98E99
    709: (242, 104, 119), #F26877
    710: (224, 66, 81), #E04251

    711: (209, 45, 51), #D12D33
    712: (255, 211, 170), #FFD3AA
    713: (249, 201, 163), #F9C9A3
    714: (249, 186, 130), #F9BA82
    715: (252, 158, 73), #FC9E49
    716: (242, 132, 17), #F28411

    717: (211, 109, 0), #D36D00
    718: (191, 91, 0), #BF5B00
    719: (244, 209, 175), #F4D1AF
    720: (239, 196, 158), #EFC49E
    721: (232, 178, 130), #E8B282
    722: (209, 142, 84), #D18E54

    723: (186, 117, 48), #BA7530
    724: (142, 73, 5), #8E4905
    725: (117, 56, 2), #753802
    726: (237, 211, 181), #EDD3B5
    727: (226, 191, 155), #E2BF9B
    728: (211, 168, 124), #D3A87C

    729: (193, 142, 96), #C18E60
    730: (170, 117, 63), #AA753F
    731: (114, 63, 10), #723F0A
    732: (96, 51, 10), #60330A
    801: (0, 170, 204), #00AACC
    801.2: (0, 137, 175), #0089AF
    802: (96, 221, 73), #60DD49
    802.2: (28, 206, 40), #1CCE28
    803: (255, 237, 56), #FFED38

    803.2: (255, 216, 22), #FFD816
    804: (255, 147, 56), #FF9338
    804.2: (255, 127, 30), #FF7F1E
    805: (249, 89, 81), #F95951
    805.2: (249, 58, 43), #F93A2B
    806: (255, 0, 147), #FF0093

    806.2: (247, 2, 124), #F7027C
    807: (214, 0, 158), #D6009E
    807.2: (191, 0, 140), #BF008C
    808: (0, 181, 155), #00B59B
    808.2: (0, 160, 135), #00A087
    809: (221, 224, 15), #DDE00F

    809.2: (214, 214, 12), #D6D60C
    810: (255, 204, 30), #FFCC1E
    810.2: (255, 188, 33), #FFBC21
    811: (255, 114, 71), #FF7247
    811.2: (255, 84, 22), #FF5416
    812: (252, 35, 102), #FC2366

    812.2: (252, 7, 79), #FC074F
    813: (229, 0, 153), #E50099
    813.2: (209, 0, 132), #D10084
    814: (140, 96, 193), #8C60C1
    814.2: (112, 63, 175), #703FAF

    877: (138, 141, 143),
    '877c': (138, 141, 143),
    '877u': (180, 183, 185),
}

# Replace integers by float numbers.
for spot, (r, g, b) in SPOT_RGB.items():
    SPOT_RGB[spot] = r/255, g/255, b/255

if __name__ == '__main__':
    import doctest
    doctest.testmod()

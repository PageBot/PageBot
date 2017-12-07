from pagebot.fonttoolbox.objects.font import Font, getFontByName

path = '/Users/petr/fonts/_instances/AmstelvarAlpha-VF-GRAD94.9084751948.ttf'
path = '/Users/petr/fonts/_instances/AmstelvarAlpha-Default.ttf'

f = Font(path)

S = u'Ae'

fs = FormattedString(S, font=f.installedName, fontSize=500)
textBox(fs, (20, -10, 900, 900))


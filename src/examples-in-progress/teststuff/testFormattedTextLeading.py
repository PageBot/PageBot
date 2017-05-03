from pagebot.style import getRootStyle
from pagebot import getFormattedString

rs = getRootStyle()
rs['leading'] = 10
rs['fontSize'] = 9
rs['font'] = 'Verdana'
fs = getFormattedString('aaa', None, rs)

a = FormattedString('', lineHeight=rs['leading'], fontSize=rs['fontSize'], font='Verdana')
for n in range(100):
    a += 'AAA%s\n' % n
    fs += 'RS%s\n' % n
    fs += FormattedString('SSSS', fontSize=18, lineHeight=20)
    fs += FormattedString('DDDD\n', fontSize=9, lineHeight=10)
    stroke(0)
    strokeWidth(0.5)
    line((10, n*rs['leading']), (500, n*rs['leading']))

print textBox(a, (10, 10, 300, 800))
print textBox(fs, (320, 10, 300, 800))


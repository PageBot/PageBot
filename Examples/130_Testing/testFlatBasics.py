
# Only runs under Flat
from flat import rgb, font, shape, strike, document
from pagebot.fonttoolbox.objects.font import findFont

f = findFont('Roboto-Bold')
print(f)
print(f.path)
c = rgb(255, 0, 0)
ff = font.open(f.path)
print(ff)
figure = shape().stroke(c).width(2.5)
headline = strike(ff).color(c).size(80, 96)
d = document(400, 200, 'mm')
p = d.addpage()
p.place(figure.circle(50, 50, 20))
t = headline.text(u'Hello world! AVT.TeYAYeYé')
#p.place(t).frame(10, 10, 380, 80)
'''
im = p.image(kind='rgb')
im.png('_export/hello.png')
im.jpeg('_export/hello.jpg')
p.svg('_export/hello.svg')
d.pdf('_export/hello.pdf')
'''
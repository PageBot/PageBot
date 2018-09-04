 # Only runs under Flat
from flat import rgb, font, shape, strike, document
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.contexts.platform import getContext
from pagebot.toolbox.color import blackColor
from pagebot import getResourcesPath
import os, os.path

WIDTH = 400
HEIGHT = 200

f = findFont('Roboto-Bold')

#print(f)j
#print(f.path)
c = rgb(255, 0, 0)

# Flat font.
ff = font.open(f.path)
#print(ff.name)
#print(ff)
binary = bytes(ff.source.embed())
#print(type(binary))

figure = shape().stroke(c).width(2.5)
headline = strike(ff).color(c).size(80, 96)
'''
print(headline.style.size)
print(headline.style.leading)
print(headline.style.color.r)
print(headline.style.color.g)
print(headline.style.color.b)
'''
# Creates the document.
d = document(WIDTH, HEIGHT, 'mm')
p = d.addpage()
p.place(figure.circle(50, 50, 20))
t = headline.text('Hello world!')
#print(type(t))
entity = p.place(t)
entity.frame(10, 10, 380, 80)
im = p.image(kind='rgb')
if not os.path.exists('_export'):
    os.mkdir('_export')
p.svg('_export/hello.svg')
im.png('_export/hello.png')
d.pdf('_export/hello.pdf')
#im.jpeg('_export/hello.jpg')

context = getContext('Flat')
#print(context)
context.newDocument(WIDTH, HEIGHT)
context.newPage()
context.rect(50, 50, 20, 20	)
imagePath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
context.imageSize(imagePath)
#context.saveDocument('_export/test.svg')
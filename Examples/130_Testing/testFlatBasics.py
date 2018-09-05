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
c1 = rgb(180, 0, 125)
c2 = rgb(100, 180, 0)

# Flat font.
ff = font.open(f.path)
#print(ff.name)
#print(ff)
binary = bytes(ff.source.embed())
#print(type(binary))

figure = shape().stroke(c1).width(2.5)
headline = strike(ff).color(c2).size(80, 96)
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
p.place(figure.rectangle(50, 50, 20, 20))
t = headline.text('Hello world!')
#print(type(t))
entity = p.place(t)
entity.frame(10, 10, 380, 80)
im = p.image(kind='rgb')

if not os.path.exists('_export'):
    os.mkdir('_export')

'''
print('Writing to export folder as SVG, PNG, PDF and JPEG.')
p.svg('_export/hello.svg')
im.png('_export/hello.png')
d.pdf('_export/hello.pdf')
im.jpeg('_export/hello.jpg')
'''

context = getContext('Flat')
print(context)
context.newDocument(WIDTH, HEIGHT)
print(context.doc)
context.fill((1, 1, 0))
context.newPage()
print(context.pages)
context.fill((1, 0, 0))
context.stroke((0, 0, 1))
context.text('bla', (100, 100))
context.rect(50, 50, 20, 20)
print(context.pages[0].items)
s = context.pages[0].items[0]
print(s.item.style.fill)
print(s.item.style.stroke)
print(s.item.style.join)
print(s.item.style.limit)
#imagePath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
#size = context.imageSize(imagePath)
#print(size)

# FIXME:
#context.saveDocument('_export/test.pdf')
context.saveDocument('_export/test.png')
#context.saveDocument('_export/test.svg')
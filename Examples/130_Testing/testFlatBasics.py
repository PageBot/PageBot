 # Only runs under Flat
from flat import rgb, font, shape, strike, document
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.contexts.platform import getContext
from pagebot.toolbox.color import blackColor
from pagebot import getResourcesPath
from pagebot.toolbox.units import pt
import os, os.path

WIDTH = 400
HEIGHT = 200

context = getContext('Flat')
f = findFont('Roboto-Regular')
ff = font.open(f.path)
style = dict(font='Roboto-Regular', fontSize=pt(80))
c1 = rgb(180, 0, 125)
c2 = rgb(100, 180, 0)


# Creates the document.
d = document(WIDTH, HEIGHT, 'mm')
#print(d.width)
#print(d.height)
p = d.addpage()
#print(p.width)
context.newDocument(WIDTH, HEIGHT)
#print(context.doc.width)
#print(context.doc.height)

context.newPage()
print(context.pages[0].width)
print(context.pages[0].height)

figure = shape().fill(c1).stroke(c2).width(2.5)
r = figure.rectangle(50, 50, 20, 20)
print(r)
p.place(r)

context.fill((180, 0, 125))
context.stroke((100, 180, 0))
context.strokeWidth(2.5)
context.rect(50, 50, 20, 20)

#print(p.items[0].item.style.width)
#print(context.pages[0].items[0].item.style.width)
s = context.pages[0].items[0]
#print(s.item.style.fill)
#print(s.item.style.stroke)
#print(s.item.style.join)
#print(s.item.style.limit)



#headline = strike(ff).color(c2).size(80, 96)
#t = headline.text('Hello world!')
#entity = p.place(t)
#entity.frame(10, 10, 380, 80)
#bs = context.newString('Hello world!', style=style)
#print(bs.__class__.__name__)
#context.text(bs, (100, 100))


'''
print(headline.style.size)
print(headline.style.leading)
print(headline.style.color.r)
print(headline.style.color.g)
print(headline.style.color.b)
'''


#im = p.image(kind='rgb')
#print(p.items)






# TODO:
#imagePath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
#size = context.imageSize(imagePath)
#print(size)



if not os.path.exists('_export'):
    os.mkdir('_export')

print('Exporting native')
d.pdf('_export/native-flat.pdf')
print('Exporting pagebot')
context.saveDocument('_export/pagebot-flat.pdf')

'''
p.svg('_export/hello.svg')
im.png('_export/hello.png')
im.jpeg('_export/hello.jpg')
'''

# FIXME:

#context.saveDocument('_export/test.png')
#context.saveDocument('_export/test.svg')
from pagebot.fonttoolbox.objects.font import findFont

# TODO: find out how to remove overlap on text.
# Maybe avoid using text but load font in path?

size('A3Landscape')
f = findFont('Roboto-Black')
fontName = installFont(f.path)

fontSize(200)
font(fontName)
stroke(0, 1, 0)
path = BezierPath()
path.rect(x=50, y=100, w=900, h=500)
path.text('Difference', font=fontName, fontSize=200, offset=(105, 200))
path.removeOverlap()

text('Hello world', (100, 650))

drawPath(path)
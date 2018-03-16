from pagebot.contexts.platform import defaultContext as context

W = 600
H = 400

HEAD_LINE = """When fonts started a new world"""

newPage(W, H)


w = 500
x = 20
y = 20

def textBounds(s, x, y, w):
    bs = context.newString(s, w=w,
                           style=dict(font='Georgia', 
                                      rTracking=0.15,
                                      textFill=0))

    tw, th = context.textSize(bs)
    bx, by, bw, bh = bs.bounds()

    context.text(bs, (x-bx, y-by))

    context.fill(None)
    context.stroke((1, 0, 0), 0.5)
    context.rect(x, y, bw, bh)
    context.stroke((0, 0.5, 0), 0.5)
    context.rect(x, y, tw, th)

    return bs

bs = textBounds(HEAD_LINE, x, y, w)
print('%s %s %s' % (bs, bs.fittingFontSize, bs.bounds())
y += 50
bs = textBounds('When fonts...', x, y, w)
print('%s %s %s' % (bs, bs.fittingFontSize, bs.bounds())
y += 80
bs = textBounds('Fonts...', x, y, w)
print('%s %s %s' % (bs, bs.fittingFontSize, bs.bounds())


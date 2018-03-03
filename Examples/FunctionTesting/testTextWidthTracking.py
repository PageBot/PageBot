from pagebot.contexts import defaultContext as context

W = 600
H = 300

HEAD_LINE = """When fonts started a new world"""

newPage(W, H)


w = 500
x = 20
y = 20

bs = context.newString(HEAD_LINE, w=w,
                       style=dict(font='Verdana', rTracking=0.15,
                                  fontSize=24,
                                  textFill=0))
print bs.fittingFontSize

tw, th = context.textSize(bs)
bx, by, bw, bh = bs.bounds()

context.textBox(bs, (x, y, tw, th))

context.stroke((1, 0, 0), 0.5)
context.fill(None)
context.rect(x, y, bw, bh)


y += 40
bs = context.newString('When fonts...', w=w,
                       style=dict(font='Verdana', rTracking=0.15,
                                  fontSize=24,
                                  textFill=0))
print bs.fittingFontSize

tw, th = context.textSize(bs)
bx, by, bw, bh = bs.bounds()

context.textBox(bs, (x-bx, y+by, tw, th))

context.stroke((1, 0, 0), 0.5)
context.fill(None)
context.rect(x, y, bw-bx, bh-by)

y += 80
bs = context.newString('Fonts...', w=w,
                       style=dict(font='Verdana', rTracking=0.15,
                                  fontSize=24,
                                  textFill=0))
print bs.fittingFontSize

tw, th = context.textSize(bs)
bx, by, bw, bh = bs.bounds()

context.textBox(bs, (x-bx, y+by, tw, th))

context.stroke((1, 0, 0), 0.5)
context.fill(None)
context.rect(x, y, bw-bx, bh-by)


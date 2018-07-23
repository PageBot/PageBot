# 
#    Show the DrawBot relation bestween baseline of text() and textbox()
#
size(200, 200)
fontSize(17)
font("Times")
t = "hello world "

text(t, (10, 100))

lineHeight(28)
r = (66, 0, 100, 100 + fontLineHeight()+fontDescender())

textBox(t * 10, r)


stroke(0)

line((0, 100), (200, 100))

stroke(1, 0, 0)
fill(None)
rect(*r)

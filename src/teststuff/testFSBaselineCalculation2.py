size(200, 200)
t = "hello world "
fs = FormattedString(t, font="Times", fontSize=17, lineHeight=28)
fs.fontLineHeight(28)


font("Times")
lineHeight(28)
fontSize(17) 

text(fs, (10, 100))

r = (66, 0, 100, 100 + fontLineHeight()+fontDescender())

fs = FormattedString(t * 10, font="Times", fontSize=17, lineHeight=28)
fs.fontLineHeight(28)

textBox(fs, r)


stroke(0)

line((0, 100), (200, 100))

stroke(1, 0, 0)
fill(None)
rect(*r)
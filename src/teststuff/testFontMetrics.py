M = 20
fill(0.9)
rect(M, M, 1000-2*M, 1000-2*M)

fs = FormattedString('Hlxg', fontSize=400, font='Georgia')
Y = 1000 - M
BASE = Y - 367
YS = (BASE, BASE+fs.fontXHeight(), BASE+fs.fontCapHeight(), BASE+fs.fontAscender(), BASE+fs.fontDescender())
for y in YS:
    stroke(0)
    strokeWidth(0.5)
    line((0, y), (1000, y))

textBox(fs, (M, M, 1000-2*M, 1000-2*M))


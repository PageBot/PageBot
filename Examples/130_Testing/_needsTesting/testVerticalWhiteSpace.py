L = 15

def grid():
    stroke(0.5)
    strokeWidth(0.5)

    for y in range(0, 1600, L):
        line((0, y), (1000, y))

def col(f, x):
    s1 = 'AAAAAAA\n'
    s3 = 'bbbbbbb\n---------------\n'

    s = FormattedString(s1, fontSize=60, font=f, lineHeight=4*L,
        tracking=5)
    s += FormattedString(s1, fontSize=60)
    #s += FormattedString(s3, fontSize=20, paragraphTopSpacing=20)
    print(f, 'Ascender', s.fontAscender())
    print(f, 'Descender', s.fontDescender())
    textBox(s, (x+10, 10, 400, 900))

    stroke(0)
    fill(None)
    rect(x+10, 10, 400, 900)


grid()
col('Verdana', 0)
col('Georgia', 450)

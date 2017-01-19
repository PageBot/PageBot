from pagebot import textBoxBaseLines

leading = 24
for n in range(0, 1000, leading):
    stroke(1, 0, 0)
    fill(None)
    line((0, n),(1000,n))

def appendS(fs1, fs2, w, baselineGrid):
    u"""Append fs2 to fs2, while keeping baseline grid locked.
    Assumed is that the top fs1 textBox is already on the baseline grid."""
    h = 1000
    box = 0, 0, w, h
    # Get the status of of the target string. We need to know the position of the last line.
    baselines = textBoxBaseLines(fs2, box)
    if baselines:
        print 1000-baselines[0][1], 1000-baselines[-1][1]
    return fs1
    
    #paragraphTopSpacing
   
fs1 = FormattedString('')   
fs2 = FormattedString('aaa vvv bbbbbb\nss' * 5, fontSize=14, lineHeight=24)

appendS(fs1, fs2, 300, 24)

bx, by, bw, bh = 50, 50, leading*3, 200, leading*20
stroke(0)
fill(None)
rect(bx, by, bw, bh)
"""
Y = 100
bx, by, bw, bh = box = (100, Y, 400, 500)
baselines = textBoxBaseLines(fs, box)
for x, y in baselines:
    stroke(0, 1, 0)
    fill(None)
    line((x-10, y), (400+10, y))
dy = round(baselines[0][1]/leading)*leading - baselines[0][1]
print dy
box2 = (bx,by+dy, 400, 500)
textBox(fs, box2)
rect(bx, by+dy, bw, bh)
"""

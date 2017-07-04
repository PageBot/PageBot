W, H = 1000, 1000

# --------------------------------------------
newPage(W, H)
font('Verdana')
fontSize(300)
fill(1, 0, 0)
text('aaa', (50, 50))

fs = FormattedString('aaaa', font='Georgia', fontSize=300, fill=(0, 1, 0))
fs += FormattedString('a', font='Georgia-Bold', fontSize=200, fill=(0, 0.5, 0.5))
tw, th = textSize(fs)

text(fs, (W/2-tw/2, 400)) 

fs = FormattedString('aa', font='Georgia-Italic', fontSize=200, fill=(0, 1, 0))
fs += FormattedString('aaa', font='Georgia-Bold', fontSize=30, fill=(0, 0.5, 0.5))
tw, th = textSize(fs)

text(fs, (W/2-tw/2, 600)) 
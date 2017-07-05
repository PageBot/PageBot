## Works with this version of DrawBot:
## https://github.com/thomgb/drawbot
## download my DrawBot: https://www.dropbox.com/s/xsu1mz89ipo5x3y/DrawBot.dmg?dl=0

t = FormattedString("programmatic", fontSize=30, hyphenationHead=4, hyphenationTail=3)
hyphenation(True)

w=200 # change width to see other hyphenations

textBox(t, (100,100,w,600)) fill(None)
stroke(0)
rect(100,100,w,600)
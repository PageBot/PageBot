import pagebot
import pagebot.toolbox
import pagebot.toolbox.timemark

from pagebot.toolbox.timemark import TimeMark


tms = [TimeMark(0, 'aaaa'), TimeMark(1000, 'vvv')]

tms.append(TimeMark(4, 'xxx'))
print tms
print tms.sort()
print tms
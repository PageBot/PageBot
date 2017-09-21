from pagebot.builders import drawBotBuilder as b
if b is None:
	print 'Example only runs in DrawBot'
	raise KeyboardInterrupt()
	
f = FormattedString()

f.fill(1, 0, 0)
f.fontSize(100)
f += "hello"

attr = f.getNSObject()

attr.addAttribute_value_range_("com.petr.pageBot.myAttribute", "this is my data", (0, 5)) 

f += " "
f += "world"

attr = f.getNSObject()
attr.addAttribute_value_range_("com.petr.pageBot.myOtherAttibute", ["a", "list", "object"], (5, 5)) 

text(f, (96, 172))


#print attr

ff = b.FormattedString('AAAA', font='Verdana', fontSize=100, fill=(0, 0.5, 0))
b.text(ff, (96, 440))
attr = ff.getNSObject()
attr.addAttribute_value_range_("io.pageBot.class", 'CLASS_NAME', (0, len(ff))) 
attr.addAttribute_value_range_("io.pageBot.tag", 'TAG_NAME', (0, len(ff))) 

#print attr

fff = ff + f
attr = fff.getNSObject()

print attr


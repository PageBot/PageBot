t = '''Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent
claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium
lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.'''

s = 36
fontSize(s)
font('Verdana')
hyphenation(True)

p= 10
x = p
w = 600
h = 400
y0 = p
y1 = h + 2*p

overflow = textBox(t, (x, y0, w, h), align='right')
print('Overflow: %d' % len(overflow))

hyphenation(False)
baselineShift(s)
lh = 100
lineHeight(lh)
print('Line height: %d' % lh)
print('Leading: %s' % fontLeading())
print('Ascender %s' % fontAscender())
overflow = textBox(t, (x, y1, w, h), align='center')
print('Overflow: %d' % len(overflow))


fill(None)
stroke(0, 1, 0)
rect(x=x, y=y0, w=w, h=h)
rect(x=x, y=y1, w=w, h=h)
stroke(1, 0, 0)
line((x, y0+h-s), (w+x, y0+h-s))
line((x, y1 + h-s), (w+x, y1 + h-s))


spacer = FormattedString('a\n', lineHeight=1, fontSize=2)

t = spacer + FormattedString('Hello', font='Verdana', lineHeight=110, fontSize=100)

textBox(t, (10, 10, 500, 500))

stroke(0)
fill(None)
rect(10, 10, 300, 500)



spacer = FormattedString('a\nb', lineHeight=1, fontSize=2)

t = spacer + FormattedString('Hello', font='Verdana', lineHeight=110, fontSize=100)

textBox(t, (320, 10, 300, 500))

stroke(0)
fill(None)
rect(320, 10, 300, 500)
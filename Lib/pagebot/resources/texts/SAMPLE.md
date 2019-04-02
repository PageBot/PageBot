~~~
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.contributions.filibuster.blurb import blurb
box = newTextBox(parent=page, name='Content', conditions=[Fit2Height(), Fit2ColSpan(0, 2)])
box.bs += doc.context.newString(blurb.getBlurb('_headline')+'\n')
page.solve()

~~~

## Headline

### H3 Headline

~~~
box.bs += doc.context.newString(blurb.getBlurb('article')+'\n')
page = page.next
box = newTextBox(parent=page, name='Content', conditions=[Fit()])
page.solve()

box.bs += doc.context.newString(blurb.getBlurb('article')+'\n')

~~~
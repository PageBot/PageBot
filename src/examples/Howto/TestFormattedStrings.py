aa = FormattedString('Book Cover', font='Georgia', fontSize=40)
print textSize(aa)


aa = FormattedString('')
aa.font('Georgia')
aa.fontSize(14)
aa += '123'
aa.fontSize(40)
aa.lineHeight(1.3)
aa += ('Book Cover')
print textSize(aa)

aa = FormattedString('')
aa.font('Georgia')
aa.fontSize(40)
aa += 'Book Cover'
print textSize(aa)
print aa.fontAscender()
print aa.fontDescender()
print aa.fontAscender() - aa.fontDescender()

stroke(0)
fill(None)
rect(100, 100, 200, 200)
text(aa, (100, 100))
def css(name, e, styles=None, default=None):
    u"""Answer the named style values. Search in optional style dict first, otherwise up the 
    parent tree of styles in element e. Both e and style can be None. In that case None is answered."""
    if styles is not None: # Can be single style or stack of styles.
        if not isinstance(styles, (tuple, list)):
            styles = [styles] # Make stack of styles.
        for style in styles:
            if name in style:
                return style[name]
    if e is not None:
        return e.css(name)
    return default


def getFormattedString(t, e=None, style=None):
    u"""Answer a formatted string from valid attributes in Style. Set the all values after testing
    their existence, so they can inherit from previous style formats."""

    fs = FormattedString('')
    sFont = css('font', e, style)
    if sFont is not None:
        fs.font(sFont)
    sFontSize = css('fontSize', e, style)
    if sFontSize is not None:
        fs.fontSize(sFontSize)
    return fs + t
    
fs = getFormattedString('Book Cover', style=dict(font='Georgia', fontSize=40))
print textSize(fs)
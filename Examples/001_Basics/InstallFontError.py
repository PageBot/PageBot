
path = 'Roboto-Regular.ttf'
installFont(path)

fs = FormattedString('bbb', font=path, fontSize=100)
text(fs, (120, 400))
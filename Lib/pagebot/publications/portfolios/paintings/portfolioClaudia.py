
from pagebot.publications.portfolio import PortFolio
path = '/Volumes/Flatter/2018-10 tekeningen clau bijeenkomst nina'
from pagebot.constants import A4
name = 'Portfolio Claudia Mens'
pf = PortFolio(path=path, cols=3, rows=4, padding=30, resolution=2,
    originTop=False, size=A4, name=name)
pf.export(name, path='_export/PortFolio.pdf')


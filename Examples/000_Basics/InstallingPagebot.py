import sys
print('Python version is:')
print(sys.version)

print('\nChecking library installation paths... \n')
import site
try:
    packages = site.getsitepackages()
    for p in packages:
        print(' - %s' % p)
except:
    print('x Could not read site packages :S')
    
try:
    import pagebot
    print('\n! Pagebot found at %s' % pagebot.__path__[0])
except:
    print('\nx Pagebot not found')

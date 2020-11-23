#!/usr/bin/env python3

import os
import subprocess

def getDirs(root):
    return [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]

def getFiles(root):
    return [(f, os.path.join(root, f)) for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]

def reverse(files):
    for (f, p) in files:
        if f.startswith('.'):
            continue

        else:
            name = f.split('.')[0]
            subprocess.call('pyreverse')# -p %s %s' % (name, p))
            print(name, p)
            break

if __name__ == "__main__":
    root = '../Lib/pagebot'
    files = getFiles(root)
    reverse(files)



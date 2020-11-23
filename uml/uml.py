#!/usr/bin/env python3

# pyreverse -p contexts_basecontext_basecontext ../Lib/pagebot/contexts/basecontext/basecontext.py
# dot -Tpng classes_contexts_basecontext_basecontext.dot -o classes_contexts_basecontext_basecontext.png

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



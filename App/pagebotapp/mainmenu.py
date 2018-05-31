#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# mainmenu.py
#
# Script to write MainMenu.xib XML.

try:
    from lxml import etree
except:
    print('lxml is not installed, can\'t write XML')

# TODO: to en.proj
path = './MainMenu.xib'

appName = 'PageBot'
delegateID = 373
ibType = "com.apple.InterfaceBuilder3.Cocoa.XIB"
pluginIdentifier = "com.apple.InterfaceBuilder.CocoaPlugin"
version = '3.0'
toolsVersion="12118"
systemVersion="16E195"
targetRuntime="MacOSX.Cocoa"
propertyAccessControl="none"
s = 'separator'

menuDict = {appName:
        ['About %s' % appName, s,
        'Preferences...', s,
        'Services', s,
        'Hide %s' % appName,
        'Hide Others',
        'Show All', s,
        'Quit %s' % appName]}

def mainMenu():
    """Writes design space XML file using the lxml library.."""
    root = etree.Element('document', type=ibType, version=version,
            toolsVersion=toolsVersion, systemVersion=systemVersion,
            targetRuntime=targetRuntime,
            propertyAccessControl=propertyAccessControl)

    # XCode settings.
    dependencies = etree.SubElement(root, 'dependencies')
    deployment = etree.Element('deployment', version='1050', identifier='macosx')
    plugIn = etree.Element('plugIn', identifier=pluginIdentifier, version=toolsVersion)
    dependencies.append(deployment)
    dependencies.append(plugIn)

    # Application objects.
    objects = etree.SubElement(root, 'objects')
    co1 = etree.Element('customObject', id='-2', userLabel="File's Owner", customClass="NSApplication")
    co2 = etree.Element('customObject', id='-1', userLabel="First Responder", customClass="FirstResponder")
    co3 = etree.Element('customObject', id='-3', userLabel="Application", customClass="NSObject")

    # Connection to PyObjC AppDelegate class.
    connections = etree.Element('connections')
    outlet = etree.Element('outlet', property='delegate', destination=str(delegateID), id="M3r-9y-AZh")
    connections.append(outlet)
    co3.append(connections)
    objects.append(co1)
    objects.append(co2)
    objects.append(co3)
    menu = buildMenu()
    objects.append(menu)

    # PyObjC AppDelegate class.
    delegate = etree.Element('customObject', id=str(delegateID), userLabel="AppDelegate", customClass="AppDelegate")
    objects.append(delegate)
    writeFile(root, path)

def buildMenu():
    menu = etree.Element('menu', title="MainMenu", systemMenu="main",
            showsStateColumn="NO", autoenablesItems="NO", id="29",
            userLabel="MainMenu")
    items = etree.SubElement(menu, 'items')
    id = 56

    for key, value in menuDict.items():
        m = etree.Element('menuItem', title=key, id=str(id))
        items.append(m)
        id += 1

        if isinstance(value, list):
            for v in value:
                if v == s:
                    i = etree.Element('menuItem', isSeparatorItem="YES", id=str(id))
                    mm = etree.Element('modifierMask', key='keyEquivalentModifierMask', commmand='YES')
                    i.append(mm)
                    m.append(i)
                    id += 1
                else:
                    i = etree.Element('menuItem', title=v, id=str(id))
                    m.append(i)
                    id += 1
    return menu

def writeFile(root, path):
    f = open(path, 'wb')
    lines = etree.tostring(root, xml_declaration=True, encoding='utf-8',
            pretty_print=True)
    f.write(lines)
    f.close()


if __name__ == '__main__':
    mainMenu()

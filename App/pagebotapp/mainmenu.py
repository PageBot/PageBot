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

path = './en.lproj/MainMenu.xib'

appName = 'PageBot'
delegateID = 373
ibType = "com.apple.InterfaceBuilder3.Cocoa.XIB"
pluginIdentifier = "com.apple.InterfaceBuilder.CocoaPlugin"
version = '3.0'
toolsVersion="11542"
systemVersion="16B2657"
targetRuntime="MacOSX.Cocoa"
propertyAccessControl="none"
s = 'separator'

'''
{title':"About PageBot", id:"58", 'modifierMask': "keyEquivalentModifierMask"
'selector':"orderFrontStandardAboutPanel:", 'target':"-2", id:"142"}
{'title':"Preferences…", keyEquivalent:",", id:"129", userLabel:"Preferences"}
{'title':"Services", id:"131"}
{menu key:"submenu", 'title':"Services", systemMenu:"services", id:"130"}
{'title':"Hide PageBot", keyEquivalent:"h", id:"134": 'selector':"hide:",
'target':"-1", id:"367"}
{'title':"Hide Others", keyEquivalent:"h", id:"145", 'modifierMask':
"keyEquivalentModifierMask", 'option':"YES", 'command':"YES",
'selector':"hideOtherApplications:", 'target':"-1", id:"368"}
{'title':"Show All", 'selector':"unhideAllApplications:", 'target':"-1", id:"370"}
{'title':"Quit PageBot", keyEquivalent:"q", id:"136", userLabel:"Quit PageBot", 'selector':"terminate:", 'target':"-3", id:"Fad-te-kKi"}
'''

about = {'title': 'About %s' % appName, 'id': '58',
        'modifierMask': "keyEquivalentModifierMask",
        'action': {'selector': 'orderFrontStandardAboutPanel:', 'target': '-2', 'id': "142"}}

hide = {'title': 'Hide %s' % appName, 'id': '134',
        'action': {'selector':"hide:", 'target':"-1", 'id':"367"}}

preferences = {'title': 'Preferences...', 'id': '143'}
services = {'title': 'Services', 'id': '131'}
hideOthers = {'title': 'Hide Others', 'modifierMask':
        "keyEquivalentModifierMask", 'id': '145'}
showAll = {'title': 'Show All', 'id': '150'}

quit = {'title': 'Quit %s' % appName, 'keyEquivalent': "q", 'id': '136',
        'action': {'selector':"terminate:", 'target':"-3", 'id':"Fad-te-kKi"}}

open_ = {'title':"New", 'keyEquivalent':"n", 'id':"83", 'userLabel':'New'}

menuPageBot = [about, hide, preferences, services, hideOthers, showAll, quit]
menuFile = [open_]
menuEdit = []
menuHelp = []

menuList = [
    {'title': appName, 'systemMenu': 'apple', 'menu': menuPageBot, 'id': '56'},
    {'title': 'File', 'menu': menuFile, 'id': '81'},
    #{'title': 'Edit', 'menu': []},
    #{'title': 'Help', 'menu': []}
]

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
    co1 = etree.Element('customObject', id='-2', userLabel="File's Owner",
            customClass="NSApplication")
    co2 = etree.Element('customObject', id='-1', userLabel="First Responder",
            customClass="FirstResponder")
    co3 = etree.Element('customObject', id='-3', userLabel="Application",
            customClass="NSObject")

    # Connection to PyObjC AppDelegate class.
    connections = etree.Element('connections')
    outlet = etree.Element('outlet', property='delegate',
            destination=str(delegateID), id="M3r-9y-AZh")
    connections.append(outlet)
    co3.append(connections)
    objects.append(co1)
    objects.append(co2)
    objects.append(co3)
    menu = buildMenu()
    objects.append(menu)

    # PyObjC AppDelegate class.
    delegate = etree.Element('customObject', id=str(delegateID),
            userLabel="AppDelegate", customClass="AppDelegate")
    objects.append(delegate)
    writeFile(root, path)


def buildMenu():

    # Main menu wrapper.
    menu = etree.Element('menu', title="MainMenu", systemMenu="main",
            showsStateColumn="NO", autoenablesItems="NO", id="29",
            userLabel="MainMenu")
    items = etree.SubElement(menu, 'items')

    # The menu columns.
    for menuDict in menuList:
        t = menuDict['title']
        itemID = menuDict['id']

        # Wraps a column.
        m = etree.Element('menuItem', title=t, id=str(itemID))
        if 'systemMenu' in menuDict:
            sm = menuDict['systemMenu']
            mm = etree.Element('menu', key='submenu', systemMenu=sm, title=t,
                    id=str(int(itemID) + 1))
        else:
            mm = etree.Element('menu', key='submenu', title=t, id=str(int(itemID) + 1))
        m.append(mm)
        subitems = etree.SubElement(menu, 'items')
        mm.append(subitems)
        items.append(m)

        # Now upack the list.
        submenuList = menuDict['menu']

        for v in submenuList:
            i = menuItem(v)
            subitems.append(i)
    return menu

def menuItem(v):
    i = None
    if v == s:

        # TODO: ID's for separators.
        itemID = 500
        i = etree.Element('menuItem', isSeparatorItem="YES", id=str(itemID))
        mm = etree.Element('modifierMask', key='keyEquivalentModifierMask',
                commmand='YES')
        i.append(mm)

    elif isinstance(v, dict):
        attrib = {}

        for key in ('id', 'title', 'keyEquivalent', 'userLabel', 'option', 'command'):
            if key in v:
                attrib[key] = v[key]

        i = etree.Element('menuItem', attrib=attrib)

        if 'modifierMask' in v:
            mm = etree.Element('modifierMask', key='keyEquivalentModifierMask')
            i.append(mm)

        if 'action' in v:
            a = v['action']

            c = etree.SubElement(i, 'connections')
            action = etree.Element('action', selector=a['selector'], target=a['target'],
                    id=a['id'])
            c.append(action)

    return i

def writeFile(root, path):
    f = open(path, 'wb')
    lines = etree.tostring(root, xml_declaration=True, encoding='utf-8',
            pretty_print=True)
    f.write(lines)
    f.close()


if __name__ == '__main__':
    mainMenu()

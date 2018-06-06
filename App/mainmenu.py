#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# mainmenu.py
#
# Script to write MainMenu.xib XML.

import traceback
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

# Keys that are directly copied to the XML element.
flatKeys = ('isSeparatorItem', 'id', 'title', 'keyEquivalent', 'userLabel',
        'option', 'command', 'state', 'shift')

def getSeparator(sid):
    return {'isSeparatorItem': 'YES', 'id': str(sid), 'userLabel': 'Separator',
            'modifierMask': {'key': 'keyEquivalentModifierMask', 'command': 'YES'}}

'''
Menu as a dictionary. This part should be edited.

'''

# Pagebot menu items.
about = {'title': 'About %s' % appName, 'id': '58', 'modifierMask':
        {'key': 'keyEquivalentModifierMask'}, 'action': {'selector':
            'orderFrontStandardAboutPanel:', 'target': '-2', 'id': '142'}}
s236 = getSeparator(236)
hide = {'title': 'Hide %s' % appName, 'id': '134', 'keyEquivalent': 'h',
        'action': {'selector':'hide:', 'target':'-1', 'id':'367'}}
preferences = {'title': 'Preferences...', 'id': '129', 'keyEquivalent': ',',
        'userLabel': 'Preferences'}
s143 = getSeparator(143)
servicesMenu = {'key':'submenu', 'title':'Services', 'systemMenu':'services',
        'id':'130'}
services = {'title': 'Services', 'id': '131', 'menu': servicesMenu}
s144 = getSeparator(144)
hideOthers = {'title': 'Hide Others', 'modifierMask':
        {'key': 'keyEquivalentModifierMask'}, 'keyEquivalent': 'h', 'option': 'YES',
        'command': 'YES', 'id': '145'}
showAll = {'title': 'Show All', 'id': '150', 'action':
        {'selector':'unhideAllApplications:', 'target':'-1', 'id': '370'}}
s149 = getSeparator(149)
quit = {'title': 'Quit %s' % appName, 'keyEquivalent': 'q', 'id': '136',
        'userLabel': 'Quit PageBot', 'action': {'selector':'terminate:',
            'target':'-3', 'id':'Fad-te-kKi'}}

menuPageBot = [about, s236, hide, preferences, s143, services, s144,
        hideOthers, showAll, s149, quit]

# File menu items.
new = {'title':'New', 'keyEquivalent':'n', 'id':'82', 'userLabel':'New'}
        #'action': {'selector':'new:', 'target':'-3', 'id':'bla'}}
open_ = {'title':'Open...', 'keyEquivalent': 'o', 'id':'3rG-1J-ytm'}

clearMenu = {'title':"Clear Menu", 'state': "on", 'id': "126", 'action':
        {'selector': "clearRecentDocuments:", 'target':"-1", 'id': "127"}}

recentMenu = {'key': "submenu", 'title': "Open Recent", 'systemMenu':
        "recentDocuments", 'id': "125", 'items': [clearMenu]}

openRecent = {'title':"Open Recent", 'id':"124", 'menu': recentMenu}
s79 = {'isSeparatorItem': 'YES', 'id':'79', 'userLabel': 'Separator',
        'modifierMask': {'key': 'keyEquivalentModifierMask', 'command': 'YES'}}
close = {'title':'Close', 'keyEquivalent':'w', 'id':'73', 'userLabel':'Close'}
save = {'title':"Save", 'keyEquivalent':"s", 'id':"75", 'userLabel':"Save"}
saveAs = {'title':'Save As...', 'keyEquivalent': "S", 'id': "80", 'userLabel':
        "Save As...", 'modifierMask': {'key': "keyEquivalentModifierMask",
            'shift': "YES", 'command': "YES"}}
revert = {'title':"Revert to Saved", 'id':"112", 'userLabel':"Revert to Saved",
        'modifierMask': { 'key':"keyEquivalentModifierMask"}, 'action':
        {'selector':"revertDocumentToSaved:", 'target':"-1", 'id':"364"}}
export = {'title':"Export...", 'keyEquivalent':"X", 'id':"4Lj-dJ-kqz"}
info = {'title':"Info...", 'keyEquivalent':"I", 'id':"Caq-rH-He2",
        'modifierMask': {'key':"keyEquivalentModifierMask"}}
s74 = {'isSeparatorItem':"YES", 'id':"74", 'userLabel':"Separator",
        'modifierMask': {'key':"keyEquivalentModifierMask", 'command':"YES"}}
pageSetup = {'title':"Page Setup...", 'keyEquivalent':"P", 'id':"77",
        'userLabel':"Page Setup...", 'modifierMask':
        {'key':"keyEquivalentModifierMask", 'shift':"YES", 'command':"YES"},
        'action': {'selector':"runPageLayout:", 'target':"-1", 'id':"87"}}
print_ = {'title':"Print...", 'keyEquivalent':"p", 'id':"78",
        'userLabel':"Print...", 'action': {'selector':"print:", 'target':"-1",
            'id':"86"}}

menuFile = [new, open_, openRecent, s79, close, save, saveAs, revert, export, info,
        s74, pageSetup, print_]

# Edit menu items.
redo = {'title':"Redo", 'keyEquivalent':"Z", 'id':"215", 'modifierMask':
        {'key':"keyEquivalentModifierMask", 'shift':"YES", 'command':"YES"}}
undo = {'title':"Undo", 'keyEquivalent':"z", 'id':"207"}
s206 = {'isSeparatorItem':"YES", 'id':"206", 'modifierMask':
        {'key':"keyEquivalentModifierMask", 'command':"YES"}}
cut = {'title':"Cut", 'keyEquivalent':"x", 'id':"199", 'action':
        {'selector':"cut:", 'target':"-1", 'id':"228"}}
copy = {'title':"Copy", 'keyEquivalent':"c", 'id':"197", 'action':
        {'selector':"copy:", 'target':"-1", 'id':"224"}}
paste = {'title':"Paste", 'keyEquivalent':"v", 'id':"203", 'action':
        {'selector':"paste:", 'target':"-1", 'id':"226"}}
delete = {'title':"Delete", 'id':"202", 'action': {'selector':"delete:",
    'target':"-1", 'id':"235"}}
selectAll = {'title':"Select All", 'id':"198", 'modifierMask':
        {'key':"keyEquivalentModifierMask"}}
s214 = {'isSeparatorItem':"YES", 'id':"214", 'modifierMask':
        {'key':"keyEquivalentModifierMask", 'command':"YES"}}

menuEdit = [redo, undo, s206, cut, copy, paste, delete, selectAll, s214]

# Find menu items.

find_ = {'title':"Find...", 'tag':"1", 'keyEquivalent':"f", 'id':"209",
        'action': {'selector':"performFindPanelAction:", 'target':"-1",
            'id':"241"}}
findNext = {'title':"Find Next", 'tag':"2", 'keyEquivalent':"g", 'id':"208"}
findPrevious = {'title':"Find Previous", 'tag':"3", 'keyEquivalent':"G",
        'id':"213", 'modifierMask': {'key':"keyEquivalentModifierMask"},
        'shift':"YES", 'command':"YES"}
useSelection = {'title':"Use Selection for Find", 'tag':"7",
        'keyEquivalent':"e", 'id':"221"}
jumpTo = {'title':"Jump to Selection", 'keyEquivalent':"j", 'id':"210",
        'action': {'selector':"centerSelectionInVisibleArea:", 'target':"-1",
            'id':"245"}}

menuFind = [find_, findNext, findPrevious, useSelection, jumpTo]

# Help menu items.
pagebotHelp = {'title':"PageBot Help", 'keyEquivalent':"?", 'id':"111",
        'userLabel':"PageBot Help", 'action': {'selector':"showHelp:",
            'target':"-1", 'id':"360"}}

menuHelp = [pagebotHelp]

# TODO: 'items' instead of 'menu' for full recursion from top level.
menuList = [
    {'title': appName, 'systemMenu': 'apple', 'menu': menuPageBot, 'id': '56',
        'subMenuId': '57'},
    {'title': 'File', 'menu': menuFile, 'id': '83', 'subMenuId': '81'},
    {'title': 'Edit', 'menu': menuEdit, 'id': '217', 'subMenuId': '205'},
    {'title': 'Find', 'menu': menuFind, 'id': '218', 'subMenuId': '220'},
    {'title': 'Help', 'menu': menuHelp, 'id': '103', 'subMenuId': '106'}
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
    for d in menuList:
        t = d['title']

        # Wraps a column.
        m = etree.Element('menuItem', title=t, id=d['id'])

        if 'systemMenu' in d:
            sm = d['systemMenu']
            mm = etree.Element('menu', key='submenu', systemMenu=sm, title=t,
                    id=d['subMenuId'])
        else:
            mm = etree.Element('menu', key='submenu', title=t, id=d['subMenuId'])

        m.append(mm)
        subitems = etree.SubElement(menu, 'items')
        mm.append(subitems)
        items.append(m)

        # Now upack the list.
        submenuList = d['menu']

        for v in submenuList:
            try:
                i = getMenuItem(v)
            except Exception as e:
                print(traceback.format_exc())
            subitems.append(i)
    return menu

def getMenuItem(v):
    assert isinstance(v, dict)
    attrib = {}

    for key in flatKeys:
        if key in v:
            attrib[key] = v[key]

    try:
        menuItem = etree.Element('menuItem', attrib=attrib)
    except Exception as e:
        print("Error creating Element %s" % v['title'])
        raise(e)

    if 'modifierMask' in v:
        attrib = v['modifierMask']
        modifierMask = etree.Element('modifierMask', attrib=attrib)
        menuItem.append(modifierMask)

    if 'action' in v:
        a = v['action']

        connections = etree.SubElement(menuItem, 'connections')
        action = etree.Element('action', selector=a['selector'], target=a['target'],
                id=a['id'])
        connections.append(action)

    if 'menu' in v:
        subMenu = getSubMenu(v['menu'])
        menuItem.append(subMenu)

    return menuItem

def getSubMenu(d):
    # TODO: recursion.
    # if 'menu' in d:
    #     pop submenu
    #     do recursion.
    i = []
    attrib = {}

    for key, value in d.items():
        if 'items' in d:
            i = d['items']
        else:
            attrib[key] = value

    menu = etree.Element('menu', attrib=attrib)
    items = etree.SubElement(menu, 'items')

    for v in i:
        menuItem = getMenuItem(v)
        items.append(menuItem)

    return menu

def writeFile(root, path):
    f = open(path, 'wb')
    lines = etree.tostring(root, xml_declaration=True, encoding='utf-8',
            pretty_print=True)
    f.write(lines)
    f.close()
    print('Wrote menu to %s' % path)

if __name__ == '__main__':
    mainMenu()

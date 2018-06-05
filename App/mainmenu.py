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
flatKeys = ('isSeparator', 'id', 'title', 'keyEquivalent', 'userLabel', 'option', 'command')

about = {'title': 'About %s' % appName, 'id': '58', 'modifierMask':
        'keyEquivalentModifierMask', 'action': {'selector':
            'orderFrontStandardAboutPanel:', 'target': '-2', 'id': '142'}}
sep0 = {'isSeparator': 'YES', 'id': '236'}
hide = {'title': 'Hide %s' % appName, 'id': '134', 'keyEquivalent': 'h',
        'action': {'selector':'hide:', 'target':'-1', 'id':'367'}}

preferences = {'title': 'Preferences...', 'id': '143', 'keyEquivalent': ',',
        'userLabel': 'Preferences'}

servicesMenu = {'key':'submenu', 'title':'Services', 'systemMenu':'services',
        'id':'130'}
services = {'title': 'Services', 'id': '131', 'menu': servicesMenu}

hideOthers = {'title': 'Hide Others', 'modifierMask':
        'keyEquivalentModifierMask', 'keyEquivalent': 'h', 'option': 'YES',
        'command': 'YES', 'id': '145'}

showAll = {'title': 'Show All', 'id': '150', 'action':
        {'selector':'unhideAllApplications:', 'target':'-1', 'id': '370'}}

quit = {'title': 'Quit %s' % appName, 'keyEquivalent': 'q', 'id': '136',
        'userLabel': 'Quit PageBot', 'action': {'selector':'terminate:',
            'target':'-3', 'id':'Fad-te-kKi'}}

new = {'title':'New', 'keyEquivalent':'n', 'id':'83', 'userLabel':'New'}
open_ = {'title':'Open...', 'keyEquivalent': 'o', 'id':'3rG-1J-ytm'}
openRecent = {'title':"Open Recent", 'id':"124"}

'''
{menu key:"submenu", 'title': "Open Recent", 'systemMenu': "recentDocuments", 'id': "125"}
{'title':"Clear Menu", state: "on", 'id': "126"}
{action 'selector': "clearRecentDocuments:", 'target':"-1", 'id': "127"}
{menu}
'''

sep10 = {'isSeparatorItem': 'YES', 'id':'79', 'userLabel': 'Separator'}
close = {'title':'Close', 'keyEquivalent':'w', 'id':'73', 'userLabel':'Close'}

menuPageBot = [about, sep0, hide, preferences, services, hideOthers, showAll,
        quit]
menuFile = [new, open_, openRecent, sep10]
menuEdit = []
menuHelp = []

menuList = [
    {'title': appName, 'systemMenu': 'apple', 'menu': menuPageBot, 'id': '56'},
    {'title': 'File', 'menu': menuFile, 'id': '81'},
    #{'title': 'Edit', 'menu': menuEdit, 'id'217'},
    #{'title': 'Help', 'menu': menuHelp}
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
        modifierMask = etree.Element('modifierMask', key='keyEquivalentModifierMask')
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
    attrib = {}
    # TODO: recursion?
    e = etree.Element('menu', attrib=attrib)
    return e

def writeFile(root, path):
    f = open(path, 'wb')
    lines = etree.tostring(root, xml_declaration=True, encoding='utf-8',
            pretty_print=True)
    f.write(lines)
    f.close()


if __name__ == '__main__':
    mainMenu()

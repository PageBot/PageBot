# elements.variablefonts.variableeditor


## Functions

### DatePicker
**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the date picker control.

+-------------------------------------+
| **Standard Dimensions - Text Mode** |
+---------+---+-----------------------+
| Regular | H | 22|
+---------+---+-----------------------+
| Small   | H | 19|
+---------+---+-----------------------+
| Mini| H | 16|
+---------+---+-----------------------+

+------------------------------------------+
| **Standard Dimensions - Graphical Mode** |
+--------------------+---------------------+
| Calendar and Clock | 227w 148h   |
+--------------------+---------------------+
| Calendar   | 139w 148h   |
+--------------------+---------------------+
| Clock  | 122w 123h   |
+--------------------+---------------------+

**date** A *NSDate* object representing the date and time that should be set in the control.

**minDate** A *NSDate* object representing the lowest date and time that can be set in the control.

**maxDate** A *NSDate* object representing the highest date and time that can be set in the control.

**showStepper** A boolean indicating if the thumb stepper should be shown in text mode.

**mode** A string representing the desired mode for the date picker control. The options are:

+-------------+
| "text"  |
+-------------+
| "graphical" |
+-------------+

**timeDisplay** A string representing the desired time units that should be displayed in the
date picker control. The options are:

+--------------------+-------------------------------+
| None   | Do not display time.  |
+--------------------+-------------------------------+
| "hourMinute"   | Display hour and minute.  |
+--------------------+-------------------------------+
| "hourMinuteSecond" | Display hour, minute, second. |
+--------------------+-------------------------------+

**dateDisplay** A string representing the desired date units that should be displayed in the
date picker control. The options are:

+----------------+------------------------------+
| None   | Do not display date. |
+----------------+------------------------------+
| "yearMonth"| Display year and month.  |
+----------------+------------------------------+
| "yearMonthDay" | Display year, month and day. |
+----------------+------------------------------+

**sizeStyle** A string representing the desired size style of the date picker control. This only
applies in text mode. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### FloatingWindow
A window that floats above all other windows.

To add a control to a window, simply set it as an attribute of the window.

from vanilla import *

class FloatingWindowDemo(object):

def __init__(self):
self.w = FloatingWindow((200, 70), "FloatingWindow Demo")
self.w.myButton = Button((10, 10, -10, 20), "My Button")
self.w.myTextBox = TextBox((10, 40, -10, 17), "My Text Box")
self.w.open()

FloatingWindowDemo()

No special naming is required for the attributes. However, each attribute
must have a unique name.

**posSize** Tuple of form *(left, top, width, height)* representing the position
and size of the window. It may also be a tuple of form *(width, height)*.
In this case, the window will be positioned on screen automatically.

**title** The title to be set in the title bar of the window.

**minSize** Tuple of the form *(width, height)* representing the minimum size
that the window can be resized to.

**maxSize** Tuple of the form *(width, height)* representing the maximum size
that the window can be resized to.

**textured** Boolean value representing if the window should have a textured
appearance or not.

**autosaveName** A string representing a unique name for the window. If given,
this name will be used to store the window position and size in the application
preferences.

**closable** Boolean value representing if the window should have a close button
in the title bar.

**screen** A `NSScreen <http://tinyurl.com/NSScreen>`_ object indicating the screen that
the window should be drawn to. When None the window will be drawn to the main screen.
### CheckBox
### Group
An invisible container for controls.

To add a control to a group, simply set it as an attribute of the group.::

from vanilla import *

class GroupDemo(object):

def __init__(self):
self.w = Window((150, 50))
self.w.group = Group((10, 10, -10, -10))
self.w.group.text = TextBox((0, 0, -0, -0),
"This is a group")
self.w.open()

GroupDemo()

No special naming is required for the attributes. However, each attribute must have a unique name.

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the group.

**blendingMode** The blending mode for the window. These are the possible options:

+----------------+-------------------------------------------+
| None   | No special blending.  |
+----------------+-------------------------------------------+
| "behindWindow" | Blend with the content behind the window. |
+----------------+-------------------------------------------+
| "withinWindow" | Blend with the content within the window. |
+----------------+-------------------------------------------+
### PopUpButton
A button which, when selected, displays a list of items for the user to choose from.::

from vanilla import *

class PopUpButtonDemo(object):

def __init__(self):
self.w = Window((100, 40))
self.w.popUpButton = PopUpButton((10, 10, -10, 20),
  ["A", "B", "C"],
  callback=self.popUpButtonCallback)
self.w.open()

def popUpButtonCallback(self, sender):
print "pop up button selection!", sender.get()

PopUpButtonDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and
size of the pop up button. The size of the button sould match the appropriate value
for the given *sizeStyle*.

+-------------------------+
| **Standard Dimensions** |
+---------+---+-----------+
| Regular | H | 20|
+---------+---+-----------+
| Small   | H | 17|
+---------+---+-----------+
| Mini| H | 15|
+---------+---+-----------+

**items** A list of items to appear in the pop up list.

**callback** The method to be called when the user selects an item in the pop up list.

**sizeStyle** A string representing the desired size style of the pop up button. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### ImageListCell
**horizontalAlignment** A string representing the desired horizontal
alignment of the image in the view. The options are:

+-------------+-------------------------+
| "left"  | Image is aligned left.  |
+-------------+-------------------------+
| "right" | Image is aligned right. |
+-------------+-------------------------+
| "center"| Image is centered.  |
+-------------+-------------------------+

**verticalAlignment** A string representing the desired vertical alignment
of the image in the view. The options are:

+-------------+--------------------------+
| "top"   | Image is aligned top.|
+-------------+--------------------------+
| "bottom"| Image is aligned bottom. |
+-------------+--------------------------+
| "center"| Image is centered.   |
+-------------+--------------------------+

**scale** A string representing the desired scale style of the image in the
view. The options are:

+----------------+----------------------------------------------+
| "porportional" | Proportionally scale the image to fit in the |
|| view if it is larger than the view.  |
+----------------+----------------------------------------------+
| "fit"  | Distort the proportions of the image until   |
|| it fits exactly in the view. |
+----------------+----------------------------------------------+
| "none" | Do not scale the image.  |
+----------------+----------------------------------------------+

Example::

from AppKit import *
from vanilla import *

class ImageListCellDemo(object):

def __init__(self):
self.w = Window((100, 100))
self.w.myList = List((0, 0, -0, -0),
[
{"image": NSImage.imageNamed_("NSActionTemplate")},
{"image": NSImage.imageNamed_("NSRefreshTemplate")}
],
columnDescriptions=[
{"title": "image", "cell": ImageListCell()}
])
self.w.open()

ImageListCellDemo()
### VanillaBaseControl
### EditText
Standard short text entry control.::

from vanilla import *

class EditTextDemo(object):

def __init__(self):
self.w = Window((100, 42))
self.w.editText = EditText((10, 10, -10, 22),
callback=self.editTextCallback)
self.w.open()

def editTextCallback(self, sender):
print "text entry!", sender.get()

EditTextDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the text entry control.

+-------------------------+
| **Standard Dimensions** |
+---------+---+-----------+
| Regular | H | 22|
+---------+---+-----------+
| Small   | H | 19|
+---------+---+-----------+
| Mini| H | 16|
+---------+---+-----------+

**text** An object representing the contents of the text entry control. If no formatter has been assigned to the control,
this should be a string. If a formatter has been assigned, this should be an object of the type that the formatter expects.

**callback** The method to be called when the user enters text.

**continuous** If True, the callback (if any) will be called upon each keystroke, if False, only call the callback when
editing finishes. Default is True.

**readOnly** Boolean representing if the text can be edited or not.

**formatter** An `NSFormatter <http://developer.apple.com/documentation/Cocoa/Reference/Foundation/Classes/NSFormatter_Class/index.html>`_
for controlling the display and input of the text entry.

**placeholder** A placeholder string to be shown when the text entry control is empty.

**sizeStyle** A string representing the desired size style of the text entry control. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### Tabs
A drawer attached to a window. Drawers are capable of containing controls.

To add a control to a tab, simply set it as an attribute of the tab.::

from vanilla import *

class TabDemo(object):

def __init__(self):
self.w = Window((250, 100))
self.w.tabs = Tabs((10, 10, -10, -10), ["Tab One", "Tab Two"])
tab1 = self.w.tabs[0]
tab1.text = TextBox((10, 10, -10, -10), "This is tab 1")
tab2 = self.w.tabs[1]
tab2.text = TextBox((10, 10, -10, -10), "This is tab 2")
self.w.open()

TabDemo()

No special naming is required for the attributes. However, each attribute
must have a unique name.

To retrieve a particular tab, access it by index:::

myTab = self.w.tabs[0]


**posSize** Tuple of form *(left, top, width, height)* representing the position
and size of the tabs.

**titles** An ordered list of tab titles.

**callback** The method to be called when the user selects a new tab.

**sizeStyle** A string representing the desired size style of the tabs.
The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### CheckBoxListCell
An object that displays a check box in a List column.

**This object should only be used in the *columnDescriptions*
argument during the construction of a List.**

**title** The title to be set in *all* items in the List column.

Example::

from vanilla import *

class CheckBoxListCellDemo(object):

def __init__(self):
self.w = Window((100, 100))
self.w.myList = List((0, 0, -0, -0),
 [{"value": True}, {"value": False}],
 columnDescriptions=[{"title": "value", "cell": CheckBoxListCell()}],
 editCallback=self.editCallback)
self.w.open()

def editCallback(self, sender):
print sender.get()

CheckBoxListCellDemo()
### Window
A window capable of containing controls.

To add a control to a window, simply set it as an attribute of the window.::

from vanilla import *

class WindowDemo(object):

def __init__(self):
self.w = Window((200, 70), "Window Demo")
self.w.myButton = Button((10, 10, -10, 20), "My Button")
self.w.myTextBox = TextBox((10, 40, -10, 17), "My Text Box")
self.w.open()

WindowDemo()

No special naming is required for the attributes. However, each attribute
must have a unique name.

**posSize** Tuple of form *(left, top, width, height)* representing the position and
size of the window. It may also be a tuple of form *(width, height)*. In this case,
the window will be positioned on screen automatically.

**title** The title to be set in the title bar of the window.

**minSize** Tuple of the form *(width, height)* representing the minimum size that
the window can be resized to.

**maxSize** Tuple of the form *(width, height)* representing the maximum size that
the window can be resized to.

**textured** Boolean value representing if the window should have a textured
appearance or not.

**autosaveName** A string representing a unique name for the window. If given,
this name will be used to store the window position and size in the application preferences.

**closable** Boolean value representing if the window should have a close button in the
title bar.

**miniaturizable** Boolean value representing if the window should have a minimize button
in the title bar.

**initiallyVisible** Boolean value representing if the window will be initially visible.
Default is *True*. If *False*, you can show the window later by calling `window.show()`.

**fullScreenMode** An indication of the full screen mode. These are the options:

+---------------+---------------------------------------------------------------+
| *None*| The window does not allow full screen.|
+---------------+---------------------------------------------------------------+
| *"primary"*   | Corresponds to NSWindowCollectionBehaviorFullScreenPrimary.   |
+---------------+---------------------------------------------------------------+
| *"auxiliary"* | Corresponds to NSWindowCollectionBehaviorFullScreenAuxiliary. |
+---------------+---------------------------------------------------------------+

**titleVisible** Boolean value indicating if the window title should be displayed.

**fullSizeContentView** Boolean value indicating if the content view should be the
full size of the window, including the area underneath the titlebar and toolbar.

**screen** A `NSScreen <http://tinyurl.com/NSScreen>`_ object indicating the screen that
the window should be drawn to. When None the window will be drawn to the main screen.
### RadioGroup
A collection of radio buttons.::

from vanilla import *

class RadioGroupDemo(object):

def __init__(self):
self.w = Window((100, 60))
self.w.radioGroup = RadioGroup((10, 10, -10, 40),
["Option 1", "Option 2"],
callback=self.radioGroupCallback)
self.w.open()

def radioGroupCallback(self, sender):
print "radio group edit!", sender.get()

RadioGroupDemo()

**posSize** Tuple of form *(left, top, width, height)* representing
the position and size of the radio group.

**titles** A list of titles to be shown next to the radio buttons.

**isVertical** Boolean representing if the radio group is
vertical or horizontal.

**callback** The method to be caled when a radio button is selected.

**sizeStyle** A string representing the desired size style of the radio group.
The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### Popover
A popover capable of containing controls.

**size** Tuple of form *(width, height)* representing the size of the content
in the popover.

**size** The parent view that the popover should pop out from. This can be either
a vanilla object or an instance of NSView or NSView subclass.

**preferredEdge** The edge of the parent view that you want the popover
to pop out from. These are the options:
+------------+
| *"left"*   |
+------------+
| *"right"*  |
+------------+
| *"top"*|
+------------+
| *"bottom"* |
+------------+

**behavior** The desired behavior of the popover. These are the options:
+------------------------+-----------------------------------------------------+
| *"applicationDefined"* | Corresponds to NSPopoverBehaviorApplicationDefined. |
+------------------------+-----------------------------------------------------+
| *"transient"*  | Corresponds to NSPopoverBehaviorTransient.  |
+------------------------+-----------------------------------------------------+
| *"semitransient"*  | Corresponds to NSPopoverBehaviorSemitransient.  |
+------------------------+-----------------------------------------------------+
### Sheet
A window that is attached to another window.

To add a control to a sheet, simply set it as an attribute of the sheet.::

from vanilla import *

class SheetDemo(object):

def __init__(self, parentWindow):
self.w = Sheet((200, 70), parentWindow)
self.w.myButton = Button((10, 10, -10, 20), "My Button")
self.w.myTextBox = TextBox((10, 40, -10, 17), "My Text Box")
self.w.open()

SheetDemo()

No special naming is required for the attributes. However, each attribute
must have a unique name.

**posSize** Tuple of form *(width, height)* representing the size of the sheet.

**parentWindow** The window that the sheet should be attached to.

**minSize** Tuple of the form *(width, height)* representing the minimum size that
the sheet can be resized to.

**maxSize** Tuple of the form *(width, height)* representing the maximum size that
the sheet can be resized to.

**autosaveName** A string representing a unique name for the sheet. If given,
this name will be used to store the sheet size in the application preferences.
### SegmentedButtonListCell
**segmentDescriptions** An ordered list of dictionaries describing the segments.

+------------------------+--------------------------------------------------------------------------------------------------+
| title (optional)   | The title of the segment.|
+------------------------+--------------------------------------------------------------------------------------------------+
| imagePath (optional)   | A file path to an image to display in the segment.   |
+------------------------+--------------------------------------------------------------------------------------------------+
| imageNamed (optional)  | The name of an image already loaded as a *NSImage* by the application to display in the segment. |
+------------------------+--------------------------------------------------------------------------------------------------+
| imageObject (optional) | A *NSImage* object to display in the segment.|
+------------------------+--------------------------------------------------------------------------------------------------+

Note: when using this cell in a List, the `binding` in the
column description must be set to `selectedIndex`.

Example::

from vanilla import *

class SegmentedButtonListCellDemo(object):

def __init__(self):
self.w = Window((100, 100))
self.w.myList = List((0, 0, -0, -0),
[{"value": 0}, {"value": 1}],
columnDescriptions=[
{
"title": "value",
"cell": SegmentedButtonListCell([dict(title="0"), dict(title="1")]),
"binding": "selectedIndex"
}
],
editCallback=self.editCallback)
self.w.open()

def editCallback(self, sender):
print sender.get()

SegmentedButtonListCellDemo()
### ColorWell
A control that allows for showing and choosing a color value.

ColorWell objects handle
`NSColor <http://developer.apple.com/documentation/Cocoa/Reference/ApplicationKit/Classes/NSColor_Class/index.html>`_
objects.::
from AppKit import NSColor
from vanilla import *

class ColorWellDemo(object):

def __init__(self):
self.w = Window((100, 50))
self.w.colorWell = ColorWell((10, 10, -10, -10),
callback=self.colorWellEdit,
color=NSColor.redColor())
self.w.open()

def colorWellEdit(self, sender):
print "color well edit!", sender.get()

ColorWellDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the color well.

**callback** The method to be caled when the user selects a new color.

**color** A *NSColor* object. If *None* is given, the color shown will be white.
### HorizontalLine
A horizontal line.::

from vanilla import *

class HorizontalLineDemo(object):

def __init__(self):
self.w = Window((100, 20))
self.w.line = HorizontalLine((10, 10, -10, 1))
self.w.open()

HorizontalLineDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the line.

+-------------------------+
| **Standard Dimensions** |
+---+---------------------+
| H | 1   |
+---+---------------------+
### HelpButton
A standard help button.::

from vanilla import *

class HelpButtonDemo(object):

 def __init__(self):
 self.w = Window((90, 40))
 self.w.button = HelpButton((10, 10, 21, 20),
callback=self.buttonCallback)
 self.w.open()

 def buttonCallback(self, sender):
 print "help button hit!"

HelpButtonDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and
size of the button. The size of the button sould match the standard dimensions.

+-------------------------+
| **Standard Dimensions** |
+--------+----------------+
| Width  | 21 |
+--------+----------------+
| Height | 20 |
+--------+----------------+

**callback** The method to be called when the user presses the button.
### getAxisInfo
### Drawer
A drawer attached to a window. Drawers are capable of containing controls.

To add a control to a drawer, simply set it as an attribute of the drawer.::

from vanilla import *

class DrawerDemo(object):

def __init__(self):
self.w = Window((200, 200))
self.w.button = Button((10, 10, -10, 20), "Toggle Drawer",
callback=self.toggleDrawer)
self.d = Drawer((100, 150), self.w)
self.d.textBox = TextBox((10, 10, -10, -10),
"This is a drawer.")
self.w.open()
self.d.open()

def toggleDrawer(self, sender):
self.d.toggle()

DrawerDemo()

No special naming is required for the attributes. However, each attribute must have a unique name.

**size** Tuple of form *(width, height)* representing the size of the drawer.

**parentWindow** The window that the drawer should be attached to.

**minSize** Tuple of form *(width, height)* representing the minimum size of the drawer.

**maxSize** Tuple of form *(width, height)* representing the maximum size of the drawer.

**preferredEdge** The preferred edge of the window that the drawe should be attached to. If the
drawer cannot be opened on the preferred edge, it will be opened on the opposite edge. The options are:

+----------+
| "left"   |
+----------+
| "right"  |
+----------+
| "top"|
+----------+
| "bottom" |
+----------+

**forceEdge** Boolean representing if the drawer should *always* be opened on the preferred edge.

**leadingOffset** Distance between the top or left edge of the drawer and the parent window.

**trailingOffset** Distance between the bottom or right edge of the drawer and the parent window.
### intToTag
### ComboBox
A text entry control that allows direct text entry or selection for a list of options.::

from vanilla import *

class ComboBoxDemo(object):

def __init__(self):
self.w = Window((100, 41))
self.w.comboBox = ComboBox((10, 10, -10, 21),
["AA", "BB", "CC", "DD"],
callback=self.comboBoxCallback)
self.w.open()

def comboBoxCallback(self, sender):
print "combo box entry!", sender.get()

ComboBoxDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the
combo box control. The size of the combo box sould match the appropriate value for the given *sizeStyle*.

+-------------------------+
| **Standard Dimensions** |
+---------+---+-----------+
| Regular | H | 21|
+---------+---+-----------+
| Small   | H | 17|
+---------+---+-----------+
| Mini| H | 14|
+---------+---+-----------+

**items** The items to be displayed in the combo box.

**completes** Boolean representing if the combo box auto completes entered text.

**continuous** If True, the callback (if any) will be called upon each keystroke, if False, only call the callback when
editing finishes or after item selection. Default is False.

**callback** The method to be called when the user enters text.

**formatter** An `NSFormatter <http://developer.apple.com/documentation/Cocoa/Reference/Foundation/Classes/NSFormatter_Class/index.html>`_
for controlling the display and input of the combo box.

**sizeStyle** A string representing the desired size style of the combo box. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### SecureEditText
Standard secure text entry control.::

from vanilla import *

class SecureEditTextDemo(object):

def __init__(self):
self.w = Window((100, 42))
self.w.secureEditText = SecureEditText((10, 10, -10, 22),
callback=self.secureEditTextCallback)
self.w.open()

def secureEditTextCallback(self, sender):
print "text entry!", sender.get()

SecureEditTextDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the text entry control.

+-------------------------+
| **Standard Dimensions** |
+---------+---+-----------+
| Regular | H | 22|
+---------+---+-----------+
| Small   | H | 19|
+---------+---+-----------+
| Mini| H | 16|
+---------+---+-----------+

**text** An object representing the contents of the text entry control. If no formatter has been assigned to the control,
this should be a string. If a formatter has been assigned, this should be an object of the type that the formatter expects.

**callback** The method to be called when the user enters text.

**continuous** If True, the callback (if any) will be called upon each keystroke, if False, only call the callback when
editing finishes. Default is True.

**readOnly** Boolean representing if the text can be edited or not.

**formatter** An `NSFormatter <http://developer.apple.com/documentation/Cocoa/Reference/Foundation/Classes/NSFormatter_Class/index.html>`_
for controlling the display and input of the text entry.

**placeholder** A placeholder string to be shown when the text entry control is empty.

**sizeStyle** A string representing the desired size style of the text entry control. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### ActionButton
An Action Button with a menu.

from vanilla import *

class ActionPopUpButtonDemo(object):

def __init__(self):
self.w = Window((100, 40))

items = [
dict(title="first", callback=self.firstCallback),
dict(title="second", callback=self.secondCallback),
dict(title="third", items=[
dict(title="sub first", callback=self.subFirstCallback)
])
]

self.w.actionPopUpButton = ActionButton((10, 10, 30, 20),
  items,
  )
self.w.open()

def firstCallback(self, sender):
print "first"

def secondCallback(self, sender):
print "second"

def subFirstCallback(self, sender):
print "sub first"

ActionPopUpButtonDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and
size of the pop up button. The size of the button sould match the appropriate value
for the given *sizeStyle*.

+-------------------------+
| **Standard Dimensions** |
+---------+---+-----------+
| Regular | H | 20|
+---------+---+-----------+
| Small   | H | 17|
+---------+---+-----------+
| Mini| H | 15|
+---------+---+-----------+

**items** A list of items to appear in the pop up list as dictionaries. Optionally an item could be a NSMenuItem. 
when an item is set to "----" will be a menu item separator.

+------------+--------------------------------------------------------------------------------+
| "title"*   | The title of the item. |
+------------+--------------------------------------------------------------------------------+
| "callback" | The callback fo the item.  |
+------------+--------------------------------------------------------------------------------+
| "items"| Each item could have sub menu's, as list of dictionaries with the same format. |
+------------+--------------------------------------------------------------------------------+

**sizeStyle** A string representing the desired size style of the pop up button. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+

**bordered** Boolean representing if the button should be bordered.
### Slider
A standard slider control. Sliders can be vertical or horizontal and
they can show tick marks or not show tick marks.::

from vanilla import *

class SliderDemo(object):

 def __init__(self):
 self.w = Window((200, 43))
 self.w.slider = Slider((10, 10, -10, 23),
tickMarkCount=10,
callback=self.sliderCallback)
 self.w.open()

 def sliderCallback(self, sender):
 print "slider edit!", sender.get()

SliderDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and
size of the slider. The size of the slider sould match the appropriate value for
the given *sizeStyle*.

+---------------------------+
| **Standard Dimensions**   |
+---------------------------+
| *without ticks*   |
+---------+---+----+---+----+
| Regular | W | 15 | H | 15 |
+---------+---+----+---+----+
| Small   | W | 12 | H | 11 |
+---------+---+----+---+----+
| Mini| W | 10 | H | 10 |
+---------+---+----+---+----+
| *with ticks*  |
+---------+---+----+---+----+
| Regular | W | 24 | H | 23 |
+---------+---+----+---+----+
| Small   | W | 17 | H | 17 |
+---------+---+----+---+----+
| Mini| W | 16 | H | 16 |
+---------+---+----+---+----+

**minValue** The minimum value allowed by the slider.

**maxValue** The maximum value allowed by the slider.

**value** The initial value of the slider.

**tickMarkCount** The number of tick marcks to be displayed on the slider.
If *None* is given, no tick marks will be displayed.

**stopOnTickMarks** Boolean representing if the slider knob should only
stop on the tick marks.

**continuous** Boolean representing if the assigned callback should be
called during slider editing. If *False* is given, the callback will be
called after the editing has finished.

**callback** The method to be called when the slider has been edited.

**sizeStyle** A string representing the desired size style of the slider.
The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### SplitView2
View that can be split into two or more subviews with dividers.::

from vanilla import *

class SplitViewDemo(object):

def __init__(self):
self.w = Window((200, 200), "SplitView Demo", minSize=(100, 100))
list1 = List((0, 0, -0, 100), ["A", "B", "C"])
list2 = List((0, 0, -0, 100), ["a", "b", "c"])
paneDescriptors = [
dict(view=list1, identifier="pane1"),
dict(view=list2, identifier="pane2"),
]
self.w.splitView = SplitView((0, 0, -0, -0), paneDescriptors)
self.w.open()

SplitViewDemo()

**posSize** Tuple of form *(left, top, width, height)* representing
the position and size of the split view.

**paneDescriptions** An ordered list of dictionaries describing the
subviews, or "panes". Those dictionaries can have the following keys:

+-----------------------+-----------------------------------------------------------------------------+
| *view*| A view, either a Vanilla object or a NSView. Required.  |
+-----------------------+-----------------------------------------------------------------------------+
| *"identifier"*| A string identifying the pane. Required.|
+-----------------------+-----------------------------------------------------------------------------+
| *"size"*  | The initial size of the pane. Optional. |
+-----------------------+-----------------------------------------------------------------------------+
| *"minSize"*   | The minimum size of the pane. Optional. The default is 0.   |
+-----------------------+-----------------------------------------------------------------------------+
| *"maxSize"*   | The maximum size of the pane. Optional. The default is no maximum size. |
+-----------------------+-----------------------------------------------------------------------------+
| *"canCollapse"*   | Boolean indicating if the pane can collapse. Optional. The default is True. |
+-----------------------+-----------------------------------------------------------------------------+
| *"resizeFlexibility"* | Boolean indicating if the pane can adjust its size automatically when the   |
|   | SplitView size changes. Optional. The default is True unless the pane has a |
|   | fixed size. |
+-----------------------+-----------------------------------------------------------------------------+

**isVertical** Boolean representing if the split view is vertical.
Default is *True*.

**dividerStyle** String representing the style of the divider.
These are the options:
+----------+
| splitter |
+----------+
| thin |
+----------+
| thick|
+----------+
| None |
+----------+

**dividerThickness** An integer representing the desired thickness of the divider.

**dividerColor** A NSColor that should be used to paint the divider.

**autosaveName** The autosave name for the SplitView.
### VarFontTextEditor
### Box
A bordered container for other controls.

To add a control to a box, simply set it as an attribute of the box.::

from vanilla import *

class BoxDemo(object):

def __init__(self):
self.w = Window((150, 70))
self.w.box = Box((10, 10, -10, -10))
self.w.box.text = TextBox((10, 10, -10, -10), "This is a box")
self.w.open()

BoxDemo()

No special naming is required for the attributes. However, each attribute must have a unique name.

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the box.

**title** The title to be displayed dabove the box. Pass *None* if no title is desired.
### GradientButton
### LevelIndicatorListCell
An object that displays a level indicator in a List column.

**This object should only be used in the *columnDescriptions* argument
during the construction of a List.**::

from vanilla import *

class LevelIndicatorListCellDemo(object):

 def __init__(self):
 self.w = Window((340, 140))
 items = [
 {"discrete": 3, "continuous": 4, "rating": 1, "relevancy": 9},
 {"discrete": 8, "continuous": 3, "rating": 5, "relevancy": 5},
 {"discrete": 3, "continuous": 7, "rating": 3, "relevancy": 4},
 {"discrete": 2, "continuous": 5, "rating": 4, "relevancy": 7},
 {"discrete": 6, "continuous": 9, "rating": 3, "relevancy": 2},
 {"discrete": 4, "continuous": 0, "rating": 6, "relevancy": 8},
 ]
 columnDescriptions = [
 {"title": "discrete",
 "cell": LevelIndicatorListCell(style="discrete", warningValue=7, criticalValue=9)},
 {"title": "continuous", 
 "cell": LevelIndicatorListCell(style="continuous", warningValue=7, criticalValue=9)},
 {"title": "rating",
 "cell": LevelIndicatorListCell(style="rating", maxValue=6)},
 {"title": "relevancy",
 "cell": LevelIndicatorListCell(style="relevancy")},
 ]
 self.w.list = List((0, 0, -0, -0), items=items,
columnDescriptions=columnDescriptions)
 self.w.open()

LevelIndicatorListCellDemo()

**style** The style of the level indicator. The options are:

+--------------+-----------------------------------------+
| "continuous" | A continuous bar.   |
+--------------+-----------------------------------------+
| "discrete"   | A segmented bar.|
+--------------+-----------------------------------------+
| "rating" | A row of stars. Similar to the rating   |
|  | indicator in iTunes.|
+--------------+-----------------------------------------+
| "relevancy"  | A row of lines. Similar to the search   |
|  | result relevancy indicator in Mail. |
+--------------+-----------------------------------------+

**minValue** The minimum value allowed by the level indicator.

**maxValue** The maximum value allowed by the level indicator.

**warningValue** The value at which the filled portions of the
level indicator should display the warning color. Applies only to
discrete and continuous level indicators.

**criticalValue** The value at which the filled portions of the
level indicator should display the critical color. Applies only to
discrete and continuous level indicators.
### HUDFloatingWindow
A window that floats above all other windows and has the HUD appearance.

To add a control to a window, simply set it as an attribute of the window.

from vanilla import *

class HUDFloatingWindowDemo(object):

def __init__(self):
self.w = HUDFloatingWindow((200, 70), "HUDFloatingWindow Demo")
self.w.myButton = Button((10, 10, -10, 20), "My Button")
self.w.myTextBox = TextBox((10, 40, -10, 17), "My Text Box")
self.w.open()

HUDFloatingWindowDemo()

No special naming is required for the attributes. However, each attribute
must have a unique name.

**posSize** Tuple of form *(left, top, width, height)* representing the position
and size of the window. It may also be a tuple of form *(width, height)*.
In this case, the window will be positioned on screen automatically.

**title** The title to be set in the title bar of the window.

**minSize** Tuple of the form *(width, height)* representing the minimum size
that the window can be resized to.

**maxSize** Tuple of the form *(width, height)* representing the maximum size
that the window can be resized to.

**textured** Boolean value representing if the window should have a textured
appearance or not.

**autosaveName** A string representing a unique name for the window. If given,
this name will be used to store the window position and size in the application
preferences.

**closable** Boolean value representing if the window should have a close button
in the title bar.

**screen** A `NSScreen <http://tinyurl.com/NSScreen>`_ object indicating the screen that
the window should be drawn to. When None the window will be drawn to the main screen.
### List
A control that shows a list of items. These lists can contain one or more columns.

A single column example::

from vanilla import *

class ListDemo(object):

def __init__(self):
self.w = Window((100, 100))
self.w.myList = List((0, 0, -0, -0), ["A", "B", "C"],
 selectionCallback=self.selectionCallback)
self.w.open()

def selectionCallback(self, sender):
print sender.getSelection()

ListDemo()

A mutliple column example::

from vanilla import *

class ListDemo(object):

def __init__(self):
self.w = Window((100, 100))
self.w.myList = List((0, 0, -0, -0),
 [{"One": "A", "Two": "a"}, {"One": "B", "Two": "b"}],
 columnDescriptions=[{"title": "One"}, {"title": "Two"}],
 selectionCallback=self.selectionCallback)
self.w.open()

def selectionCallback(self, sender):
print sender.getSelection()

ListDemo()

List objects behave like standard Python lists. For xample, given this List:::

self.w.myList = List((10, 10, 200, 100), ["A", "B", "C"])

The following Python list methods work:::

# Getting the length of the List.
>>> len(self.w.myList)
3

# Retrieving an item or items from a List.
>>> self.w.myList[1]
"B"
>>> self.w.myList[:2]
["A", "B"]

# Setting an item in a List.
>>> self.w.myList[1] = "XYZ"
>>> self.w.myList.get()
["A", "XYZ", "C"]

# Deleting an item at an index in a List.
>>> del self.w.myList[1]
>>> self.w.myList.get()
["A", "C"]

# Appending an item to a List.
>>> self.w.myList.append("Z")
>>> self.w.myList.get()
["A", "B", "C", "Z"]

# Removing the first occurance of an item in a List.
>>> self.w.myList.remove("A")
>>> self.w.myList.get()
["B", "C"]

# Getting the index for the first occurance of an item in a List.
>>> self.w.myList.index("B")
1

# Inserting an item into a List.
>>> self.w.myList.insert(1, "XYZ")
>>> self.w.myList.get()
["A", "XYZ", "B", "C"]

# Extending a List.
>>> self.w.myList.extend(["X", "Y", "Z"])
>>> self.w.myList.get()
["A", "B", "C", "X", "Y", "Z"]

# Iterating over a List.
>>> for i in self.w.myList:
>>> i
"A"
"B"
"C"

**posSize** Tuple of form *(left, top, width, height)* representing the
position and size of the list.

**items** The items to be displayed in the list. In the case of multiple
column lists, this should be a list of dictionaries with the data for
each column keyed by the column key as defined in columnDescriptions.
If you intend to use a dataSource, *items* must be *None*.

**dataSource** A Cocoa object supporting the *NSTableDataSource*
protocol. If *dataSource* is given, *items* must be *None*.

**columnDescriptions** An ordered list of dictionaries describing the
columns. This is only necessary for multiple column lists.

+--------------------------------+--------------------------------------------------------------------------------+
| *"title"*  | The title to appear in the column header.  |
+--------------------------------+--------------------------------------------------------------------------------+
| *"key"* (optional) | The key from which this column should get  |
|| its data from each dictionary in *items*. If   |
|| nothing is given, the key will be the string   |
|| given in *title*.  |
+--------------------------------+--------------------------------------------------------------------------------+
| *"formatter"* (optional)   | An `NSFormatter` <http://tinyurl.com/NSFormatter>`_|
|| for cntrolling the display and input of the|
|| column's cells.|
+--------------------------------+--------------------------------------------------------------------------------+
| *"cell"* (optional)| A cell type to be displayed in the column. |
|| If nothing is given, a text cell is used.  |
+--------------------------------+--------------------------------------------------------------------------------+
| *"editable"* (optional)| Enable or disable editing in the column. If|
|| nothing is given, it will follow the   |
|| editability of the rest of the list.   |
+--------------------------------+--------------------------------------------------------------------------------+
| *"width"* (optional)   | The width of the column.   |
+--------------------------------+--------------------------------------------------------------------------------+
| *"minWidth"* (optional)| The minimum width of the column. The fallback is `width`.  |
+--------------------------------+--------------------------------------------------------------------------------+
| *"maxWidth"* (optional)| The maximum width of the column. The fallback is `width`.  |
+--------------------------------+--------------------------------------------------------------------------------+
| *"allowsSorting"* (optional)   | A boolean representing that this column allows the user|
|| to sort the table by clicking the column's header. |
|| The fallback is `True`. If a List is set to disallow   |
|| sorting the column level settings will be ignored  |
+--------------------------------+--------------------------------------------------------------------------------+
| *"typingSensitive"* (optional) | A boolean representing that this column|
|| should be the column that responds to user |
|| key input. Only one column can be flagged as   |
|| True. If no column is flagged, the first   |
|| column will automatically be flagged.  |
+--------------------------------+--------------------------------------------------------------------------------+
| *binding* (optional)   | A string indicating which `binding object <http://tinyurl.com/CocoaBindings>`_ |
|| the column's cell should be bound to. By   |
|| default, this is "value." You should only  |
|| override this in very specific cases.  |
+--------------------------------+--------------------------------------------------------------------------------+

**showColumnTitles** Boolean representing if the column titles should be shown or not.
Column titles will not be shown in single column lists.

**selectionCallback** Callback to be called when the selection in the list changes.

**doubleClickCallback** Callback to be called when an item is double clicked.

**editCallback** Callback to be called after an item has been edited.

**enableDelete** A boolean representing if items in the list can be deleted via the interface.

**enableTypingSensitivity** A boolean representing if typing in the list will jump to the
closest match as the entered keystrokes. *Available only in single column lists.*

**allowsMultipleSelection** A boolean representing if the list allows more than one item to be selected.

**allowsEmptySelection** A boolean representing if the list allows zero items to be selected.

**allowsSorting** A boolean indicating if the list allows user sorting by clicking column headers.

**drawVerticalLines** Boolean representing if vertical lines should be drawn in the list.

**drawHorizontalLines** Boolean representing if horizontal lines should be drawn in the list.

**drawFocusRing** Boolean representing if the standard focus ring should be drawn when the list is selected.

**rowHeight** The height of the rows in the list.

**autohidesScrollers** Boolean representing if scrollbars should automatically be hidden if possible.

**selfDropSettings** A dictionary defining the drop settings when the source of the drop
is this list. The dictionary form is described below.

**selfWindowDropSettings** A dictionary defining the drop settings when the source of the drop
is contained the same document as this list. The dictionary form is described below.

**selfDocumentDropSettings** A dictionary defining the drop settings when the source of the drop
is contained the same window as this list. The dictionary form is described below.

**selfApplicationDropSettings** A dictionary defining the drop settings when the source of the drop
is contained the same application as this list. The dictionary form is described below.

**otherApplicationDropSettings** A dictionary defining the drop settings when the source of the drop
is contained an application other than the one that contains this list. The dictionary form is described below.

The drop settings dictionaries should be of this form:

+-----------------------------------+--------------------------------------------------------------------+
| *type*| A single drop type indicating what drop types the list accepts.|
|   | For example, NSFilenamesPboardType or "MyCustomPboardType".|
+-----------------------------------+--------------------------------------------------------------------+
| *operation* (optional)| A "drag operation <http://tinyurl.com/NSDraggingIn>`_ that |
|   | the list accepts. The default is *NSDragOperationCopy*.|
+-----------------------------------+--------------------------------------------------------------------+
| *allowDropBetweenRows* (optional) | A boolean indicating if the list accepts drops between rows.   |
|   | The default is True.   |
+-----------------------------------+--------------------------------------------------------------------+
| *allowDropOnRow* (optional)   | A boolean indicating if the list accepts drops on rows.|
|   | The default is False.  |
+-----------------------------------+--------------------------------------------------------------------+
| *callback*| Callback to be called when a drop is proposed and when a drop  |
|   | is to occur. This method should return a boolean representing  |
|   | if the drop is acceptable or not. This method must accept *sender* |
|   | and *dropInfo* arguments. The _dropInfo_ will be a dictionary as   |
|   | described below.   |
+-----------------------------------+--------------------------------------------------------------------+

The dropInfo dictionary passed to drop callbacks will be of this form:

+--------------+--------------------------------------------------------------------------------------------+
| *data*   | The data proposed for the drop. This data will be of the type specified by dropDataFormat. |
+--------------+--------------------------------------------------------------------------------------------+
| *rowIndex*   | The row where the drop is proposed.|
+--------------+--------------------------------------------------------------------------------------------+
| *source* | The source from which items are being dragged. If this object is wrapped by Vanilla, the   |
|  | Vanilla object will be passed as the source.   |
+--------------+--------------------------------------------------------------------------------------------+
| *dropOnRow*  | A boolean representing if the row is being dropped on. If this is False, the drop should   |
|  | occur between rows.|
+--------------+--------------------------------------------------------------------------------------------+
| *isProposal* | A boolean representing if this call is simply proposing the drop or if it is time to   |
|  | accept the drop.   |
+--------------+--------------------------------------------------------------------------------------------+
### ImageView
A view that displays an image.

**posSize** Tuple of form *(left, top, width, height)* representing
the position and size of the view.

**horizontalAlignment** A string representing the desired horizontal
alignment of the image in the view. The options are:

+-------------+-------------------------+
| "left"  | Image is aligned left.  |
+-------------+-------------------------+
| "right" | Image is aligned right. |
+-------------+-------------------------+
| "center"| Image is centered.  |
+-------------+-------------------------+

**verticalAlignment** A string representing the desired vertical alignment
of the image in the view. The options are:

+-------------+--------------------------+
| "top"   | Image is aligned top.|
+-------------+--------------------------+
| "bottom"| Image is aligned bottom. |
+-------------+--------------------------+
| "center"| Image is centered.   |
+-------------+--------------------------+

**scale** A string representing the desired scale style of the image in the
view. The options are:

+----------------+----------------------------------------------+
| "porportional" | Proportionally scale the image to fit in the |
|| view if it is larger than the view.  |
+----------------+----------------------------------------------+
| "fit"  | Distort the proportions of the image until   |
|| it fits exactly in the view. |
+----------------+----------------------------------------------+
| "none" | Do not scale the image.  |
+----------------+----------------------------------------------+
### ScrollView
A view with scrollers for containing another view.::

from AppKit import NSView, NSColor, NSRectFill
from vanilla import *

class DemoView(NSView):

def drawRect_(self, rect):
NSColor.redColor().set()
NSRectFill(self.bounds())


class ScrollViewDemo(object):

def __init__(self):
self.w = Window((200, 200))
self.view = DemoView.alloc().init()
self.view.setFrame_(((0, 0), (300, 300)))
self.w.scrollView = ScrollView((10, 10, -10, -10),
self.view)
self.w.open()

ScrollViewDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the
position and size of the scroll view.

**nsView** A *NSView* object.

**hasHorizontalScroller** Boolean representing if the scroll view has
horizontal scrollers.

**hasVerticalScroller** Boolean representing if the scroll view has
vertical scrollers.

**autohidesScrollers** Boolean representing if the scroll view auto-hides
its scrollers.

**backgroundColor** A *NSColor* object representing the background
color of the scroll view.

**drawsBackground** Boolean representing if the background should be drawn.
### ProgressSpinner
An animated, spinning progress indicator.::

from vanilla import *

class ProgressSpinnerDemo(object):

def __init__(self):
self.w = Window((80, 52))
self.w.spinner = ProgressSpinner((24, 10, 32, 32),
displayWhenStopped=True)
self.w.spinner.start()
self.w.open()

ProgressSpinnerDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the
position and size of the spinner. The size of the spinner sould match the
appropriate value for the given *sizeStyle*.

+---------------------------+
| **Standard Dimensions**   |
+---------+---+----+---+----+
| Regular | W | 32 | H | 32 |
+---------+---+----+---+----+
| Small   | W | 16 | H | 16 |
+---------+---+----+---+----+

**displayWhenStopped** Boolean representing if the spiiner should be
displayed when it is not spinning.

**sizeStyle** A string representing the desired size style of the spinner.
The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
### Button
A standard button.::

from vanilla import *

class ButtonDemo(object):

 def __init__(self):
 self.w = Window((100, 40))
 self.w.button = Button((10, 10, -10, 20), "A Button",
callback=self.buttonCallback)
 self.w.open()

 def buttonCallback(self, sender):
 print "button hit!"

ButtonDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position
and size of the button. The size of the button sould match the appropriate value
for the given *sizeStyle*.

+-------------------------+
| **Standard Dimensions** |
+=========+===+===========+
| Regular | H | 20|
+---------+---+-----------+
| Small   | H | 17|
+---------+---+-----------+
| Mini| H | 14|
+---------+---+-----------+

**title** The text to be displayed on the button. Pass *None* is no title is desired.

**callback** The method to be called when the user presses the button.

**sizeStyle** A string representing the desired size style of the button. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### ObjectBrowser
An object browser.

**posSize** Tuple of form *(left, top, width, height)* representing the position and
size of the browser.

**obj** The object to be displayed.
### PathControl
A path control.

**posSize** Tuple of form *(left, top, width, height)* representing the position
and size of the control. The size of the control sould match the appropriate value
for the given *sizeStyle*.

+-------------------------+
| **Standard Dimensions** |
+=========+===+===========+
| Regular | H | 22|
+---------+---+-----------+
| Small   | H | 20|
+---------+---+-----------+
| Mini| H | 18|
+---------+---+-----------+

**url** The url to be displayed in the control. This should be a NSURL object.

**editable** A boolean indicating if this control is editable or not.

**callback** The method to be called when the user presses the control.

**sizeStyle** A string representing the desired size style of the button. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### TextEditor
Standard long text entry control.::

from vanilla import *

class TextEditorDemo(object):

def __init__(self):
self.w = Window((200, 200))
self.w.textEditor = TextEditor((10, 10, -10, 22),
callback=self.textEditorCallback)
self.w.open()

def textEditorCallback(self, sender):
print "text entry!", sender.get()

TextEditorDemo()

**posSize** Tuple of form *(left, top, width, height)* representing
the position and size of the text entry control.

**text** The text to be displayed in the text entry control.

**callback** The method to be called when the user presses the text
entry control.

**readOnly** Boolean representing if the text can be edited or not.

**checksSpelling** Boolean representing if spelling should be automatically
checked or not.
### getFont
### TextBox
A rectangle containing static text.::

from vanilla import *

class TextBoxDemo(object):

 def __init__(self):
 self.w = Window((100, 37))
 self.w.textBox = TextBox((10, 10, -10, 17), "A TextBox")
 self.w.open()

TextBoxDemo()

**posSize** Tuple of form *(left, top, width, height)* representing
the position and size of the text box.

+-------------------------+
| **Standard Dimensions** |
+---------+---+-----------+
| Regular | H | 17|
+---------+---+-----------+
| Small   | H | 14|
+---------+---+-----------+
| Mini| H | 12|
+---------+---+-----------+

**text** The text to be displayed in the text box. If the object is a
*NSAttributedString*, the attributes will be used for display.

**alignment** A string representing the desired visual alignment of the
text in the text box. The options are:

+-------------+-----------------------------------------------------+
| "left"  | Text is aligned left.   |
+-------------+-----------------------------------------------------+
| "right" | Text is aligned right.  |
+-------------+-----------------------------------------------------+
| "center"| Text is centered.   |
+-------------+-----------------------------------------------------+
| "justified" | Text is justified.  |
+-------------+-----------------------------------------------------+
| "natural"   | Follows the natural alignment of the text's script. |
+-------------+-----------------------------------------------------+

**selectable** Boolean representing if the text is selectable or not.

**sizeStyle** A string representing the desired size style of the button.
The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### SplitView
View that can be split into two or more subviews with dividers.::

from vanilla import *

class SplitViewDemo(object):

def __init__(self):
self.w = Window((200, 200), "SplitView Demo", minSize=(100, 100))
list1 = List((0, 0, -0, 100), ["A", "B", "C"])
list2 = List((0, 0, -0, 100), ["a", "b", "c"])
paneDescriptors = [
dict(view=list1, identifier="pane1"),
dict(view=list2, identifier="pane2"),
]
self.w.splitView = SplitView((0, 0, -0, -0), paneDescriptors)
self.w.open()

SplitViewDemo()

The wrapped object is an `RBSplitView <http://www.brockerhoff.net/src/rbs.html>`_ object.

**posSize** Tuple of form *(left, top, width, height)* representing
the position and size of the split view.

**paneDescriptions** An ordered list of dictionaries describing the
subviews, or "panes". Those dictionaries can have the following keys:

+-----------------+-----------------------------------------------------------------------------+
| *view*  | A view, either a Vanilla object or a NSView. Required.  |
+-----------------+-----------------------------------------------------------------------------+
| *"identifier"*  | A string identifying the pane. Required.|
+-----------------+-----------------------------------------------------------------------------+
| *"size"*| The initial size of the pane. Optional. |
+-----------------+-----------------------------------------------------------------------------+
| *"minSize"* | The minimum size of the pane. Optional. The default is 1.   |
+-----------------+-----------------------------------------------------------------------------+
| *"maxSize"* | The maximum size of the pane. Optional. The default is no maximum size. |
+-----------------+-----------------------------------------------------------------------------+
| *"canCollapse"* | Boolean indicating if the pane can collapse. Optional. The default is True. |
+-----------------+-----------------------------------------------------------------------------+

**isVertical** Boolean representing if the split view is vertical.
Default is *True*.
### ImageButton
A button with an image.::

from vanilla import *

class ImageButtonDemo(object):

 def __init__(self):
 path = "/path/to/an/image"
 self.w = Window((50, 50))
 self.w.button = ImageButton((10, 10, 30, 30), imagePath=path,
callback=self.buttonCallback)
 self.w.open()

 def buttonCallback(self, sender):
 print "button hit!"

ImageButtonDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the button.

**title** The text to be displayed on the button. Pass *None* is no title is desired.

**bordered** Boolean representing if the button should be bordered.

**imagePath** A file path to an image.

**imageNamed** The name of an image already load as a *NSImage* by the application.

**imageObject** A *NSImage* object.

*Only one of imagePath, imageNamed, imageObject should be set.*

**imagePosition** The position of the image relative to the title. The options are:

+----------+
| "top"|
+----------+
| "bottom" |
+----------+
| "left"   |
+----------+
| "right"  |
+----------+

**callback** The method to be called when the user presses the button.

**sizeStyle** A string representing the desired size style of the button. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### SquareButton
A standard square button.::

from vanilla import *

class SquareButtonDemo(object):

 def __init__(self):
 self.w = Window((200, 100))
 self.w.button = SquareButton((10, 10, -10, -10), "A Button",
callback=self.buttonCallback)
 self.w.open()

 def buttonCallback(self, sender):
 print "button hit!"

SquareButtonDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the button.

**title** The text to be displayed on the button. Pass _None_ is no title is desired.

**callback** The method to be called when the user presses the button.

**sizeStyle** A string representing the desired size style of the button. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### VanillaBaseObject
### SegmentedButton
A standard segmented button.::

from vanilla import *

class SegmentedButtonDemo(object):

 def __init__(self):
 self.w = Window((100, 40))
 self.w.button = SegmentedButton((10, 10, -10, 20),
 [dict(title="A"), dict(title="B"), dict(title="C")],
callback=self.buttonCallback)
 self.w.open()

 def buttonCallback(self, sender):
 print "button hit!"

SegmentedButtonDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position
and size of the segmented button. The size of the segmented button sould match
the appropriate value for the given *sizeStyle*.

+-------------------------+
| **Standard Dimensions** |
+=========+===+===========+
| Regular | H | 21|
+---------+---+-----------+
| Small   | H | 18|
+---------+---+-----------+
| Mini| H | 15|
+---------+---+-----------+

**segmentDescriptions** An ordered list of dictionaries describing the segments.

+------------------------+--------------------------------------------------------------------------------------------------+
| width (optional)   | The desired width of the segment.|
+------------------------+--------------------------------------------------------------------------------------------------+
| title (optional)   | The title of the segment.|
+------------------------+--------------------------------------------------------------------------------------------------+
| enabled (optional) | The enabled state of the segment. The default is `True`. |
+------------------------+--------------------------------------------------------------------------------------------------+
| imagePath (optional)   | A file path to an image to display in the segment.   |
+------------------------+--------------------------------------------------------------------------------------------------+
| imageNamed (optional)  | The name of an image already loaded as a *NSImage* by the application to display in the segment. |
+------------------------+--------------------------------------------------------------------------------------------------+
| imageObject (optional) | A *NSImage* object to display in the segment.|
+------------------------+--------------------------------------------------------------------------------------------------+

**callback** The method to be called when the user presses the segmented button.

**selectionStyle** The selection style in the segmented button.

+-----------+---------------------------------------------+
| one   | Only one segment may be selected.   |
+-----------+---------------------------------------------+
| any   | Any number of segments may be selected. |
+-----------+---------------------------------------------+
| momentary | A segmented is only selected when tracking. |
+-----------+---------------------------------------------+

**sizeStyle** A string representing the desired size style of the segmented button. The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### ProgressBar
A standard progress bar.::

from vanilla import *

class ProgressBarDemo(object):

def __init__(self):
self.w = Window((200, 65))
self.w.bar = ProgressBar((10, 10, -10, 16))
self.w.button = Button((10, 35, -10, 20), "Go!",
callback=self.showProgress)
self.w.open()

def showProgress(self, sender):
import time
self.w.bar.set(0)
for i in range(10):
self.w.bar.increment(10)
time.sleep(.2)

ProgressBarDemo()

**posSize** Tuple of form *(left, top, width, height)* representing
the position and size of the progress bar. The height of the progress
bar sould match the appropriate value for the given *sizeStyle*.

+-------------------------+
| **Standard Dimensions** |
+---------+---+-----------+
| Regular | H | 16|
+---------+---+-----------+
| Small   | H | 10|
+---------+---+-----------+

**minValue** The minimum value of the progress bar.

**maxValue** The maximum value of the progress bar.

**isIndeterminate** Boolean representing if the progress bar is indeterminate.
Determinate progress bars show how much of the task has been completed.
Indeterminate progress bars simply show that the application is busy.

**sizeStyle** A string representing the desired size style of the pregress bar.
The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
### VanillaError
### VerticalLine
A vertical line.::

from vanilla import *

class VerticalLineDemo(object):

def __init__(self):
self.w = Window((80, 100))
self.w.line = VerticalLine((40, 10, 1, -10))
self.w.open()

VerticalLineDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the line.

+-------------------------+
| **Standard Dimensions** |
+---+---------------------+
| V | 1   |
+---+---------------------+
### tagToInt
### PopUpButtonListCell
An object that displays a pop up list in a List column.

**This object should only be used in the *columnDescriptions*
argument during the construction of a List.**

**items** The items that should appear in the pop up list.

Note: when using this cell in a List, the `binding` in the
column description must be set to `selectedValue`.

Example::

from vanilla import *

class PopUpButtonListCellDemo(object):

def __init__(self):
self.w = Window((100, 100))
self.w.myList = List((0, 0, -0, -0),
[{"value": "A"}, {"value": "B"}],
columnDescriptions=[
{"title": "value", "cell": PopUpButtonListCell(["A", "B", "C"]), "binding": "selectedValue"}
],
editCallback=self.editCallback)
self.w.open()

def editCallback(self, sender):
print sender.get()

PopUpButtonListCellDemo()
### SliderListCell
An object that displays a slider in a List column.

**This object should only be used in the *columnDescriptions*
argument during the construction of a List.**

**minValue** The minimum value for the slider.

**maxValue** The maximum value for the slider.

**tickMarkCount** The number of tick marcks to be displayed on the slider.
If *None* is given, no tick marks will be displayed.

**stopOnTickMarks** Boolean representing if the slider knob should only
stop on the tick marks.

Example::

from vanilla import *

class SliderListCellDemo(object):

def __init__(self):
self.w = Window((200, 100))
self.w.myList = List((0, 0, -0, -0),
[{"value1": 30, "value2": 70}],
columnDescriptions=[
{"title": "value1", "cell": SliderListCell()},
{"title": "value2", "cell": SliderListCell(tickMarkCount=10)},
],
editCallback=self.editCallback)
self.w.open()

def editCallback(self, sender):
print sender.get()

SliderListCellDemo()
### SearchBox
A text entry field similar to the search field in Safari.::

from vanilla import *

class SearchBoxDemo(object):

def __init__(self):
self.w = Window((100, 42))
self.w.searchBox = SearchBox((10, 10, -10, 22),
callback=self.searchBoxCallback)
self.w.open()

def searchBoxCallback(self, sender):
print "search box entry!", sender.get()

SearchBoxDemo()

**posSize** Tuple of form *(left, top, width, height)* representing
the position and size of the search box.

+-------------------------+
| **Standard Dimensions** |
+---------+---+-----------+
| Regular | H | 22|
+---------+---+-----------+
| Small   | H | 19|
+---------+---+-----------+
| Mini| H | 15|
+---------+---+-----------+

**text** The text to be displayed in the search box.

**callback** The method to be called when the user presses the search box.

**formatter** A `NSFormatter <http://developer.apple.com/documentation/Cocoa/Reference/Foundation/Classes/NSFormatter_Class/index.html>`_
for controlling the display and input of the text entry.

**placeholder** A placeholder string to be shown when the text entry
control is empty.

**sizeStyle** A string representing the desired size style of the search box.
The options are:

+-----------+
| "regular" |
+-----------+
| "small"   |
+-----------+
| "mini"|
+-----------+
### LevelIndicator
A control which shows a value on a linear scale.::

from vanilla import *

class LevelIndicatorDemo(object):

 def __init__(self):
 self.w = Window((200, 68))
 self.w.discreteIndicator = LevelIndicator(
(10, 10, -10, 18), callback=self.levelIndicatorCallback)
 self.w.continuousIndicator = LevelIndicator(
(10, 40, -10, 18), style="continuous",
callback=self.levelIndicatorCallback)
 self.w.open()

 def levelIndicatorCallback(self, sender):
 print "level indicator edit!", sender.get()

LevelIndicatorDemo()

**posSize** Tuple of form *(left, top, width, height)* representing the position
and size of the level indicator.

+-------------------------------+
| **Standard Dimensions()** |
+-------------------------------+
| *discrete without ticks*  |
+-------------------------------+
| H | 18|
+-------------------------------+
| *discrete with minor ticks*   |
+-------------------------------+
| H | 22|
+-------------------------------+
| *discrete with major ticks*   |
+-------------------------------+
| H | 25|
+-------------------------------+
| *continuous without ticks*|
+-------------------------------+
| H | 16|
+-------------------------------+
| *continuous with minor ticks* |
+-------------------------------+
| H | 20|
+-------------------------------+
| *continuous with major ticks* |
+-------------------------------+
| H | 23|
+-------------------------------+

**style** The style of the level indicator. The options are:

+--------------+-------------------+
| "continuous" | A continuous bar. |
+--------------+-------------------+
| "discrete"   | A segmented bar.  |
+--------------+-------------------+

**value** The initial value of the level indicator.

**minValue** The minimum value allowed by the level indicator.

**maxValue** The maximum value allowed by the level indicator.

**warningValue** The value at which the filled portions of the
level indicator should display the warning color.

**criticalValue** The value at which the filled portions of the
level indicator should display the critical color.

**tickMarkPosition** The position of the tick marks in relation
to the level indicator. The options are:

+---------+
| "above" |
+---------+
| "below" |
+---------+

**minorTickMarkCount** The number of minor tick marcks to be displayed
on the level indicator. If *None* is given, no minor tick marks will be displayed.

**majorTickMarkCount** The number of major tick marcks to be displayed on the level
indicator. If *None* is given, no major tick marks will be displayed.

**callback** The method to be called when the level indicator has been edited.
If no callback is given, the level indicator will not be editable.

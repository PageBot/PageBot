# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     Module for global storage by scripts that use Variable UI or want to exchange
#	  other non-persistent information.
#
#	  In order to let PageBot scripts and/applications exchange information, without the need to save 
#     data in files, the pbglobals module supports the storage of non-persistent information.
#     This way, applications with Vanilla windows can be used as UI for scripts that perform as batch process.
#     Note that it is up to the responsibilty of individual scripts to create uniqued ids for 
#     attributes. Also they need to know from each other, in case information is exchanges""".
#
# Key is script/application id, e.g. their __file__ value.
# Access as:
# from pagebot.toolbox.transformer import path2ScriptId
# scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))
# or direct as:
#
globals = {} 

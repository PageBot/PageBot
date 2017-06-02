# -*- coding: UTF-8 -*-

"""
        filenames
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'


content = {
	'filename': [
		"<#file_project#><#file_state#>.<#file_extension#>",
		"<#file_project#><#file_state#><#file_state#>.<#file_extension#>",
		"<#file_project#><#file_state#><#file_morestate#><#file_state#><#file_state#>__<#names_first#>.<#file_extension#>",
	],
	'file_state': ['', '', '', '', '', '', '', 'ready', 'done', 'final',
				'final<#_,time_days#>', 'FINAL<#^^^_,time_days#>', "DONE", "FINAL", "!", "!!", "!!!",
				'<#time_date#>', '_<#colors_elaborate#>', "<#figs#>", "<#figs#><#figs#>", 'draft', "<#figs_ord#>_draft",
				'<#file_morestate#>'
				],
	'file_morestate': ['', '', '', '', '', '', '', '', '', '', '', "DONE", "EDIT", "NEEDSFIX", "APPROVED", "APPROVED?"],
	'file_project': ['<#_,name#>', '<#^@,name#>', '<#^_,name#>', '<#^_,hero#>', '<#i_dir_generic#>',
		'Proposal', 'draft', "curriculum", 'pressrelease', 'thesis', 'project', 'inventory_<#city#>', '<#city#>'
	],
	'file_extension': [
		"<#file_extension_image#>",
		"<#^^^,file_extension_image#>",
		"<#file_extension_office#>",
		"<#^^^,file_extension_office#>",
		"<#file_extension_web#>",
		"<#^^^,file_extension_web#>",
		],
	'file_extension_image': ['jpeg', 'psd', 'tiff', 'gif', 'png', 'pdf'],
	'file_extension_office': ['doc', 'docx', 'dot', 'wbk', 'docm', 'xls', 'xlsx', 'ppt'],
	'file_extension_web': ['php', 'html', 'htm', "js", "css"],
}

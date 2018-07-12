# -*- coding: UTF-8 -*-
#
"""
        history
        Generally useful stuff should go here, see content for ideas
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

from datetime import date
thisYear = date.today().year

__version__ = '4.0'


content = {
    'alphabet_caps'            :    ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
    'alphabet_lc'            :    ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
    'alphabet_common_lc'    :    ['s','t','r','n','d','m','n','l','e','a','o'],
    'alphabet_sizes'        :    ['A','B','C','D','E','F','A','B','C','D','E','F','A','B','C','D','E','F','AA','BB','CC','DD','EE','AA','BB','CC','DD','EE','FF','AAA','EEE',],

    'syllables'                :    ['am','air','com','cor','dac','dar','dat','dec','dom','fas','far','haz','lor','mac','mat','nor','or','pat','par','sac','sog','tow','us','vis','war','zen'],

    'colors_primary'        :    ['cyan', 'magenta', 'yellow', 'black', 'red', 'green', 'blue'],
    'colors_more'            :    ['chartreuse','taupe','beige','teal','brown','gray','white','carmine','purple','moss green',
                            ],
    'colors_adj'            :    ['light ', 'dark ', 'deep ', '','','','','','','','',],
    'colors_elaborate'        :    [
                                '<#colors_adj#><#colors_primary#>',
                                '<#colors_adj#><#colors_more#>',
                                ],

    'num_card'                :    ['one','two','three','four','five','six','seven','eight','nine'],
    'num_card_multiple'        :    ['two','three','four','five','six','seven','eight','nine'],
    'num_card_few'            :    ['two','three','four'],
    'num_card_010_019'        :    ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'],
    'num_card_010_090'        :    ['twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety'],
    'num_card_000_100'        :    ['<#num_card#>','<#num_card_010_019#>','<#num_card_010_090#>','<#num_card_010_090#><#num_card#>'],

    'num_roman'                :    ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'],

    'num_ord'                :    ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth'],
    'num_ord_010_019'        :    ['tenth','eleventh','twelfth','thirteenth','fourteenth','fifteenth','sixteenth','seventeenth','eighteenth','nineteenth'],
    'num_ord_010_090'        :    ['twentieth','thirtieth','fortieth','fiftieth','sixtieth','seventieth','eightieth','ninetieth'],
    'num_ord_000_100'        :    ['<#num_ord#>','<#num_ord_010_019#>','<#num_ord_010_090#>','<#num_card_010_090#> <#num_ord#>'],

    'num_temperatureF'        :    [u'<-randint(-20, 100)->°'],
    'num_temperatureC'        :    [u'<-randint(-20, 50)->°'],
    'num_temperature'        :    [u'<#num_temperatureF#>F',u'<#num_temperatureC#>C',],

    'amount_small'            :     ['some','few','2','3','4','5','6'],
    'amount_more'            :   ['over seven', 'over eight', 'over nine', 'over ten', 'over a dozen', 'dozens'],
    'amount_many'            :    ['dozens','a lot','too many','many','a large group', 'a large number'],

    'figs'                    :    ['1','2','3','4','5','6','7','8','9','0'],
    'figs_nonzero'            :    ['1','2','3','4','5','6','7','8','9'],
    'figs_multiple'            :    ['2','3','4','5','6','7','8','9'],
    'figs_rand_5digit'        :    ['<-randint(100, 999)->','<-randint(1000, 9999)->','<-randint(10000, 99999)->'],
    'figs_rand_4digit'        :    ['<-randint(1000, 9999)->'],
    'figs_rand_3digit'        :    ['<-randint(100, 999)->'],
    'figs_rand_2digit'        :    ['<-randint(10, 99)->'],
    'figs_rand_04digit'        :   ['<#figs#><#figs#><#figs#><#figs#>'],
    'figs_rand_03digit'        :   ['<#figs#><#figs#><#figs#>'],
    'figs_rand_02digit'        :   ['<#figs#><#figs#>'],
    'figs_ord'                :    ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th'],

    'age_adult'                :   ['<-randint(20, 99)->'],
    'age_child'                :   ['<-randint(3, 12)->'],
    'age_baby'                :   ['<-randint(1, 2)->'],
    'age_teenager'            :   ['<-randint(12, 18)->'],
    'age_retired'            :   ['<-randint(65, 99)->'],
    'age_worker'            :    ['<-randint(21, 65)->'],

    'time_comingyears'        :    [str(thisYear), str(thisYear+1), str(thisYear+2), str(thisYear+3), str(thisYear+4) ],
    'time_thisyear'            :    [str(thisYear)],
    'time_nextyear'            :    [str(thisYear+1)],
    'time_lastyear'            :    [str(thisYear-1)],
    'time_monthday'            :    ['<-randint(1,29)->'],

    'time_seasons'            :    ['Spring', 'Summer', 'Autumn', 'Winter' ],
    'time_holidays'            :    [
                                '<#time_seasons#>', '<#time_seasons#>', '<#time_seasons#>', 'Holidays', 'Thanksgiving', 'Christmas', 'Easter',
                                '<#time_holidays_minor#>',],

    'time_holidays_minor'    :    ['Kwanzaa','Armageddon',"Secretary's Day",'Auto Safety Week','Arbor Day','Cinco de Mayo','Bastille Day',"Guy Fawkes' Night",'Black <#time_days#>'],

    'time_months'            :    ['January','February','March','April','May','June','July','August','September','October','November','December'],
    'time_monthdays'        :   ['<#figs_nonzero#>','1<#figs_nonzero#>','2<#figs_nonzero#>'],
    'time_date'             :   ['1<#figs#> <#time_months#> 200<#figs#>'],
    'time_days'                :    ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
    'time_workhours'        :   ['8 a.m.', '9 a.m.', '10 a.m.', '11 a.m.', '12 a.m.', '1 p.m.', '2 p.m.', '3 p.m.', '4 p.m.', '5 p.m.', '6 p.m.'],
    'time_usenet'            :    ['<#time_days#>, 1<#figs#> <#time_months#> 199<#figs#> 1<#figs#>:3<#figs#>:2<#figs#> +<#figs#><#figs#>00 (GMT)'],
    'time_age'                :   ['<#figs_rand_2digit#>'],
    'time_day_recentpast'    :    ['yesterday', 'this morning', 'early this morning', 'last night', 'yesterday afternoon'],
    'time_day_nearfuture'    :    ['today','later today','tomorrow'],

    'time_week_recentpast'    :    ['recently','last week','last <#time_days#>'],
    'time_week_nearfuture'    :    ['presently','shortly','tomorrow','this week','within the week','this <#time_days#>','next <#time_days#>'],

    'p_figures_pop'            :    ['thunderbird','cadillac','corvette','elcamino','bongwater','xrayspex','lavalamp',    'snowcrash','hiro','raven',
            'bladerunner','wallace','gromit','pikachu','batman','robin','greenlantern','spiderman','laracroft','dasher','dancer','prancer',
            'vixen','comet','cupid','donner','blitzen','mentos','borg','enterprise','hal9000','kremlin','moulinrouge','bigben',
            'ernie','bert','kermit','piggy','bigbird'],
    'p_miscellaneous'    :    ['bubbles','paxil','wynona','static','cannonball','roadrage','nascar','mgs','cornflakes','alphabits','zarvox','beanie',
            'grand','royal','windmill','touchdown','station'],

    'p_whatever'            :    [
                            '<#sci_astro#>','<#sci_astro#>','<#sci_astro#>',
                            '<#lit_mythology#>','<#lit_mythology#>','<#lit_mythology#>',
                            '<#lit_figures#>','<#lit_figures#>','<#lit_figures#>',
                            '<#p_figures_pop#>','<#p_figures_pop#>',
                            '<#p_miscellaneous#>',
                            '<#sci_elements#>'],
    'left_or_right'            :    ['left', 'right'],

    }

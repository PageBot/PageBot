# -*- coding: UTF-8 -*-
#
"""
        history
        Internet related stuff, URL's, domains, email
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

__version__ = '4.0'




# ------------------------------------------------------
#    internet
#
content = {
    'i_tld'            :    ['.com','.net','.org'],
    'i_tld_misc'        :    ['.edu','.gov','.mil','.arpa','.nato'],
    'i_tld_natl'        :    ['.us','.ar','.au','.at','.be','.br','.ca','.dk','.fi','.fr','.de','.hk','.it','.jp','.nl','.nz','.no','.pt','.sg','.es','.se','.ch','.uk','.af','.al','.dz','.as','.ad','.ao','.ai',
            '.aq','.ag','.am','.aw','.ac','.az','.bs','.bh','.bd','.bb','.by','.bz','.bj','.bm','.bt','.bo','.ba','.bw','.bv','.vg','.bn','.bg','.bf','.bi','.kh','.cm','.cv','.ky','.cf','.td','.gg','.je',
            '.cl','.cn','.cx','.cc','.co','.km','.cg','.cd','.ck','.cr','.hr','.cu','.cy','.cz','.dj','.dm','.do','.tp','.ec','.eg','.sv','.gq','.er','.ee','.et','.fk','.fo','.fj','.gf','.pf','.tf','.ga','.gm',
            '.ge','.gh','.gi','.gr','.gl','.gd','.gp','.gu','.gt','.gn','.gw','.gy','.ht','.hm','.hn','.hu','.is','.in','.id','.ir','.iq','.ie','.im','.il','.ci','.jm','.jo','.kz','.ke','.ki','.kw','.kg','.la','.lv',
            '.lb','.ls','.lr','.ly','.li','.lt','.lu','.mo','.mk','.mg','.mw','.my','.mv','.ml','.mt','.mh','.mq','.mr','.mu','.yt','.hm','.mx','.fm','.md','.mc','.mn','.ms','.ma','.mz','.mm','.na',
            '.nr','.np','.an','.nc','.ni','.ne','.ng','.nu','.nf','.kp','.mp','.pk','.pw','.pa','.pg','.py','.pe','.ph','.pn','.pl','.pr','.qa','.re','.ro','.ru','.rw','.ws','.sm','.st','.sa','.sn','.sc','.sl',
            '.sk','.si','.sb','.so','.za','.gs','.kr','.gs','.lk','.sh','.kn','.lc','.pm','.vc','.sd','.om','.sr','.sj','.sz','.sy','.tw','.tj','.tz','.th','.tg','.tk','.to','.tt','.tn','.tr','.tm','.tc','.tv','.ug',
            '.ua','.ae','.uy','.uz','.vu','.va','.ve','.vn','.vi','.wf','.eh','.ye','.yu','.zm','.zw','.io','.fx','.um'],
    'i_tld_natl_major'    :    ['.us','.ar','.au','.at','.be','.br','.ca','.dk','.fi','.fr','.de','.hk','.it','.jp','.nl','.nz','.no','.pt','.sg','.es','.se','.ch','.uk','<#i_tld_natl#>','<#i_tld_natl#>','<#i_tld_natl#>'],

    'i_ip_quad'    :    ['<-randint(0, 256)->.<-randint(0, 256)->.<-randint(0, 256)->.<-randint(0, 256)->'],


    # ------------------------------------------------------
    #     internet:    Directories
    #

    'i_dir_users'        :    ['users','usr'],
    'i_dir_scripts'        :    ['cgi','cgi-bin','ftp','db','english','ns-search','exec','obidos'],
    'i_dir_generic'        :    ['projects','misc','proj','pers','general','stuff','files','things','test','<#names_last_patrician#>',
            '<#alphabet_common_lc#><#alphabet_common_lc#><#alphabet_common_lc#>','<#alphabet_lc#><#alphabet_lc#>'],

    'i_dir_formtrash'    :    [
            '<#alphabet_lc#><#alphabet_lc#>=<#figs#>-<#figs#>',
            '<#alphabet_lc#>id=<#figs_rand_5digit#>',
            '<#alphabet_lc#><#alphabet_lc#>=<#figs#><#figs#>&<#alphabet_lc#><#alphabet_lc#>=<#figs#><#figs#>&sortval=Name',
            ],

    'i_dir_searchtrash'    :    [
            '<#i_dir_scripts#>/productdetail.asp?product_id=<#figs_rand_5digit#>',
            '<#i_dir_scripts#>/showitem.cgi?SUBMIT=<#p_whatever#>',
            'ISAPI.dll?ViewItem&item=<#figs_rand_5digit#>',
            'searchresults.asp?<#i_dir_formtrash#>',
            'pag<#figs_rand_5digit#>.htm',
            '<#p_counters#>.cgi?=<#p_whatever#>',
            '<#i_dir_scripts#>/<#i_dir_scripts#>/<#i_dir_scripts#>/<#i_dir_formtrash#>/<#i_dir_formtrash#>',
            '<#i_dir_scripts#>/<#i_dir_scripts#>/<#i_dir_scripts#>/<#i_dir_formtrash#>',
            '<#names_first#>%20<#names_last#>',
            '<#i_dir_formtrash#>'
            ],


    # ------------------------------------------------------
    #     internet:    Servers
    #

    'i_host_server_mail'    :    ['','','','','','','','','','','','','','','','','','','','','mail.','mail.','mail.','mail.','smtp.','pop.'],
    'i_host_server_misc'    :    ['','','','','','','','','','','','','','','','','','','','','server.','firewall.','intranet.','extranet.'],
    'i_host_server_web'    :    ['','www.','www.','www.','www.','www.','www.','www.','www.','www.','www.','www.','www2.','www3.','web.','web.','web.','web.'],
    'i_host_server_news'    :    ['news.'],
    'i_host_server_biz'        :    ['admin','sales','storefront','secure','info','product','<#p_news_name#>','<#j_noun_pl#>'],

    # ------------------------------------------------------
    #     internet:    Academic URLS & e-mail
    #

    'i_host_edu_server_names'    :    ['<#sci_astro#>.','<#lit_mythology#>.','<#lit_figures#>.','<#p_figures_pop#>.','<#names_last_patrician#>.','<#sci_elements#>.'],
    'i_host_edu_departments'    :    ['','','','','','','','','','','','','','phys.','sci.','chem.','bio.','math.','calc.','comp.','comp-sci.','lang.','gov.','hist.','pol.',
            'edu.','psych.','med.','bus.','ba.','bfa.','bs.','mfa.','mba.','msc.','admin.','mus.','comp-lit.','engl.','lit.','acct.','phil.','phd.','lib.',],
    'i_host_edu_institution'        :    ['<#state_abbr_lc#>c','u<#state_abbr_lc#>','<#names_last_patrician#>','<#town_us_px#><#town_us_sx#>'],
    'i_host_edu'                :    [
            '<#i_host_edu_departments#><#i_host_edu_institution#>.edu',
            '<#i_host_edu_departments#><#i_host_edu_institution#>.edu',
            '<#i_host_edu_departments#><#i_host_edu_institution#>.edu',
            '<#i_host_edu_departments#><#i_host_edu_institution#>.edu',
            '<#i_host_edu_departments#><#i_host_edu_institution#>.edu',
            '<#i_host_edu_server_names#><#i_host_edu_departments#><#i_host_edu_institution#>.edu',
            '<#i_host_edu_server_names#><#i_host_edu_departments#><#i_host_edu_institution#>.edu',
            '<#i_host_edu_server_names#><#i_host_edu_departments#><#i_host_edu_institution#>.edu',
            'u<#alphabet_common_lc#><#alphabet_common_lc#>.ac<#i_tld_natl_major#>',
            'u<#alphabet_common_lc#><#alphabet_common_lc#>.ac<#i_tld_natl_major#>',
            '<#i_host_edu_departments#><#alphabet_common_lc#><#alphabet_common_lc#>c.ac<#i_tld_natl_major#>',
            '<#i_host_edu_departments#><#alphabet_common_lc#><#alphabet_common_lc#>cs.ac<#i_tld_natl_major#>',
            '<#i_host_edu_departments#>u<#alphabet_common_lc#><#alphabet_common_lc#>.ac<#i_tld_natl_major#>',
            '<#i_host_edu_departments#>u<#alphabet_common_lc#><#alphabet_common_lc#>.ac<#i_tld_natl_major#>',
            '<#i_host_edu_server_names#><#i_host_edu_departments#><#alphabet_common_lc#><#alphabet_common_lc#>cs.ac<#i_tld_natl_major#>'
            ],
    'eMail_edu'    :    ['<#i_users#>@<#i_host_server_mail#><#i_host_edu#>'],


    # ------------------------------------------------------
    #     internet:    Government URLS & e-mail
    #

    'i_host_gov_server_names'        :    ['<#sci_astro#>.','<#lit_mythology#>.','<#names_last_patrician#>.'],
    'i_host_gov_institution_state'    :    ['justice','labor','education','state','hhr','treasury'],
    'i_host_gov_institution_fed'        :    ['justice','labor','education','state','nasa','hhr','treasury','defense','nasa'],
    'i_host_gov'                    :    [
            '<#i_host_gov_institution_fed#>.gov',
            '<#i_host_gov_institution_fed#>.gov',
            '<#i_host_gov_server_names#><#i_host_gov_institution_fed#>.gov',
            '<#i_host_gov_server_names#><#i_host_gov_institution_fed#>.gov',
            '<#i_host_gov_institution_state#>.<#state_abbr_lc#>.gov',
            '<#town_us_px#><#town_us_sx#>.<#state_abbr_lc#>.gov',
            '<#i_host_gov_server_names#><#i_host_gov_institution_state#>.<#state_abbr_lc#>.gov',
            ],
    'eMail_gov'    :    ['<#i_users_formal#>@<#i_host_server_mail#><#i_host_gov#>'],


    # ------------------------------------------------------
    #     internet:    Military URLS & e-mail
    #

    'i_host_mil_server_names'        :    ['<#sci_astro#>.','<#lit_mythology#>.','<#sci_elements#>.'],
    'i_host_mil_institution'            :    ['defense','army','airforce','marines','navy','pentagon'],
    'i_host_mil'                    :    [
            '<#i_host_mil_institution#>.mil',
            '<#i_host_mil_institution#>.mil',
            '<#syllables#><#syllables#>.<#i_host_mil_institution#>.mil',
            '<#syllables#><#syllables#>.<#i_host_mil_institution#>.mil',
            '<#i_host_mil_server_names#><#i_host_mil_institution#>.mil',
            '<#i_host_mil_server_names#><#i_host_mil_institution#>.mil',
            '<#i_host_mil_server_names#><#syllables#><#syllables#>.<#i_host_mil_institution#>.mil',
            '<#i_host_mil_server_names#><#syllables#><#syllables#>.<#i_host_mil_institution#>.mil',
            '<#i_host_mil_server_names#><#i_host_mil_institution#>.mil',
            '<#i_host_mil_server_names#>arpa',
            '<#i_host_mil_server_names#><#syllables#><#syllables#>.arpa'
            ],
    'eMail_mil'    :    ['<#i_users_formal#>@<#i_host_server_mail#><#i_host_mil#>'],


    # ------------------------------------------------------
    #     internet:    Individual URLS & e-mail
    #

    'i_host_users_institution'        :    [
            '<#p_business_px#>host',
            '<#p_business_px#>port',
            '<#p_business_px#>mail',
            '<#p_business_px#>net',
            'free<#p_consolidatedbiz_sx#>',
            'web<#p_consolidatedbiz_sx#>',
            '<#i_host_biz_institution#>',
            '<#i_host_biz_institution#>',
            '<#alphabet_common_lc#><#alphabet_common_lc#><#alphabet_common_lc#>'
            ],
    'i_host_users'                    :    [
            '<#i_host_users_institution#>.com','<#i_host_users_institution#>.com','<#i_host_users_institution#>.com',
            '<#i_host_users_institution#>.com','<#i_host_users_institution#>.com','<#i_host_users_institution#>.com',
            '<#i_host_users_institution#>.com','<#i_host_users_institution#>.com','<#i_host_users_institution#>.com',
            '<#i_host_users_institution#>.com','<#i_host_users_institution#>.com','<#i_host_users_institution#>.com',
            '<#i_host_users_institution#>.co<#i_tld_natl_major#>','<#i_host_users_institution#>.co<#i_tld_natl_major#>',
            '<#i_host_users_institution#>.co<#i_tld_natl_major#>','<#i_host_users_institution#>.co<#i_tld_natl_major#>',
            '<#i_host_users_institution#>.co<#i_tld_natl_major#>','<#i_host_users_institution#>.co<#i_tld_natl#>',
            '<#i_host_edu_server_names#><#i_host_users_institution#>.com',
            '<#i_host_edu_server_names#><#i_host_users_institution#>.com',
            '<#i_host_edu_server_names#><#i_host_users_institution#>.co<#i_tld_natl_major#>',
            '<#i_host_edu_server_names#><#i_host_users_institution#>.co<#i_tld_natl_major#>',
            '<#i_host_users_institution#>.net','<#i_host_users_institution#>.net','<#i_host_users_institution#>.net',
            '<#i_host_users_institution#><#i_tld_natl_major#>','<#i_host_users_institution#><#i_tld_natl_major#>',
            '<#i_host_users_institution#><#i_tld_natl_major#>','<#i_host_users_institution#><#i_tld_natl#>',
            '<#i_host_edu_server_names#><#i_host_users_institution#>.net',
            '<#i_host_edu_server_names#><#i_host_users_institution#>.net',
            '<#names_last_patrician#>.org','<#names_last_patrician#>.org','<#names_last_patrician#>.org',
            ],
    'eMail_user'    :    ['<#i_users#>@<#i_host_server_mail#><#i_host_users#>'],


    # ------------------------------------------------------
    #     internet:    Commercial URLS & e-mail
    #

    'i_host_biz_institution'            :    [
            '<#p_business_px#><#p_business_name#>',
            '<#p_news_name#><#p_business_name#>',
            '<#p_business_px#><#p_news_name#>',
            '<#p_consolidatedbiz_px#><#p_consolidatedbiz_sx#>'
            ],
    'i_host_biz'                :    [
            '<#i_host_biz_institution#>.com',
            '<#i_host_biz_institution#>.com',
            '<#i_host_biz_institution#>.com',
            '<#i_host_biz_institution#>.co<#i_tld_natl_major#>',
            '<#i_host_server_biz#>.<#i_host_biz_institution#>.com',
            '<#i_host_server_biz#>.<#i_host_biz_institution#>.com',
            '<#i_host_server_biz#>.<#i_host_biz_institution#>.com',
            '<#i_host_server_biz#>.<#i_host_biz_institution#>.co<#i_tld_natl_major#>',
            ],
    'eMail_biz_formal'        :    ['<#i_users_formal#>@<#i_host_server_mail#><#i_host_biz#>'],
    'eMail_biz'            :    ['<#i_users#>@<#i_host_server_mail#><#i_host_biz#>'],
    'eMail_biz_info'        :    ['<#i_users_depts#>@<#i_host_server_mail#><#i_host_biz#>'],


    # ------------------------------------------------------
    #     internet:    Users
    #

    'i_users_depts'    :    ['info','sales','admin','support'],

    'i_users_formal'    :    [
            '<#names_last#>','<#names_last#>','<#names_last#>','<#names_last#>','<#names_last#>',
            '<#alphabet_caps#><#names_last#>','<#alphabet_caps#><#names_last#>',
            '<#names_last#><#alphabet_caps#><#alphabet_caps#>',
            '<#names_last#><#alphabet_caps#>',
            '<#names_last#><#alphabet_caps#>',
            '<#names_first#><#alphabet_caps#>',
            '<#names_first#><#alphabet_caps#>',
            '<#alphabet_caps#>_<#names_last#>',
            '<#names_last#>_<#alphabet_caps#>'
            ],

    'i_users_informal'    :    [
            '<#p_whatever#>',
            '<#alphabet_caps#><#names_last#>',
            '<#alphabet_caps#><#names_last#><#figs_rand_5digit#>',
            '<#names_first#><#alphabet_caps#><#figs_rand_5digit#>',
            '<#alphabet_common_lc#><#alphabet_common_lc#><#alphabet_lc#><#figs_rand_5digit#>',
            '<#p_whatever#>',
            '<#p_whatever#><#figs_rand_5digit#>'
            ],

    'i_users'    :    ['<#i_users_formal#>','<#i_users_informal#>'],



    # ------------------------------------------------------
    #     internet:    Web Pages
    #

    'i_host_random'    :    [
            '<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>',
            '<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>','<#i_host_biz#>',
            '<#i_host_users#>','<#i_host_users#>','<#i_host_users#>','<#i_host_users#>','<#i_host_users#>','<#i_host_users#>','<#i_host_users#>',
            '<#i_host_users#>','<#i_host_users#>','<#i_host_users#>','<#i_host_users#>','<#i_host_users#>','<#i_host_users#>','<#i_host_users#>',
            '<#i_host_edu#>','<#i_host_edu#>','<#i_host_edu#>','<#i_host_edu#>','<#i_host_edu#>',
            '<#i_host_edu#>','<#i_host_edu#>','<#i_host_edu#>','<#i_host_edu#>','<#i_host_edu#>',
            '<#i_host_gov#>','<#i_host_gov#>','<#i_host_gov#>',
            '<#i_host_mil#>','<#i_host_mil#>','<#i_host_mil#>',
            '<#i_ip_quad#>',
            '<#i_ip_quad#>',
            ],

    'i_page'        :    [
            'index.<#i_page_sx#>',
            'index.<#i_page_sx#>',
            'index.<#i_page_sx#>',
            'welcome.<#i_page_sx#>',
            'index.<#i_page_sx#>',
            '<#p_whatever#>.<#i_page_sx#>',
            '<#p_whatever#>.<#i_page_sx#>',
            'index.<#i_page_sx#>',
            '<#i_host_server_biz#>.<#i_page_sx#>',
            '<#i_dir_generic#>.<#i_page_sx#>'
            ],

    'i_page_sx'        :    [
            'html','html',
            'htm','htm',
            'htm#<#i_host_server_biz#>',
            'html#<#p_whatever#>',
            'cgi',
            'cfm','cfm',
            'asp','asp',
            'swf',
            'jpg'
            ],

    # ------------------------------------------------------
    #     internet:    URLs
    #

    'URL_biz'    :    [
            '<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>',
            '<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>',
            '<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>',
            '<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>','<#i_host_server_web#><#i_host_biz#>',
            '<#i_host_server_web#><#i_host_biz#>/<#navigation_shortform#>',
            '<#i_host_server_web#><#i_host_biz#>/<#navigation_shortform#>',
            '<#i_host_server_web#><#i_host_biz#>/<#navigation_shortform#>',
            '<#p_counters#>.<#i_host_biz#>',
            '<#p_counters#>.<#i_host_biz#>',
            '<#i_host_server_biz#>.<#i_host_biz#>',
            '<#i_host_server_biz#>.<#i_host_biz#>',
            '<#i_host_server_biz#>.<#i_host_biz#>',
            '<#i_host_server_web#><#i_host_server_biz#>.<#i_tld#>/<#IPO1#>',
            '<#i_host_server_web#><#i_host_biz#>/<#i_host_server_biz#>',
            '<#i_host_server_web#><#i_host_biz#>/<#i_host_server_biz#>',
            '<#i_host_server_web#><#i_host_biz#>/<#i_dir_searchtrash#>'
            ],

    'URL'    :    [
            '<#i_host_server_web#><#i_host_random#>/<#i_dir_users#>/~<#i_users#>/<#i_page#>',
            '<#i_host_server_web#><#i_host_random#>/<#names_last#>/<#i_page#>',
            '<#i_host_server_web#><#i_host_random#>/<#i_dir_users#>/~<#i_users#>/<#i_dir_generic#>/<#p_whatever#>/<#i_dir_generic#>/<#i_page#>',
            '<#i_host_server_web#><#i_host_random#>/<#i_users#>/<#i_dir_generic#>/<#p_whatever#>/<#i_page#>',
            '<#i_host_server_web#><#i_host_random#>/<#i_users#>/<#p_whatever#>/<#i_dir_generic#>/<#i_page#>',
            '<#i_host_server_web#><#i_host_random#>/<#i_dir_scripts#>/<#i_dir_generic#>/<#p_whatever#>/<#i_page#>',
            '<#i_host_server_web#><#i_host_random#>/<#i_dir_scripts#>/<#i_dir_generic#>/<#p_whatever#>/<#i_page#>',
            '<#i_host_server_web#><#i_host_random#>/<#i_dir_scripts#>/<#i_dir_generic#>/<#i_dir_searchtrash#>',
            '<#i_host_server_web#><#i_host_random#>/<#i_dir_scripts#>/<#i_dir_generic#>/<#i_dir_searchtrash#>',
            '<#i_host_server_web#><#i_host_random#>/<#i_dir_scripts#>/<#navigation_shortform#>/<#i_dir_generic#>/<#i_dir_searchtrash#>'
            ],


    # ------------------------------------------------------
    #     internet:    email, writing, reading, subjects, enclosures
    #

    'eMail'    :    [
            '<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz#>',
            '<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz#>','<#eMail_biz_info#>','<#eMail_biz_info#>',
            '<#eMail_user#>','<#eMail_user#>','<#eMail_user#>','<#eMail_user#>','<#eMail_user#>','<#eMail_user#>','<#eMail_user#>',
            '<#eMail_user#>','<#eMail_user#>','<#eMail_user#>','<#eMail_user#>','<#eMail_user#>','<#eMail_user#>','<#eMail_user#>',
            '<#eMail_edu#>','<#eMail_edu#>','<#eMail_edu#>','<#eMail_edu#>','<#eMail_edu#>',
            '<#eMail_edu#>','<#eMail_edu#>','<#eMail_edu#>','<#eMail_edu#>','<#eMail_edu#>',
            '<#eMail_gov#>','<#eMail_gov#>','<#eMail_gov#>',
            '<#eMail_mil#>','<#eMail_mil#>','<#eMail_mil#>',
            ],

    'eMail_subject':    [
            '$$$ MAKE MILLIONS FAST $$$',
            'Full/Part time Jobs From Home',
            'XXXXXXXX',
            'Re: Participating in <#events_conference#>',
            'Re: <#events_conference#> Papers',
            'Re: Your <#filibuster_productname#> Inquiry.',
            'Re: Your <#filibuster_productname#> Complaint.',
            'Fwd: <#!capitalize,p_figures_pop#> jokes',
            'Fwd: Fwd: Fwd: Warning: <#!capitalize,p_figures_pop#> Virus',
            '<#company#> Newsletter',
            '<#university#> Alumni Weekend',

            ],
    'eMail_enclosure':    [
            '','','','','','','','vcard.vcf'
            ],
    'eMail_sender':    [
            '<#eMail#>'
            ],
    'eMail_header': [
            '''Subject: <#msgsubject=eMail_subject#><#msgsubject#>
<br>Received: <#msgreceived=time_usenet#><#msgreceived#>
<br>Date: <#msgdate=time_usenet#><#msgdate#>
<br>From: <#msgsender=eMail#><#msgsender#>
<br>To: <#msgrecipient=eMail#><#msgrecipient#>
<br>Enclosures: <#msgenclosure=eMail_enclosure#><#msgenclosure#>'''
            ],

    'eMail_msgbody':    [
            """
<#eMail_header#>


The original message was received at <#msgdate:time_usenet#>
<br>from <#host:i_host_random#> [<#i_ip_quad#>]


<br>   ----- The following addresses had permanent fatal errors -----
<br><<#msg1:eMail#>>
<br><<#msg2:eMail#>>
<br><<#msg3:eMail#>>


<br>   ----- Transcript of session follows -----
<br>451 <#msg1#>: Name server timeout
<br>451 <#msg2#>: Name server timeout
<br>451 <#msg3#>: Name server timeout
<br>Message could not be delivered for 5 days
<br>Message will be deleted from queue


<br>Reporting-MTA: dns; <#host#>
<br>Arrival-Date: <#msgdate#>


<br>Final-Recipient: RFC822; <#msg1#>
<br>Action: failed
<br>Status: 4.4.7
<br>Last-Attempt-Date: <#msgdate#>


<br>Final-Recipient: RFC822; <#msg2#>
<br>Action: failed
<br>Status: 4.4.7
<br>Last-Attempt-Date: <#msgdate#>


<br>Final-Recipient: RFC822; <#msg3#>
<br>Action: failed
<br>Status: 4.4.7
<br>Last-Attempt-Date: <#msgdate#>


<br>Subject: <#eMail_subject#>
<br>Date: <#msgdate#>
<br>From: <#name#> <#msgsender:eMail_sender#>

""",
u"""
<#eMail_header#>


<#names_first_male#>,
<br>What do you make of this filibuster thing? It's odd. I don't know what to <#names_first_male#> is
going on about. It seems a pretty ordinary site. They have some problems with their server, sometimes
I get a page I didn't ask for. What do you think? Maybe we should advertise on it?


BTW, are we on for squash on <#time_days#>?


Cheers,
<br><#names_first_male#>
""",
"""
<#eMail_header#>


<#names_first_female#>,
<br>the pictures are great! He's so cute!
<br>Love, <#names_first_female#>
""",
u"""
<#eMail_header#>

CABLE TV DE-SCRAMBLER

<br>Build Your Own Cable De-scrambler for less than $<-randint(2, 30)->.  There are only <-randint(2, 30)-> Simple steps to follow, and all the parts (parts number list provided) can be easily found at your local electronics store.

<br>We Send You:
<br>�    E-Z To follow Assembly Instructions.
<br>�    E-Z To read Original Drawings.
<br>�    The Parts List.


<br>Frequently Asked Questions--CABLE TV DE-SCRAMBLER


Q:  Will the de-scrambler work on Fiber, TCI, Jarrod and Satellite systems?
<br>A:  The answer is YES.


Q:  Do I need a converter box?
<br>A:  This plan works with or without a converter box.  Specific Instructions are included in the plan for each.


Q:  Can the de-scrambler be detected?
<br>A:  No, the signal de-scrambles right at the box and does not Move back thorough the line.


Q:  Do I have to alter my existing cable system, television or VCR?
<br>A:  The answer is no.


Q:  Does this work everywhere across the country?
<br>A:  Yes, every where in the USA plus England, Brazil, and Other countries.


Q:  When I order, when will I get my stuff?
<br>A:  We mail out all orders within 24 hours of receiving it.


To get the instruction plans, the easy to follow diagram, and parts list. Just send $<-randint(2, 30)->, (Cash, Check or Money Order.) and you will receive your Cable De-scrambler Plans right away.
You get the complete package all for just  $<-randint(2, 30)->
(Shipping and Handling included)


Send your orders to:
<br><#p_acronym#>
<br><#address#>


(DISCLAIMER pleases notes: This information is being provided for educational purposes only. The information itself is legal, while the usage of such information may be illegal. We do not advocate unauthorized use or theft of cable services. If in doubt check your local laws and act accordingly.)

"""

            ],



}


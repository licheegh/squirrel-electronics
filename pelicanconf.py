#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = '小松鼠攻城师'
SITENAME = 'Squirrel Electronics'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'
LOCALE = ['chs','zh_CN']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
        ("cold's world",'http://www.linuxzen.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)
)


# Social widget
SOCIAL = (
        ('Weibo','http://weibo.com/u/1448434815'),
        ('Linkedin','https://www.linkedin.com/in/squirrelelectronics'),
        ('github','https://github.com/licheegh'),
        ('google+','https://plus.google.com/u/0/110725897032322313948')
)
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 3

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}
#FAVICON = 'extra/favicon.ico'

# Theme Settings
#	* `MENUITEMS`
#	* `LINKS` (Blogroll will be put in the sidebar instead of the head)
#* Analytics & Comments
#	* `GOOGLE_ANALYTICS` (classic tracking code)
#	* `GOOGLE_ANALYTICS_UNIVERSAL` and `GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY` (Universal tracking code)
#	* `DISQUS_SITENAME`
#	* `PIWIK_URL`, `PIWIK_SSL_URL` and `PIWIK_SITE_ID`
SHOW_ARTICLE_AUTHOR = False
#CUSTOM_CSS = 'static/custom.css'
#BOOTSTRAP_FLUID = False
BOOTSTRAP_THEME = 'cosmo'
# amelia -
# cerulean + blue
#cosmo + black
#cupid
#cyborg
#darkly
#flatly
#journal
#lumen
#paper
#readable
#readable-old
#sandstone +
#shamrock.
#simplex
#slate
#spacelab
#superhero
#united red
#yeti
PYGMENTS_STYLE = 'fruity'
#- autumn
#- borland
#- bw
#- colorful
#- default white +
#- emacs
#- friendly
#- fruity
#- github
#- igor
#- manni
#- monokai
#- murphy
#- native
#- paraiso-dark
#- paraiso-light
#- pastie
#- perldoc
#- rrt
#- solarizeddark
#- solarizedlight
#- tango
#- trac
#- vim
#- vs
#- xcode
#- zenburn
#SITELOGO = 'images/logo_small.JPG'

#DISPLAY_CATEGORIES_ON_SIDEBAR = True
#DISPLAY_CATEGORIES_ON_MENU = False

TAG_CLOUD_MAX_ITEMS = 5
#DISPLAY_TAG_CLOUD_ON_SIDEBAR = False

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 3

CC_LICENSE = "CC-BY-NC-SA"

BANNER = 'images/logo.jpg'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [ 
            #'render_math',
            #'better_codeblock_line_numbering'
            #'tipue_search'
            #'pelican-toc',
            'bootstrapify',
            'tag_cloud'
]

BOOTSTRAPIFY = {
    'table': ['table','table-bordered','table-hover','table-striped','table-responsive'],
    'img': ['img-responsive']
}
#TOC = {
    #'TOC_HEADERS' : '^h[1-6]',  # What headers should be included in the generated toc
                                ## Expected format is a regular expression

    #'TOC_RUN'     : 'true'      # Default value for toc generation, if it does not evaluate
                                ## to 'true' no toc will be generated
#}
#DIRECT_TEMPLATES = (('search',))
#MD_EXTENSIONS = ['toc','codehilite(css_class=highlight,linenums=True)','extra']
MD_EXTENSIONS = ['toc','codehilite(css_class=highlight)','extra']

#这个东西就是像文件夹一样显示一个路径
#DISPLAY_BREADCRUMBS = True
#BOOTSTRAP_NAVBAR_INVERSE = True
#在右边栏上显示一个介绍.
#ABOUT_ME = "dsadkja"

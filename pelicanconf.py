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
#         ('You can modify those links in your config file', '#'),)
)


# Social widget
SOCIAL = (
        ('Weibo','http://weibo.com/u/1448434815'),
        ('Linkedin','https://www.linkedin.com/in/squirrelelectronics'),
        ('github','https://github.com/licheegh'),
        ('google+','https://plus.google.com/u/0/110725897032322313948'),
        ('虾米','http://www.xiami.com/u/5395152')
)

DEFAULT_PAGINATION = 6

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}
#FAVICON = 'extra/favicon.ico'

# Theme Settings
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
PYGMENTS_STYLE = 'monokai'
#- autumn w
#- borland w
#- bw x
#- colorful w
#- default white +
#- emacs g
#- friendly g x
#- fruity d
#- github g
#- igor w +
#- manni g
#- monokai dg
#- murphy w
#- native d
#- paraiso-dark p
#- paraiso-light g
#- pastie w
#- perldoc g
#- rrt x
#- solarizeddark g
#- solarizedlight x
#- tango g x
#- trac w
#- vim d too
#- vs w +
#- xcode w +
#- zenburn dg
#SITELOGO = 'images/logo_small.JPG'

#DISPLAY_CATEGORIES_ON_SIDEBAR = True
#DISPLAY_CATEGORIES_ON_MENU = False

TAG_CLOUD_MAX_ITEMS = 10
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
#DIRECT_TEMPLATES = (('search',))
#MD_EXTENSIONS = ['toc','codehilite(css_class=highlight,linenums=True)','extra']
MD_EXTENSIONS = ['toc','codehilite(css_class=highlight)','extra']

#这个东西就是像文件夹一样显示一个路径
#DISPLAY_BREADCRUMBS = True
#BOOTSTRAP_NAVBAR_INVERSE = True
#在右边栏上显示一个介绍.
#ABOUT_ME = "dsadkja"

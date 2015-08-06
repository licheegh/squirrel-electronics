#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = '小松鼠攻城师'
SITENAME = 'Squirrel Electronics'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'ch'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)


# Social widget
SOCIAL = (('新浪微博','http://weibo.com/u/1448434815'),
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
#PYGMENTS_STYLE = monokai
#- autumn
#- borland
#- bw
#- colorful
#- default
#- emacs
#- friendly
#- fruity
#- manni
#- monokai
#- murphy
#- native
#- pastie
#- perldoc
#- solarizeddark
#- solarizedlight
#- tango
#- trac
#- vim
#- vs
#- zenburn
#SITELOGO = 'images/logo_small.JPG'

#DISPLAY_CATEGORIES_ON_SIDEBAR = True
#DISPLAY_CATEGORIES_ON_MENU = False

TAG_CLOUD_MAX_ITEMS = 5
#DISPLAY_TAG_CLOUD_ON_SIDEBAR = False

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 3

BANNER = 'images/logo.jpg'

#这个东西就是像文件夹一样显示一个路径
#DISPLAY_BREADCRUMBS = True
#BOOTSTRAP_NAVBAR_INVERSE = True
#在右边栏上显示一个介绍.
#ABOUT_ME = "dsadkja"
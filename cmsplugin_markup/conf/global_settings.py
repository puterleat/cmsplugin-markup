"""
Global cmsplugin_markup settings, are applied if there isn't a value defined
in project settings. All available settings are listed here. Please don't 
put any functions / test inside, if you need to create some dynamic values /
tests, take a look at cmsplugin_markup.conf.patch
"""
import os

from django.conf import settings

CMS_MARKUP_OPTIONS = (
        'cmsplugin_markup.plugins.markdown',
        'cmsplugin_markup.plugins.textile',
        'cmsplugin_markup.plugins.restructuredtext',
)

CMS_MARKUP_RENDER_ALWAYS = True

.. _backend-api:

cmsplugin-markup backends
=========================

At its core, cmsplugin-markup is built around the idea of pluggable backends which can impliment different markup implimentations for parsing user input. By default it comes with Markdown, Textile and ReST Backends available in the cmsplugin_markup/plugins/ directory.

Specifiying available backends
------------------------------
To determine which Markup options to give to the user, cmsplugin-markup looks for a setting called CMS_MARKUP_OPTIONS. It expects this to be a tuple in this format::

    CMS_MARKUP_OPTIONS = (
        'cmsplugin_markup.plugins.markdown',
        'cmsplugin_markup.plugins.textile',
        'cmsplugin_markup.plugins.restructuredtext',
        )

Each entry should be a string and should be a complete path to a python package that contains the required attributes.

You can also configure what is a default value for markups which support dynamically rendered output, using ``CMS_MARKUP_RENDER_ALWAYS`` setting (by default ``True``).

Backend API
-----------

To be used as a Markup backend, a python package must be laid out in a specific fashion and contain a class that must implement the following methods and variables. This class must be named Markup. An example class is below.::

    from cmsplugin_markup.plugins import MarkupBase

    class Markup(MarkupBase):
        name = 'Human Readable Name for the Mark Up'
        identifier = 'Internal Identifier for Mark Up'

        def parse(self, value, context=None, placeholder=None):
            return value

This barebones class contains all the required pieces to work. 

The ``name`` variable is a human readable name and may be any length. This is the name that will be presented to the user as the option. 

The ``identifier`` variable is stored as a CharField and anything that is allowed in a CharField is allowed in this. It must be unique across all the installed Markup Parsers and may be at most 20 characters long.

The ``parse`` function must accept self, and a value argument. It must accept also possible Django template rendering context and current placeholder. Those are given when rendering markup every time the page is displayed is enabled; to give more information about the context and location in which they are rendered. This function is where you will impliment the actual parsing of the user's input. At this point in time this function should fail silently and simply return an unchanged string. This might change in the future.

There are some additional methods and a variable if markup supports adding plugins. In this case ``text_enabled_plugins`` variable should be set to ``True`` and the following methods should be defined.

``plugin_id_list(self, text)`` should return the list of plugins inserted and currently used in the markup text.

``replace_plugins(self, text, id_dict)`` should replace references to plugins in the markup text with new ids.

``plugin_markup(self)`` should return JavaScript code for anonymous function which construct plugin markup given ``plugin_id``, ``icon_src`` and ``icon_alt`` arguments. It should be marked as safe to prevent escaping.

``plugin_regexp(self)`` should return JavaScript code for anonymous function which construct plugin regexp given plugin_id. It should be marked as safe to prevent escaping.

Some markups support dynamically rendered output (like macros) which could be rendered every time differently. If your markup supports this you can set ``is_dynamic`` to ``True`` and this will then give users an option to enable rendering of the content every time the page (Markup plugin) is displayed (default value is configured by ``CMS_MARKUP_RENDER_ALWAYS`` setting). Otherwise the content is rendered only once, when saved.

Directory Layout
~~~~~~~~~~~~~~~~

A Markup Backend Package should be laid out as follows

backend_name/
- __init__.py
- optional_class.py

The __init__.py file should either contain the Markup class definition, or should import it from an optional python file in the same directory. The optional file may be named anything.

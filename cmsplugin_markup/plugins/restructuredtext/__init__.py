from django.conf import settings
from django.utils.encoding import smart_str, force_unicode

from cmsplugin_markup.plugins import MarkupBase

class Markup(MarkupBase):

    name = 'ReST (ReStructured Text)'
    identifier = 'restructuredtext'

    def parse(self, value, context=None, placeholder=None):
        try:
            from docutils.core import publish_parts
        except ImportError:
            return force_unicode(value)
        else:
            docutils_settings = getattr(settings,
                    'RESTRUCTUREDTEXT_FILTER_SETTINGS', {})
            parts = publish_parts(source=smart_str(value),
                    writer_name="html4css1",
                    settings_overrides=docutils_settings)
            return force_unicode(parts["fragment"])

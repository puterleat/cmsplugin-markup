from django.db import models
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.utils.text import truncate_words
from django.conf import settings
from cms.models import CMSPlugin

from cmsplugin_markup import utils

MARKUP_CHOICES = utils.compile_markup_choices(settings.CMS_MARKUP_OPTIONS)

class MarkupField(CMSPlugin):
    body = models.TextField(_('Body'))
    body_html = models.TextField(blank=True)
    markup = models.CharField(
            _('Markup'),
            max_length=20,
            choices=MARKUP_CHOICES,
            default=MARKUP_CHOICES[0][0] if len(MARKUP_CHOICES) == 1 else models.NOT_PROVIDED,
            )
    dynamic = models.BooleanField(_('Render every time'), default=settings.CMS_MARKUP_RENDER_ALWAYS, help_text=_('Should be the content rendered every time the page is displayed or should it be rendered only when saved?'))

    search_fields = ('body_html',)

    def __unicode__(self):
        return u'%s' %(truncate_words(strip_tags(self.body_html), 3)[:30]+'...')

    def save(self, *args, **kwargs):
        # We store it in any case to also check the parser for possible exceptions and to use it for __unicode__
        self.body_html = utils.markup_parser(self.body, self.markup)
        if not utils.get_markup_object(self.markup).is_dynamic:
            self.dynamic = False
        return super(MarkupField, self).save(*args, **kwargs)

    def render(self, context):
        if self.dynamic:
            return mark_safe(utils.markup_parser(self.body, self.markup, context, context.get('placeholder')))
        else:
            return mark_safe(self.body_html)

    def clean_plugins(self):
        ids = utils.plugin_id_list(self.body, self.markup)
        plugins = CMSPlugin.objects.filter(parent=self)
        for plugin in plugins:
            if not str(plugin.pk) in ids:
                plugin.delete() #delete plugins that are not referenced in the markup anymore

    def post_copy(self, old_instance, ziplist):
        """
        Fix references to plugins
        """

        replace_ids = {}
        for new, old in ziplist:
            replace_ids[old.pk] = new.pk

        self.body = utils.replace_plugins(old_instance.markupfield.body, replace_ids, self.markup)
        self.save()

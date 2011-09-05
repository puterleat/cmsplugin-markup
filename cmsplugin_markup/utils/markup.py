from django.conf import settings

from cmsplugin_markup.plugins import MarkupBase

def get_list_of_markup_classes(markup_options=settings.CMS_MARKUP_OPTIONS):
    """
    Takes a tuple of python packages that impliment the cmsplugin_markup
    api and return a dict of the objects with identifier as key.
    """
    import sys

    objects = {}

    for markup in markup_options:
        try:
            __import__(markup)
            module = sys.modules[markup]
        except ImportError:
            continue

        try:
            # Check for required attributes
            if not hasattr(module.Markup, 'name'):
                continue
            if not hasattr(module.Markup, 'identifier'):
                continue
            if not hasattr(module.Markup, 'parse'):
                continue
            if not issubclass(module.Markup, MarkupBase):
                continue

            objects[module.Markup.identifier] = module.Markup
        except AttributeError:
            continue
    return objects

def compile_markup_choices(markup_options):
    """
    Takes a tuple of python packages that impliment the cmsplugin_markup
    api and makes a tuple of options for the forms.
    """

    choices = []
    objects = get_list_of_markup_classes(markup_options)

    for identifier, markup_object in objects.iteritems():
        choices.append((identifier, markup_object.name))

    return tuple(choices)

def get_markup_object(markup_id):
    """
    Returns an markup object based on its id.
    """

    markup_classes = get_list_of_markup_classes(settings.CMS_MARKUP_OPTIONS)
    return markup_classes[markup_id]()

def markup_parser(value, parser_identifier, context=None, placeholder=None):
    """
    Takes a string and a parser identifier and returns a string parsed
    by that parser. If anything goes wrong it returns the original string
    """

    return get_markup_object(parser_identifier).parse(value, context, placeholder)

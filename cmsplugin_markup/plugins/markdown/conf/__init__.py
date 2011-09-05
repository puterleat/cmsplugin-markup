from django.conf import settings

ALREADY_PATCHED = False

def patch_settings():
    """Merge settings with global cms settings, so all required attributes
    will exist. Never override, just append non existing settings.

    Also check for settings inconstistence if settings.DEBUG
    """
    global ALREADY_PATCHED

    if ALREADY_PATCHED:
        return

    ALREADY_PATCHED = True

    from cmsplugin_markup.plugins.markdown.conf import global_settings
    
    # merge with global cms settings
    for attr in dir(global_settings):
        if attr == attr.upper() and not hasattr(settings, attr):
            setattr(settings._wrapped, attr, getattr(global_settings, attr))

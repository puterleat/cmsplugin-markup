VERSION = (0,1,0,'alpha', 4)
__version__ = '.'.join(map(str, VERSION))

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version

# patch settings
try:
    from conf import patch_settings
    from django.conf import settings
    patch_settings()
except ImportError:
    """
    This exception means that either the application is being built, or is
    otherwise installed improperly. Both make running patch_settings
    irrelevant.
    """
    pass
except AttributeError:
    """
    Same as Above
    """
    pass

# Add text plugin template dir even if it is not in INSTALLED_APPS
try:
    import os
    import sys
    from django.template.loaders import app_directories
    from django.utils.importlib import import_module

    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()

    mod = import_module('cms.plugins.text')
    template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')

    if os.path.isdir(template_dir):
        try:
            app_directories.app_template_dirs.index(template_dir)
            # It is already there
        except ValueError:
            app_template_dirs = list(app_directories.app_template_dirs)
            app_template_dirs.append(template_dir.decode(fs_encoding))
            app_directories.app_template_dirs = tuple(app_template_dirs)
except:
    # Something went wrong, we will ignore it
    pass

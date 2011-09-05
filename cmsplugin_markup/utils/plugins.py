from cmsplugin_markup.utils.markup import get_markup_object

def plugin_id_list(text, markup_id):
    return get_markup_object(markup_id).plugin_id_list(text)

def replace_plugins(text, id_dict, markup_id):
    return get_markup_object(markup_id).replace_plugins(text, id_dict)

class MarkupBase(object):
    text_enabled_plugins = False
    is_dynamic = False

    def plugin_id_list(self, text):
        """
        Returns the list of plugins inserted and currently used in the markup text.
        """
        return []

    def replace_plugins(self, text, id_dict):
        """
        Replaces references to plugins in the markup text with new ids.
        """
        return text

    def plugin_markup(self):
        """
        Returns JavaScript code for anonymous function which construct plugin markup given plugin_id, icon_src and icon_alt arguments. It should be marked as safe to prevent escaping.
        """
        return None

    def plugin_regexp(self):
        """
        Returns JavaScript code for anonymous function which construct plugin regexp given plugin_id. It should be marked as safe to prevent escaping.
        """
        return None

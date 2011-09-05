// Automatic preview through XHR
// Based on Trac version, http://trac.edgewall.org/

var forceAutoPreview = false;

(function($) {
  // Enable automatic previewing to <textarea> elements.
  //
  // Arguments:
  //  - `href`: URL to be called for fetching the preview data.
  //  - `args`: arguments to be passed with the XHR.
  //  - `update`: the function that is called with the preview results. It
  //              is called with the textarea, the text that was rendered and
  //              the rendered text.
  $.fn.autoPreview = function(href, args, update) {
    if (auto_preview_timeout <= 0)
      return this;
    var timeout = auto_preview_timeout * 1000;
    return this.each(function() {
      var timer = null;
      var updating = false;
      var textarea = this;
      var data = {};
      for (var key in args) {
        if (typeof(args[key]) !== "function") {
          data[key] = args[key];
        }
      }
      data["text"] = textarea.value;
      
      // Request a preview through XHR
      function request() {
        var text = textarea.value;
        if (!updating && ((text != data["text"]) || forceAutoPreview)) {
          updating = true;
          forceAutoPreview = false
          data["text"] = text;
          for (var key in args) {
            if (typeof(args[key]) === "function") {
              data[key] = args[key]();
            }
          }

          $.ajax({
            type: "POST", url: href, data: data, dataType: "html",
            success: function(data) {
              updating = false;
              update(textarea, text, data);
              if (textarea.value != text)
                timer = setTimeout(request, timeout);
            },
            error: function(req, err, exc) {
              updating = false;
            }
          });
        }
      }
      
      // Trigger a request after the given timeout
      function trigger() {
        if (!updating) {
          if (timer)
            clearTimeout(timer);
          timer = setTimeout(request, timeout);
        }
        return true;
      }
      
      $(this).keydown(trigger).keypress(trigger).blur(request);
    });
  }
})(jQuery);

jQuery(document).ready(function($) {
  $.fn.cmsPatchCSRF();
});

jQuery(document).ready(function($) {
  // Only if preview exists
  $('#plugin-preview').each(function() {
    var preview = $(this);
    $('#id_body').autoPreview(auto_preview_url, {
        'markup': function () {return $('#id_markup').val()},
        'plugin_id': plugin_id,
        'page_id': page_id
      },
      function (textarea, text, data) {
        preview.html(data);
        if (parent.setiframeheight) {
          parent.setiframeheight($('body').height() + 20, 11);
        }
      });
  });
});

// Allow resizing <textarea> elements through a drag bar
// Copied from Trac, http://trac.edgewall.org/

jQuery(document).ready(function($) {
  $('textarea.django-resizable').each(function() {
    var textarea = $(this);
    var offset = null;
    
    function beginDrag(e) {
      offset = textarea.height() - e.pageY;
      textarea.blur();
      $(document).mousemove(dragging).mouseup(endDrag);
      return false;
    }
    
    function dragging(e) {
      textarea.height(Math.max(32, offset + e.pageY) + 'px');
      parent.setiframeheight($('body').height() + 20, 11);
      return false;
    }
    
    function endDrag(e) {
      textarea.focus();
      $(document).unbind('mousemove', dragging).unbind('mouseup', endDrag);
    }
    
    var grip = $('<div class="django-grip"/>').mousedown(beginDrag)[0];
    textarea.wrap('<div class="django-resizable"><div></div></div>').parent().append(grip);
    grip.style.marginLeft = (this.offsetLeft - grip.offsetLeft) + 'px';
    grip.style.marginRight = (grip.offsetWidth - this.offsetWidth) +'px';
  });
});

function MarkupEditorPlaceholderBridge(field) {
  this.field = field;
}

MarkupEditorPlaceholderBridge.prototype.insertText = function(text) {
  var selectionStart = this.field.get(0).selectionStart;
  var selectionEnd = this.field.get(0).selectionEnd;
  this.field.val(this.field.val().substring(0, selectionStart) + text + this.field.val().substring(selectionEnd));
};

MarkupEditorPlaceholderBridge.prototype.replaceContent = function(old, rep) {
  this.field.val(this.field.val().replace(old, rep));
};

MarkupEditorPlaceholderBridge.prototype.selectedObject = function() {
  return null;
};

function add_plugin_to_list(plugin_id, icon_src, icon_alt) {
  (function ($) {
    var img = $('<img/>').attr({
     'src': icon_src,
     'alt': icon_alt,
     'title': icon_alt
    }).click(edit_plugin_click);
    var divimg = $('<div/>').addClass('divimg').append(img);
    var span = $('<span/>').html(icon_alt + '<br />Plugin ID: ' + plugin_id).click(edit_plugin_click);
    var desc = $('<div/>').append(span);
    var li = $('<li/>').attr({
      'id': 'plugin_obj_' + plugin_id
    }).append(divimg).append(desc);
    li.appendTo('#plugins_list ul');
  })(jQuery);
}

function add_plugin_for_markup(type, parent_id, language, name) {
  (function ($) {
    $.post("add-plugin/", {
      parent_id: parent_id,
      plugin_type: type
    }, function(data) {
      if ('error' != data) {
        var plugin_id = data;
        edit_plugin_for_markup(plugin_id, name);
        editPluginPopupCallbacks[data] = function(plugin_id, icon_src, icon_alt) {
          texteditor = get_editor(name);
          texteditor.insertText(plugin_admin_markup(plugin_id, icon_src, icon_alt));
          add_plugin_to_list(plugin_id, icon_src, icon_alt);
          forceAutoPreview = true;
          $('#id_body').blur();
          editPluginPopupCallbacks[data] = null;
        };
      }
    }, "html");
  })(jQuery);
}

function edit_plugin_for_markup(obj_id, name) {
  (function ($) {
    editPluginPopupCallbacks[obj_id] = function(plugin_id, icon_src, icon_alt) {
      var texteditor = get_editor(name);
      var rExp = plugin_admin_regex(obj_id);
      try {
        texteditor.replaceContent(rExp, plugin_admin_markup(plugin_id, icon_src, icon_alt));
      } catch (e) {}
      $('#plugin_obj_' + plugin_id + ' img').attr({
        'src': icon_src,
        'alt': icon_alt,
        'title': icon_alt
      });
      $('#plugin_obj_' + plugin_id + ' span').html(icon_alt + '<br />Plugin ID: ' + plugin_id);
      forceAutoPreview = true;
      $('#id_body').blur();
      editPluginPopupCallbacks[obj_id] = null;
    };
    
    window.open("edit-plugin/" + obj_id + "/?_popup=1",
                "Edit_plugin_object",
                "menubar=no,titlebar=no,toolbar=no,resizable=yes"
                + ",width=800,height=300,top=0,left=0,scrollbars=yes"
                + ",location=no"
               );
  })(jQuery);
}

function plugin_admin_regex(plugin_id) {
  return markupPlugins[$('#id_markup').val()]['regex'](plugin_id);
}

function plugin_admin_markup(plugin_id, icon_src, icon_alt) {
  return markupPlugins[$('#id_markup').val()]['markup'](plugin_id, icon_src, icon_alt);
}

function markupchange() {
  (function ($) {
    var plugin = markupPlugins[$('#id_markup').val()];
    if ((typeof(plugin) !== "undefined") && plugin['textenabled']) {
      $('.iftextplugins').show();
    }
    else {
      $('.iftextplugins').hide();
    }
    if ((typeof(plugin) !== "undefined") && plugin['isdynamic']) {
      $('#id_dynamic').closest('.form-row').show();
    }
    else {
      $('#id_dynamic').closest('.form-row').hide();
    }
  })(jQuery);
}

jQuery(document).ready(function($) {
  $('#id_markup').change(function() {
    forceAutoPreview = true;
    $('#id_body').blur();
    markupchange();
  });
  markupchange();
});

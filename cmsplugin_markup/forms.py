from django.forms.models import ModelForm
from django.forms import widgets
from django import forms

from cmsplugin_markup.models import MarkupField

class MarkupForm(ModelForm):
    class Meta:
        model = MarkupField
        exclude = ('body_html',)
        widgets = {
            'body': widgets.Textarea(attrs={'class': 'django-resizable'}),
        }

from django import forms
from store.models import Language
from store.forms import LanguageField


class ImportForm(forms.Form):
    source_language = LanguageField(required=True)
    target_language = LanguageField(required=True)
    file = forms.FileField()

class ExportForm(forms.Form):
    EXPORT_FORMATS = (
        ('txt', 'txt'),
        ('json', 'json')
    )

    source_language = LanguageField(required=True)
    target_language = LanguageField(required=True)
    export_as = forms.ChoiceField(choices=EXPORT_FORMATS)



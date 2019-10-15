from django import forms
from ..models import Language


class LanguageField(forms.CharField):
    def clean(self, *args, **kwargs):
        value = super(LanguageField, self).clean(*args, **kwargs)
        try:
            
            return Language.objects.get(pk=value)
        except Language.DoesNotExist as e:
            raise forms.ValidationError(
                'Language does not exist', 
                code='invalid', params={'value': value})
                
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ('name', 'code')
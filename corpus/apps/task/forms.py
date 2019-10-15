
from django import forms
from django.contrib.auth import get_user_model
import datetime

from store.models import Language

from store.forms import LanguageField
from accounts.forms import UserField
from .models import TranslationTask, TranslationTaskItem



class TranslationTaskForm(forms.ModelForm):

    # form related field
    word_count = forms.IntegerField(min_value=0, required=True)
    size_short = forms.BooleanField(required=False)
    size_medium = forms.BooleanField(required=False)
    size_long = forms.BooleanField(required=False)

    # modelr related field
    source_language = LanguageField(required=True)
    target_language = LanguageField(required=True)
    user = UserField(required=True)

    class Meta:
        model = TranslationTask
        fields = (
                # Model oown field
                'source_language', 
                'target_language', 
                'user', 
                'end_at')

    def save(self, commit=True):
        
        new_translation_task = super().save(commit=commit)

        word_count  = self.cleaned_data.get('word_count') # word_count to no exceed for this task item
        size_short  = self.cleaned_data.get('size_short')
        size_medium = self.cleaned_data.get('size_medium')
        size_long   = self.cleaned_data.get('size_long')

        source_phrases = TranslationTask \
                        .phrases_ready_for_translation(
                                source_language=new_translation_task.source_language,
                                target_language=new_translation_task.target_language
                        ).sizes(
                                short=size_short, 
                                medium=size_medium, 
                                long=size_long
                        ).order_by('-word_count')

        # create a translation task item for each phrases
        phrases_word_count = 0 
        for p in source_phrases:
            new_translation_task \
                .translationtaskitem_set.create(_phrases_shared_id=p.shared_id)
            
            phrases_word_count += p.word_count
            if phrases_word_count >= word_count:
                break

        # set the translation task total word count
        new_translation_task.word_count += phrases_word_count
        new_translation_task.save()

        return new_translation_task
    


# Field forms 
class TranslationTaskItemField(forms.CharField):
    def clean(self, *args, **kwargs):
        value = super(TranslationTaskItemField, self).clean(*args, **kwargs)

        try:
           return TranslationTaskItem.objects.get(pk=value)
        except TranslationTaskItem.DoesNotExist as e:
           raise forms.ValidationError(
                    'TranslationTaskItem does not exist',
                    code='invalid', params={'value': value})

        
        
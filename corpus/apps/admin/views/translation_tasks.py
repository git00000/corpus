from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.db.models import Q, Sum
from django import forms
from corpus.core.views import APIView
from accounts.serializers import UserSerializer
from task.models import TranslationTask
from task.serializers import  TranslationTaskSerializer
from store.serializers import LanguageSerializer, DynamicPhraseSerializer


from task.models import TranslationTask

from task.forms import TranslationTaskForm

from ..forms import LanguageField


class TranslationTaskAdminView(TemplateView):
    template_name = 'admin/translation_tasks.html'


class TranslationTaskAPIView(APIView):
    model = TranslationTask
    base_queryset = TranslationTask.objects.order_by('-id')
    
    serialiazer_class = TranslationTaskSerializer
    add_form_class = TranslationTaskForm
    edit_form_class = None #TranslationTaskForm
    page_size = 10
    search_fields = ()



class UntranslatedPhraseAPIView(View):
    def post(self,request):
        """
            request format:
            {
                source_language: 1, // source language id
                target_language: 3, // target language id
                size_short: true,
                size_medium: false,
                size_long: true
            }

            response format:
            {
                source_language: {id: 1, name: 'french', code: 'fr'},
                target_language: {id: 2, name: 'english', code: 'en'},
                bilingual_users: [{id: 2, enamil: 'example@gmail.com'}, ...],
                phrase_count: 1234,
                total_word_count: 1234,
            } 
        """

        form = self.get_validation_form()(request.POST)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    

    def form_valid(self, form):
        source_language = form.cleaned_data.get('source_language')
        target_language = form.cleaned_data.get('target_language')
        size_short   = form.cleaned_data.get('size_short')
        size_medium  = form.cleaned_data.get('size_medium')
        size_long    = form.cleaned_data.get('size_long')
        

        from django.contrib.auth import get_user_model 
        users = get_user_model().objects.all()
        for u in users:
            u.save()

        bilingual_user_list = [p.user for p \
                                            in source_language.user_profile_set.filter( \
                                                user__profile__in=[p2 for p2 \
                                                                        in target_language.user_profile_set.all()])]
        

    
        # Get all available phrases for this two languages
        phrases = TranslationTask \
                        .phrases_ready_for_translation(source_language, target_language) \
                        .sizes(short=size_short, medium=size_medium, long=size_long)
        
    
        # get phrase count
        phrase_count = phrases.count()
        total_word_count = phrases.aggregate(total=Sum('word_count'))['total']

        response_data = {
            'source_language': LanguageSerializer(source_language).data,
            'target_language': LanguageSerializer(target_language).data,
            'bilingual_users': UserSerializer(bilingual_user_list, many=True).data,
            'phrase_count': phrases.count(),
            'total_word_count': phrases.aggregate(total=Sum('word_count'))['total'] or 0
        }

        return JsonResponse(response_data, safe=False)

        #serializer =  DynamicPhraseSerializer(phrases, many=True)
        #print(phrases)

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)
        
    def get_validation_form(self):
        class ValidationForm(forms.Form):
            source_language = LanguageField(required=True)
            target_language = LanguageField(required=True)
            
            size_short  = forms.BooleanField(required=False)
            size_medium = forms.BooleanField(required=False)
            size_long   = forms.BooleanField(required=False)

        return ValidationForm
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django import forms
from task.models import TranslationTask, TranslationTaskItem
from task.forms import TranslationTaskItemField

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class UserAuthMixin(LoginRequiredMixin, UserPassesTestMixin):
    # LoginRequiredMixin overrides
    login_url = reverse_lazy("accounts:login")
    redirect_to_field = "next"

class UserProfileView(UserAuthMixin, TemplateView):
    template_name = 'user/profile.html'

    # UserPassesTestMixin
    def test_func(self):
        return self.request.user.is_active

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        print(self.request.user.is_authenticated)
        return ctx


    


class TranslationTaskUserView(View):
    template_name ="user/translation.html"

    def get(self, request, translation_task_id):
        context = {
            "translation_task_id": translation_task_id
        }
        return render(request, self.template_name, context)



class TranslationTaskNextItemAPIView(View):
    def post(self, request):
        """
            Request data format: 
            {
                'id': 23  # The translation task id
                'next': 'next' # can be next or previous
            }
        """
        task_id = request.POST.get('id')
        item_next = request.POST.get('next')

        try:
            translation_task = TranslationTask.objects.get(id=task_id)
        except TranslationTask.DoesNotExist:
            return JsonResponse(
                                  {'errors': [f'TranslationTask  of id {task_id} does not exist']}, 
                                  status=400, 
                                  safe=False)
        

        if item_next == 'next':
            item = translation_task.next_item
        elif item_next == 'previous':
            item = translation_task.prev_item
        elif item_next == 'current':
            item = translation_task.current_item
            if item is None: # current item is not set maybe try next
                item = translation_task.next_item

        else:
            return JsonResponse(
                                    {'errors', ["move_on request parameter not valid. Possible value are: 'next','previous'" ]},
                                    status=400,
                                    safe=False)
        
        #prev_item = translation
        if item is None:
            raise NotImplementedError("item is None, not handle yet !")
        

        return JsonResponse(item.serializer_data, safe=False)


class TranslationTaskItemPhraseSavingAPIView(View):
    def post(self,request):
        import json
        """
            request data format:
                {
                    item: 23, # the translation task item id
                    language_as: "source" | "target", # phrase is source
                    text: "Hello world",
                    item_completed: true, # whetheir the task item is completed or not
                }

            reponse format: -> PhraseSerailzier data
        """
        form = self.validation_form(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        translation_task_item = form.cleaned_data.get('item')
        language_as = form.cleaned_data.get('langauge_as')
        text     = form.cleaned_data.get('text')
        item_completed = form.cleaned_data.get("item_completed")

        # 1 - saving translate phrase
            # if source phrase is not translated yet
            # no target_phrase will be find
            # in which case we create a new target_phrase

        if language_as == 'source':
            source_phrase = translation_task_item.source_phrase
            source_phrase.text = text
            source_phrase.save()
        else: # language_as == 'target'
            target_phrase = translation_task_item.target_phrase
            if target_phrase is not None: # target phrase may be None, (please refer to step #3 above)
                target_phrase.text = text
                target_phrase.save()
            else:
                # Create a new target phrase (translation for the source phrase)
                target_phrase = translation_task_item \
                                    .translation_task \
                                    .target_language \
                                    .dictionnary \
                                    .phrases.model(shared_id=translation_task_item.phrases_shared_id,text=text)
                target_phrase.save()

        # Updating translation task item completed stat
        # 
        translation_task_item.completed = item_completed
        translation_task_item.save()
        
        return JsonResponse(target_phrase.serializer_data, safe=False)
        

    def form_invalid(self, form):
        print('from invalid')
        for err in form.errors:
            print(err, form.errors[err])
        return JsonResponse({"errors": form.errors}, status=400)
    
    
    @property
    def validation_form(self):
        class ValidationForm(forms.Form):
            LANGUAGE_AS_OPTIONS = (
                                    ('source','source'),
                                    ('target', 'target')
                                  )
            
            item            = TranslationTaskItemField(required=True)
            language_as     = forms.ChoiceField(choices=LANGUAGE_AS_OPTIONS, required=True)
            text            = forms.CharField(required=False)
            item_completed  = forms.BooleanField(required=False) 

        return ValidationForm
from django.shortcuts import render
from django.views.generic import TemplateView, View

from corpus.core.views import APIView
from store.models import Language
from store.serializers import LanguageSerializer
from store.forms import LanguageForm

class LanguageAdminView(TemplateView):
    template_name = 'admin/languages.html'

class LanguageAPIView(APIView):
    model = Language
    base_queryset = Language.objects.order_by('-id')
    
    serialiazer_class = LanguageSerializer
    add_form_class = LanguageForm
    edit_form_class = LanguageForm

    page_size = 10
    search_fields = ('name', 'code')
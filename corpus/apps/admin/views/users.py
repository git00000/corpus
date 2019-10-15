from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json

from accounts.serializers import UserSerializer
from accounts.forms import UserForm
from task.models import TranslationTask

from corpus.core.views import APIView

User = get_user_model()

class UserAdminView(TemplateView):
    template_name = 'admin/users.html'


class UserAPIView(APIView):
    
    model = get_user_model()
    base_queryset = get_user_model().objects.order_by('-id')
    
    serialiazer_class = UserSerializer
    add_form_class = UserForm
    edit_form_class = UserForm

    page_size = 10
    search_fields = ('email', )
    


class UserTranslationTaskAPIView(View):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return JsonResponse({"errors": "User does not exist"}, status=400)

        data = TranslationTask.objects.filter(user=user).serializer_data
        
        return JsonResponse(data, safe=False)
    

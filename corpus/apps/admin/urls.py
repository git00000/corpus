from django.urls import path, include
from .views import urls as admin_urls

app_name = 'myadmin'

urlpatterns = admin_urls.urlpatterns
api_patterns = admin_urls.api_patterns
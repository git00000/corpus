from django.urls import path

from . import views


app_name = 'url_service'
urlpatterns = [
    path('path-reverse/<slug:path>/',
          views.index, 
          name="path-reverse")
]
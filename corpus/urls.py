"""corpus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


# Applicatin height level urls
from admin import urls as admin_urls
from user import urls as user_urls


#from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('auth/', include('authentication.urls')),
    #path('u/', include('webuser.urls')),
    #path('adm/', include('webuadmin.urls')),

    path('admin/', include(admin_urls)),
    path('xhr/admin/', include(admin_urls.api_patterns)),

    path("u/", include(user_urls)),
    path('xhr/user/', include(user_urls.api_patterns)),

    path('xhr/url-service/', include('url_service.urls')),

    path('auth/', include('accounts.urls')),
    
    path('', include('guest.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#+ i18n_patterns(
#        path('auth/', include('authentication.urls')),
#        path('u/', include('webuser.urls')),
#        path('adm/', include('webuadmin.urls')),
#  ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

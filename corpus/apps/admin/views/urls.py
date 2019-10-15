from django.urls import path
from . import (LanguageAdminView, LanguageAPIView,
               UserAdminView, UserAPIView, UserTranslationTaskAPIView,

               TranslationTaskAdminView, TranslationTaskAPIView,
               UntranslatedPhraseAPIView,

               DashboardView,
               ImportExportAdminView, ImportAPIView, ExportAPIView,)


urlpatterns = [
      path('dashboard/',
            DashboardView.as_view(),
            name='dashboard'),

      path('users/',
            UserAdminView.as_view(),
            name="users"),
         

      path('languages/',
            LanguageAdminView.as_view(), 
            name="languages"),

      path('translation-tasks/',
            TranslationTaskAdminView.as_view(),
            name="tasks"),

      path('import-export/',
            ImportExportAdminView.as_view(),
            name='import-export'
      )

]


api_patterns = [
      path('users/', 
            UserAPIView.as_view(),
            name="corpus-xhr-admin-users"),
      
      path('users/<int:id>/',
            UserAPIView.as_view(),
            name='corpus-xhr-admin-user'),
      path('users/<int:id>/translation-tasks/',
            UserTranslationTaskAPIView.as_view(),
            name="corpus-xhr-admin-user-translationAPIView"),
      
      
      path('languages/',
            LanguageAPIView.as_view(),
            name="corpus-xhr-admin-languages"),
      
      path('languages/<int:id>/',
            LanguageAPIView.as_view(),
            name="corpus-xhr-admin-language"),

      path('translation-tasks/',
            TranslationTaskAPIView.as_view(),
            name='corpus-xhr-admin-translation-task'
      ),

      path('translation-tasks/<int:id>/',
            TranslationTaskAPIView.as_view(),
            name='corpus-xhr-admin-translation-task'
      ),
      path('untranslated-phrases/',
            UntranslatedPhraseAPIView.as_view(),
            name='corpus-xhr-admin-untranslated-phrases'
            ),

      path('import-export/import/', 
            ImportAPIView.as_view(),
            name="corpus-xhr-admin-import-export-import"
      ),
      path('import-export/export/', 
            ExportAPIView.as_view(),
            name="corpus-xhr-admin-import-export-export"
      )
]
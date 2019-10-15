from django.urls import path
from .views import (
                    UserProfileView,
                    TranslationTaskUserView, 
                    TranslationTaskNextItemAPIView,
                    TranslationTaskItemPhraseSavingAPIView)



app_name = "user"

urlpatterns = [

        path(
             '',
             UserProfileView.as_view(),
             name="profile",
        ),

        path(
            'taches/<int:translation_task_id>',
            TranslationTaskUserView.as_view(),
            name="translation-task"
        ),
]


api_patterns = [
    path(
         'translation-task-next-item/',
         TranslationTaskNextItemAPIView.as_view(),
         name="corpus-xhr-user-translation-task-next-item"
    ),

    path(
         'save-translation-task-item-phrase/',
          TranslationTaskItemPhraseSavingAPIView.as_view(),
          name="corpus-xhr-user-save-translation-task-item-phrase"
        ),

]
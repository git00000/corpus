from django.db import models
from django.db.models import Q, QuerySet, Count
from django.contrib.auth import get_user_model
from django.db.utils import cached_property
from store.models import Language

User = get_user_model()

class TranslationTaskQuerySet(QuerySet):
    @property
    def serializer_data(self):
        from ..serializers import TranslationTaskSerializer
        return TranslationTaskSerializer(self, many=True).data

class TranslationTaskManager(models.Manager):
    def get_queryset(self):
        return TranslationTaskQuerySet(self.model)



class TranslationTask(models.Model):
    
    source_language = models.ForeignKey(
                            Language,
                            related_name="source_language",
                            related_query_name="source_language",
                            on_delete=models.CASCADE
                        )

    target_language = models.ForeignKey(
                            Language,
                            related_name="target_language",
                            related_query_name="target_language",
                            on_delete=models.CASCADE
                        )

    curr_item = models.OneToOneField(
                                    'task.TranslationTaskItem',
                                     on_delete=models.SET_NULL, 
                                     null=True, default=None
                                )

    word_count = models.IntegerField(default=0)    # The total word count for translation    

    user =  models.ForeignKey(
                        User,
                        on_delete=models.CASCADE
            )

    done = models.BooleanField(default=False)



    created_at  = models.DateTimeField(auto_now=True)
    end_at      = models.DateTimeField(null=False)
    finished_at = models.DateTimeField(null=True)


    objects = TranslationTaskManager()





    def save(self, *args,  **kwargs):

        # In progress translation task are merge with their similars
        # So we will not have to similar task again multiple times
        similar_tasks = self.get_similars()
        
        if similar_tasks.count() > 0:
            if similar_tasks.count() > 1:
                raise NotImplementedError("Multiple TranslationTask merginng not Implemented yet")
            
            # Single merge
            similar = similar_tasks[0]
            if self.end_at > similar.end_at:
                similar.end_at = self.end_at
            # Substitue the self to the similar_task
            # So we will just have only one single task type at hand
            self.__dict__.update(similar.__dict__)
            super().save()
            return

        super().save(*args, **kwargs)

    
    def get_similars(self):
        from django.utils import timezone
        return TranslationTask \
            .objects \
                .filter(
                    user=self.user,
                    source_language=self.source_language,
                    target_language=self.target_language,
                    finished_at=None,
                    end_at__gte=timezone.now()) \
                .exclude(
                    id=self.id
                )
            

    @property
    def item_count(self):
        return self.translationtaskitem_set.count()
                

    @property
    def completed_item_count(self):
        return self.translationtaskitem_set.filter(completed=True).count()

    @property
    def is_done(self):
        if self.done == False:
            self.done = 0 == self.translationtaskitem_set.filter(completed=False).count()
            self.save()
        return self.done

    @property
    def current_item(self):
        if self.id is None:
            return None
        return self.curr_item
        
    @property
    def next_item(self):
        if self.id is None:
            return None

        if self.curr_item is None:
            self.curr_item = self.translationtaskitem_set \
                                    .order_by('id') \
                                    .first() 
            super().save()
            return self.curr_item

        next_item = self.translationtaskitem_set \
                            .filter(id__gt=self.curr_item.id) \
                            .order_by('id') \
                            .first() \
                if self.curr_item is not None \
                else None

        self.curr_item = next_item if next_item is not None else self.curr_item
        super().save()

        return self.curr_item

    @property
    def prev_item(self):
        if self.id is None:
            return None

        if self.curr_item is None:
            self.curr_item = self.translationtaskitem_set \
                                    .order_by('-id') \
                                    .first()
            super().save()
            return self.curr_item

        prev_item = self.translationtaskitem_set \
                            .filter(id__lt=self.curr_item.id) \
                            .order_by('-id') \
                            .first() \
                if self.curr_item is not None \
                else None

        self.curr_item = prev_item if prev_item is not None else self.curr_item
        super().save()
        
        return self.curr_item

    
    def get_uncompleted_items(self):
        return self.translationtaskitem_set.filter(completed=False)
    def get_completed_items(sef):
        return self.translationtaskitem_set.filter(completed=False)



    @classmethod
    def get_unavailable_shared_ids(cls, source_language, target_language):
        in_progress_translation_tasks = cls.objects.filter( \
                                                source_language=source_language, \
                                                target_language=target_language, done=False)
        unavailable_shared_ids = []
        for translation_task in in_progress_translation_tasks:
            uncompleted_items = translation_task.get_uncompleted_items()
            unavailable_shared_ids += [ item._phrases_shared_id for item in uncompleted_items ] \
                                  +[ item._phrases_shared_id for item in uncompleted_items ]

        return unavailable_shared_ids

    @classmethod
    def phrases_ready_for_translation(cls, source_language, target_language):

        unavailable_shared_ids = cls.get_unavailable_shared_ids(source_language, target_language)
        phrases = source_language \
                    .dictionnary \
                    .phrases.exclude(
                          Q(shared_id__in=unavailable_shared_ids) |
                          (
                             Q(shared_id__in=[p.shared_id for p in target_language.dictionnary.phrases.all()]) &
                             Q(editable=False)
                          )
                        )
        # in short, not translated yet source_phrase to target_phrase
        return phrases
    

    # for serialization
    @property
    def serializer_data(self):
        from ..serializers import TranslationTaskSerializer
        return TranslationTaskSerializer(self).data
        


    


class TranslationTaskItem(models.Model):
    translation_task    = models.ForeignKey(TranslationTask, on_delete=models.CASCADE) 
    _phrases_shared_id  = models.UUIDField()
    
    created_at          = models.DateTimeField(auto_now=True)
    completed           = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    @property
    def source_phrase(self):
        return self.translation_task \
                        .source_language \
                        .dictionnary \
                        .phrases.get(shared_id=self._phrases_shared_id)

    @property        
    def target_phrase(self):
        try:
            return self.translation_task \
                        .target_language \
                        .dictionnary \
                        .phrases.get(shared_id=self._phrases_shared_id)
        except:
            return None

    @property
    def phrases_shared_id(self):
        if self._phrases_shared_id is None:
            self._phrases_shared_id = self.get_source_phrase().shared_id
            self.save()
        return self._phrases_shared_id
                        

    @property
    def is_completed(self):
        if self.completed == False:
            self.completed = self.target_phrase_id is not None
            self.save()

        return self.completed

    @cached_property
    def position(self):
        return TranslationTaskItem.objects.filter(id__lt=self.id, translation_task=self.translation_task).aggregate(position=Count('id'))['position'] + 1
    
    @property
    def serializer_data(self):
        from ..serializers import TranslationTaskItemSerializer
        return TranslationTaskItemSerializer(self).data
    





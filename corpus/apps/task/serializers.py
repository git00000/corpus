

from rest_framework import serializers

from .models import TranslationTask, TranslationTaskItem


class TranslationTaskItemSerializer(serializers.ModelSerializer):
    source_phrase = serializers.SerializerMethodField()
    target_phrase = serializers.SerializerMethodField()
    translation_task = serializers.SerializerMethodField()
    class Meta:
        model = TranslationTaskItem
        fields = (
                    'id',
                    'translation_task',
                    'phrases_shared_id',
                    'source_phrase',
                    'target_phrase',
                    'position',
                    'completed',
                )
    
    def get_source_phrase(self, instance):
        return instance.source_phrase.serializer_data

    def get_target_phrase(self, instance):
        # Target phrase could be None
        try:
            return instance.target_phrase.serializer_data
        except AttributeError:
            return {} # We return an empty target phrase
    
    def get_translation_task(self, instance):
        return instance.translation_task.serializer_data

    

class TranslationTaskSerializer(serializers.ModelSerializer):

    source_language = serializers.SerializerMethodField()
    target_language = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    # word_count = serializers.SerializerMethodField()

    class Meta:
        model = TranslationTask
        fields = (
                'id',
                'source_language', 
                'target_language',
                'user',
                'done',
                'created_at',
                'end_at',
                'finished_at',
                'item_count',
                'word_count',
                'completed_item_count')

    def get_source_language(self, instance):
        return instance.source_language.serializer_data
    
    def get_target_language(self, instance):
        return instance.target_language.serializer_data
        
    def get_user(self, instance):
        return instance.user.serializer_data
    
    # def get_word_count(self, instance):
    #     count = 0
    #     for item in instance.translationtaskitem_set.all():
    #         count += item.source_phrase.word_count
    #     instance.word_count = count
    #     instance.save()
    #     return count

        
    
    
    


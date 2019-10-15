

from rest_framework import serializers
from django.db.models import QuerySet

class DynamicPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ('text', 'shared_id')

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)
        
        if isinstance(instance, QuerySet):
            self.Meta.model = instance.model
        else:
            self.Meta.model = type(instance)

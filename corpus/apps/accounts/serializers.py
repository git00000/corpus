from django.contrib.auth import get_user_model
from rest_framework import serializers
from store.serializers import LanguageSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'email', 'admin', 'staff', 'active', 'languages')

    def get_languages(self, instance):
        instance.save()
        languages = instance.profile.languages.order_by('code')
        serializer = LanguageSerializer(languages, many=True)
        return serializer.data

from django.db import models
from corpus.core.utils.model import create_model, install_model
from .dictionnary import Dictionnary

"""
Language
"""
class Language(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    dictionnary = models.OneToOneField(Dictionnary, db_index=True, null=True,
                                     editable=False, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
         # create corresponding dictonnary object
        self.code = self.code.lower()
        if self.dictionnary is None:
            self.dictionnary = Dictionnary.objects.create()
        return super(Language, self).save(*args, **kwargs)
    
    def get_dictionnary_name(self):
        return self.code.lower()

    
    def get_user_list(self):
        return [ profile.user for profile in self.user_profile_set.all()]

    @property
    def serializer_data(self):
        from ..serializers import LanguageSerializer
        return LanguageSerializer(self).data





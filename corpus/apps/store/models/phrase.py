import uuid
from django.db import models
from django.db.models import Q
from rest_framework import serializers
import string


class PhraseQuerySet(models.query.QuerySet):
    def shorts_only(self, value=True):
        return self.filter(size_short=value, size_medium=False, size_long=False)

    def mediums_only(self, value=True):
        return self.filter(size_short=False, size_medium=value, size_long=False)

    def longs_only(self, value=True):
        return self.filter(size_short=False, size_medium=False, size_long=value)

    def sizes(self, **sizes):
        short = sizes.get('short', True)
        medium = sizes.get('medium', True)
        long  = sizes.get('long', True)

        return self.shorts_only(value=short) | self.mediums_only(value=medium) | self.longs_only(value=long)

class PhraseManager(models.Manager):
    def get_queryset(self):
        return PhraseQuerySet(self.model)

# Create your models here.
class Phrase(models.Model):
    text        = models.TextField(blank=True, null=True)
    shared_id   = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at  = models.DateTimeField(auto_now=True)

    # Phrases are classified by work count
    SHORT_SIZE  = 5       #   
    MEDIUM_SIZE = 10      #
    LONG_SIZE   = 1000    # 

    
    word_count       = models.IntegerField()
    size_short       = models.BooleanField(default=False)
    size_medium      = models.BooleanField(default=False)
    size_long        = models.BooleanField(default=False)
    
    byte_count       = models.IntegerField()

    editable         = models.BooleanField(default=False)

    objects = PhraseManager()


    # Need for tacking individual field changes
    __original_text = None
    __original_shared_id = None
    __changed = False


    class Meta:
        abstract  = True
        ordering  = ('-word_count',)

    def __str__(self):
        return f"(id:{self.id}, text: '{self.text}')"


    def save(self, force_insert=False,*args, **kwargs):
        
        # Check if there is not already a phrase with the same shared id
        phrase_model = type(self)
        try:
            existing_phrase = phrase_model.objects.get(shared_id=self.shared_id)
            existing_phrase.text = self.text
            self.__dict__.update(existing_phrase.__dict__)
        except phrase_model.DoesNotExist:
            pass

        self.word_count = sum([i.strip(string.punctuation).isalpha() for i in self.text.split()])
        self.size_short = self.SHORT_SIZE >= self.word_count
        self.size_medium = self.MEDIUM_SIZE >= self.word_count > self.SHORT_SIZE
        self.size_long = self.LONG_SIZE >= self.word_count > self.MEDIUM_SIZE
        # compute the bye compute
        compacted_text = ''.join([e for e in self.text if e.isalnum()])
        self.byte_count = len(compacted_text.encode('utf-8'))

        super(Phrase, self).save(force_insert=False,*args, **kwargs)

    
    def __str__(self):
        return f"(text:'{self.text}', shared_id(or id):'{self.shared_id}', word_count:{self.word_count})"

    @property
    def is_short_size(self):
        return self.size_short

    @property
    def is_medium_size(self):
        return self.size_medium
        
    @property
    def is_long_size(self):
        return self.size_long

    @property
    def serializer_data(self):
        from ..serializers import DynamicPhraseSerializer
        return DynamicPhraseSerializer(self).data



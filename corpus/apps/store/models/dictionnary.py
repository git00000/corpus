from django.db import models
from django.apps import apps
from django.db.utils import ProgrammingError
from corpus.core.utils.model import create_model, install_model
from django.utils.functional import cached_property
import uuid

from ..apps import StoreConfig
from .phrase import Phrase

def get_phrase_model_or_create(name):
    app_name = getattr(StoreConfig, 'name')
    app_label = getattr(StoreConfig, 'app_label', app_name) 
    
    try:
        model, created = apps.get_model(app_label,name), False
    except:
        model, created = create_model(
            name, parent_model=Phrase,app_label=app_label
        ), True

    return model, created

class DictionnaryQuerySet(models.query.QuerySet):
    pass

class DictionnaryManager(models.Manager):
    def get_query_set(self):
        return DictionnaryQuerySet(self.model) 


class Dictionnary(models.Model):
    # any changes to the `name` field may require updating the schema
    name = models.CharField(max_length=255, default=uuid.uuid4, null=False, blank=True)
    objects = DictionnaryManager()

    def save(self, *args, **kwargs):
        # Force validation of fields.
        self.full_clean(validate_unique=False)
        super(Dictionnary, self).save(*args, **kwargs)
    
    @cached_property
    def phrases(self):
        m, created = self.get_phrase_model_or_create()
        try:
            # make sure the table does exist
            # this line will trigger request to the databse
            if m.objects.all()[:1]:
                pass
        except ProgrammingError as e:
            # create the table if not exist
            install_model(m)
                
        return m.objects

    def get_phrase_model_or_create(self):
        return get_phrase_model_or_create(self.name)

    


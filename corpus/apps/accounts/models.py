from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from store.models import Language

from .managers import UserManager


class UserProfile(models.Model):
    languages = models.ManyToManyField(
                        Language, 
                        related_name="user_profile_set", 
                        related_query_name="user_profile_set", )


class User(AbstractBaseUser):
    email   = models.EmailField(max_length=100, null=False, blank=True, unique=True)
    active  = models.BooleanField(default=True) # can login
    staff   = models.BooleanField(default=False) # staff user none super
    admin   = models.BooleanField(default=False) # superuser
    
    profile =  models.OneToOneField(UserProfile, db_index=True, null=True,
                                     editable=False, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.profile is None:
            new_profile = UserProfile()
            new_profile.save()
            print('new profile')
            self.profile = new_profile
        
        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None): 
        print(perm)
        return self.admin

    def has_module_perms(self, app_label): 
        return self.admin

    @property
    def serializer_data(self):
        from .serializers import UserSerializer
        return UserSerializer(self).data



from django.db import models

# Create your models here.
from distutils.archive_util import make_zipfile
from pickle import TRUE
import uuid

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from django_countries.fields import CountryField

# # Create your models here
class FITUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        '''
            to set table name in database
        '''
        db_table = "FITUser"

    def __str__(self) -> str:
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(FITUser, on_delete=models.DO_NOTHING)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # add country column
    office = models.CharField(max_length=200)
    country = CountryField()
    designation = models.CharField(max_length=200)

    class Meta:
        '''
            to set table name in database
        '''
        db_table = "EmployeeProfileFIT"

        # permissions = (
        #     ("can_edit_ql", "Can Edit Quote Log"),
        #     ("can_create_ql", "Can create ql"),
        # )

    def __str__(self) -> str:
        return f"{self.office}"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

from django.db import models
from userroles.models import UserRole
from django.contrib.auth.models import AbstractBaseUser, UserManager


class TestModeratorProfile(UserRole):
    stars = models.IntegerField()


class TestUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'surname']

    objects = UserManager()

    def get_full_name(self):
        #This is a required method
        return self.first_name + ' ' + self.surname

    def get_short_name(self):
        #This is a required method
        return self.email

    def __unicode__(self):
        return self.email

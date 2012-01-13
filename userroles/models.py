from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserRole(models.Model):
    user = models.OneToOneField(User, related_name='role')
    name = models.CharField(max_length=64)

    def __eq__(self, other):
        return unicode(self) == unicode(other)

    def __unicode__(self):
        return 'manager'


#class UserProfile(models.Model):
#    user = models.OneToOneField(User)
#    role = models.ForeignKey(UserRole)


def create_user_role(sender, instance, created, **kwargs):
    if created:
        UserRole.objects.create(user=instance)

post_save.connect(create_user_role, sender=User)

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

import importlib


class UserRole(models.Model):
    user = models.OneToOneField(User, related_name='role')
    name = models.CharField(max_length=64)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __eq__(self, other):
        return unicode(self) == unicode(other)

    def __unicode__(self):
        return self.name

    def __getattr__(self, name):
        if name == '_content_object_cache':
            return super(UserRole, self).__getattr__(name)
        return getattr(self.content_object, name)


def create_user_role(sender, instance, created, **kwargs):
    if created:
        (name, user_role_str) = settings.USER_ROLES[0]
        if user_role_str:
            mod_str, cls_str = user_role_str.rsplit('.', 1)
            user_role = getattr(importlib.import_module(mod_str), cls_str)
            kwargs = {'content_object': user_role.objects.create()}
        else:
            kwargs = {}
        UserRole.objects.create(user=instance, name=name, **kwargs)


post_save.connect(create_user_role, sender=User)

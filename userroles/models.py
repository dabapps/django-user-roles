from django.contrib.auth.models import User
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes import generic
from django.conf import settings
from django.db import models

import importlib


def _string_to_class(class_as_string):
    module_str, class_str = class_as_string.rsplit('.', 1)
    return getattr(importlib.import_module(module_str), class_str)


def _get_user_role_default():
    user_roles = getattr(settings, 'USER_ROLES', None)
    if not user_roles:
        return ''
    return user_roles[0][0]


def _get_user_role_choices():
    user_roles = getattr(settings, 'USER_ROLES', None)
    if not user_roles:
        return [('', '')]
    return [(name, name) for (name, model) in user_roles]


class UserRole(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64, default=_get_user_role_default,
                            choices=_get_user_role_choices())

    def __unicode__(self):
        return self.name

    def __eq__(self, other):
        return unicode(self) == unicode(other)


def _get_role(user):
    setting = getattr(settings, 'USER_ROLE_CLASS', None)
    user_role_class = setting and _string_to_class(setting) or UserRole
    return user_role_class.objects.get_or_create(user=user)[0]


def _set_role(user, role_name):
    role = user.role
    role.name = role_name
    role.full_clean()
    role.save()

User.role = property(_get_role, _set_role)


# class UserRoleProfile(models.Model):
#     user = models.OneToOneField(User, related_name='role')
#     name = models.CharField(max_length=64)
#     content_type = models.ForeignKey(ContentType, null=True)
#     object_id = models.PositiveIntegerField(null=True)
#     content_object = generic.GenericForeignKey('content_type', 'object_id')

#     def __eq__(self, other):
#         return unicode(self) == unicode(other)

#     def __unicode__(self):
#         return self.name

#     def __getattr__(self, name):
#         if name == '_content_object_cache':
#             return super(UserRole, self).__getattr__(name)
#         return getattr(self.content_object, name)


# def create_user_role(sender, instance, created, **kwargs):
#     if created:
#         (name, user_role_str) = settings.USER_ROLES[0]
#         if user_role_str:
#             mod_str, cls_str = user_role_str.rsplit('.', 1)
#             user_role = getattr(importlib.import_module(mod_str), cls_str)
#             kwargs = {'content_object': user_role.objects.create()}
#         else:
#             kwargs = {}
#         UserRole.objects.create(user=instance, name=name, **kwargs)


#post_save.connect(create_user_role, sender=User)

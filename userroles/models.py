from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from userroles import roles, _import_class_from_string


class UserRole(models.Model):
    user = models.OneToOneField(User, related_name='role')
    name = models.CharField(max_length=100, choices=roles.choices)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    profile = generic.GenericForeignKey('content_type', 'object_id')
    valid_roles = roles

    class Meta:
        abstract = bool(getattr(settings, 'USER_ROLE_CLASS', None))

    def __eq__(self, other):
        return self.name == other.name

    def __getattr__(self, name):
        if name.startswith('is_'):
            role = getattr(self.valid_roles, name[3:], None)
            if role:
                return self == role
        raise AttributeError("'%s' object has no attribute '%s'" %
                             (self.__class__.__name__, name))


def set_user_role(user, role):
    user_role_string = getattr(settings, 'USER_ROLE_CLASS', None)
    user_role_class = _import_class_from_string(user_role_string) or UserRole
    role = user_role_class(user=user, name=role.name)
    role.save()

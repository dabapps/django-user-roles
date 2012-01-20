from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from userroles import roles


class UserRole(models.Model):
    user = models.OneToOneField(User, related_name='role')
    name = models.CharField(max_length=100, choices=roles.choices)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    profile = generic.GenericForeignKey('content_type', 'object_id')
    valid_roles = roles

    def __eq__(self, other):
        return self.name == other.name

    def __getattr__(self, name):
        if name.startswith('is_'):
            role = getattr(self.valid_roles, name[3:], None)
            if role:
                return self == role
        raise AttributeError("'%s' object has no attribute '%s'" %
                             (self.__class__.__name__, name))

    def __unicode__(self):
        return self.name


def set_user_role(user, role):
    try:
        role_obj = UserRole.objects.get(user=user)
    except UserRole.DoesNotExist:
        role_obj = UserRole(user=user, name=role.name)
    else:
        role_obj.name = role.name
    role_obj.save()

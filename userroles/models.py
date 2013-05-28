import django.contrib.auth
from django.db import models
from userroles import roles
from django.conf import settings

if hasattr(django.contrib.auth, 'get_user_model'):
    user_model = settings.AUTH_USER_MODEL
else:
    user_model = 'auth.User'


class UserRole(models.Model):
    user = models.OneToOneField(user_model, related_name='role')
    name = models.CharField(max_length=100, choices=roles.choices)
    child = models.CharField(max_length=100, blank=True)
    _valid_roles = roles

    @property
    def profile(self):
        if not self.child:
            return None
        return getattr(self, self.child)

    def __eq__(self, other):
        return self.name == other.name

    def __getattr__(self, name):
        if name.startswith('is_'):
            role = getattr(self._valid_roles, name[3:], None)
            if role:
                return self == role

        raise AttributeError("'%s' object has no attribute '%s'" %
                              (self.__class__.__name__, name))

    def __unicode__(self):
        return self.name


def set_user_role(user, role, profile=None):
    if profile:
        try:
            UserRole.objects.get(user=user).delete()
        except UserRole.DoesNotExist:
            pass
        profile.user = user
        profile.name = role.name
        profile.child = str(profile.__class__.__name__).lower()

    else:
        try:
            profile = UserRole.objects.get(user=user)
        except UserRole.DoesNotExist:
            profile = UserRole(user=user, name=role.name)
        else:
            profile.name = role.name

    profile.save()
    user.role = profile

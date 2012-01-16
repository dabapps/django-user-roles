from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import importlib


def set_user_role(user, role, profile=None):
    user.role = role

_CONFIGURATION_ERROR = "USER_ROLES should be a list of strings and/or two-tuples"


def _import_class_from_string(class_path):
    """
    Given a string like 'foo.bar.Baz', returns the class it refers to.
    If the string is empty, return None, rather than raising an import error.
    """
    if not class_path:
        return None
    module_path, class_name = class_path.rsplit('.', 1)
    return getattr(importlib.import_module(module_path), class_name)


class Role(object):
    def __init__(self, name, profile):
        self.name = name
        self.profile = profile


class Roles(object):
    @property
    def roles_dict(self):
        if not hasattr(self, '_roles_dict'):
            self._roles_dict = {}
            for item in getattr(settings, 'USER_ROLES', ()):
                if isinstance(item, basestring):
                    # An item like 'manager'
                    self._roles_dict[item] = None
                elif len(item) == 2:
                    # An item like ('manager', 'myapp.models.ManagerProfile')
                    name, profile = item
                    self._roles_dict[name] = _import_class_from_string(profile)
                else:
                    # Anything else
                    raise ImproperlyConfigured(_CONFIGURATION_ERROR)
        return self._roles_dict

    def __getattr__(self, name):
        try:
            return Role(name, self.roles_dict[name])
        except KeyError:
            raise AttributeError("No such role exists '%s'" % name)

    def choices(self):
        return [(role, role) for role in self.roles_dict.items()]

roles = Roles()

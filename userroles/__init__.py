from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import importlib
from collections import namedtuple


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


Role = namedtuple('Role', ['name'])


class Roles(object):
    _roles_dict = None

    @property
    def roles_dict(self):
        """
        Load USER_ROLES setting into {name: ...}
        """
        if self._roles_dict is None:
            self._roles_dict = {}
            for item in getattr(settings, 'USER_ROLES', ()):
                if isinstance(item, basestring):
                    # An item like 'manager'
                    self._roles_dict[item] = None
                elif len(item) == 2:
                    # An item like ('manager', 'myapp.models.ManagerProfile')
                    name, profile = item
                    self._roles_dict[name] = profile
                else:
                    # Anything else
                    raise ImproperlyConfigured(_CONFIGURATION_ERROR)
        return self._roles_dict

    @property
    def choices(self):
        """
        Return a list of two-tuples of role names, suitable for use as the
        'choices' argument to a model field.
        """
        return [(role, role) for role in self.roles_dict.keys()]

    def __getattr__(self, name):
        if name in self._roles_dict.keys():
            return Role(name=name)
        else:
            raise AttributeError("No such role exists '%s'" % name)

roles = Roles()

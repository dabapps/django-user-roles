from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import importlib


__version__ = '0.1.0'


_IMPORT_FAILED = "Could not import role profile '%s'"
_INCORRECT_ARGS = "USER_ROLES should be a list of strings and/or two-tuples"


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
    """
    A single role, eg as returned by `roles.moderator`.
    """
    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.name


class Roles(object):
    _roles_mapping = None

    @property
    def roles_mapping(self):
        """
        Load list style config into list of of (role_name, role_class) tuples
        """
        if self._roles_mapping is None:
            self._roles_mapping = []
            for item in self._config:
                if isinstance(item, basestring):
                    # An item like 'manager'
                    self._roles_mapping.append((item, None))
                else:
                    # Anything else
                    raise ImproperlyConfigured(_INCORRECT_ARGS)
        return self._roles_mapping

    @property
    def choices(self):
        """
        Return a list of two-tuples of role names, suitable for use as the
        'choices' argument to a model field.
        """
        return [(role, role) for role in self.roles_mapping]

    def __init__(self, config=None):
        """
        By default the Roles object will be created using configuration from
        the django settings file, but you can also set the configuration
        explicitly, for example, when testing.
        """
        self._config = config or getattr(settings, 'USER_ROLES', ())

    def __getattr__(self, name):
        """
        Handle custom properties for returning Role objects.
        For example: `roles.moderator`
        """
        for role_name, _ in self.roles_mapping:
            if role_name == name:
                return Role(name=name)
        raise AttributeError("No such role exists '%s'" % name)

roles = Roles()

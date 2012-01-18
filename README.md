Django User Roles
=================

Simple role-based user permissions for Django.

django-user-roles is a simple, reusable app that allows you to create a set of user roles, which can be used to control which views each type of user has permission to view, and to customize how the site is presented to different types of user.

<!--
User roles can also be associated with differing profile classes, allowing you to store different types of user information for different user types.
-->

Settings
--------

Install using `pip`:

	pip install django-user-roles

Add the `USER_ROLES` setting to your `settings.py`.  For example:

    USER_ROLES = (
        'manager',
        'moderator',
        'client',
    )

<!--
Optionally, you can also store profile information specific to each role:

    USER_ROLES = (
        ('manager', 'myproject.ManagerUserProfile'),
        ('moderator', 'myproject.ModeratorUserProfile'),
        ('client', 'myproject.ClientUserProfile'),
    )
-->

Basic Usage
-----------

Setting the user role:

	from userroles.models import set_user_role
    from userroles import roles

    set_user_role(self.user, roles.manager)

<!--
    set_user_role(self.user, roles.manager, myproject.ManagerUserProfile(...))
-->

Checking the user role:

	from userroles import roles

    user.role == roles.manager
    user.role in (roles.manager, roles.moderator)
    user.role.is_moderator


The `role_required` decorator provides similar behavior to Django's `login_required` and `permission_required` decorators.  If the user accessing the view does not have the required roles, they will be redirected to the login page:

    from userroles.decorators import role_required
	from userroles import roles

    @role_required(roles.manager, roles.moderator)
    def view(request):
        ...

Using Custom Role Classes
-------------------------

It can sometime be useful to override the default user role class.
You can do this by setting `USER_ROLE_CLASS` in your settings file.

`settings.py`:

    USER_ROLE_CLASS = 'myapp.models.CustomUserRole'

`models.py`:

    def CustomUserRole(userroles.UserRole):
        @property
        def can_moderate_discussions(self):
        	return self.is_moderator or self.is_manager

`views.py`:

	def view(request):
        if user.role.can_moderate_discussions:
            ...
		else:
			...

Testing
-------

    ./manage.py test userroles

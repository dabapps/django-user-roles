Django User Roles
=================

Role-based user profiles for Django.


Django User Profiles is a reusable app that allows you to assign users to
fixed 

A User role:

1.  May have a set of user information applicable to that role that varies
    between roles.
2.  


settings
--------

USER_ROLES = (
    ('name', 'myproject.ManagerUserRole'),
)

testing
-------

./manage.py test userroles

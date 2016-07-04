LDAP Password
=============

This module changes the LDAP password of the Odoo user via the normal password change dialogue.

This module requires auth_ldap module

When an Odoo user changes its password, this module will try to first authenticate the current user via one of the configured LDAP servers, and if successful, first bind as this user with its old_password and then issue modify request of the 'userPassword' attribute with the new passowrd.


Your LDAP server must allow users change their own 'userPassword' attribute.

You can easily modify the code to change any other password attribute according to your LDAP setup.

Any feedback is welcome at <alexis@ww.net>

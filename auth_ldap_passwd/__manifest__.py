# -*- coding: utf-8 -*-
{
    'name': "auth_ldap_passwd",

    'summary': """
        LDAP password change from Odoo""",

    'description': """
        Changes user's LDAP password when it is changed in Odoo. Password reset links do not work.
        As a security safeguard if this module is installed the database passwords can not be changed.
    """,

    'author': "Alexis Yushin, White Willow B.V. <alexis@ww.net>",
    'website': "https://github.com/wwnet/odoo-addons",

    'category': 'Authentication',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['auth_ldap'],

}

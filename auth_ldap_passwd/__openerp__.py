# -*- coding: utf-8 -*-
{
    'name': "auth_ldap_passwd",

    'summary': """
	LDAP password change from Odoo
        """,

    'description': """
        Changes user's LDAP password when it is changed in Odoo. Password reset links do not work.
        As a security safeguard if this module is installed the database passwords can not be changed.
    """,

    'author': "Alexis Yushin, White Willow B.V. <alexis@ww.net>",
    'website': "http://ww.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Authentication',
    'version': '0.1',
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['auth_ldap'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
     #   'demo/demo.xml',
    ],
}

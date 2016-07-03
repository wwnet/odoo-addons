# -*- coding: utf-8 -*-
{
    'name': "account_bank_statement_import_mt940_nl",

    'summary': """
	MT940 bank statement import for Dutch banks.
        """,

    'description': """
    This module allows you to import MT940 files in Odoo.

	At the moment only supports ING NL, might work with other banks, but not yet tested.
	    """,

    'author': "White Willow B.V.",
    'website': "http://ww.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting & Finance',
    'version': '0.1',
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['account_bank_statement_import'],

}

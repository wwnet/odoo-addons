# -*- coding: utf-8 -*-
{
    'name': "account_bank_statement_import_mt940_nl",

    'summary': """
	This module imports MT940 statements for Dutch banks
	""",

    'description': """
	Module to import MT940 bank statements
	======================================

	This module allows you to import MT940 files in Odoo: they are parsed and stored in human readable format in
	Accounting \ Bank and Cash \ Bank Statements.

	At the moment only supports ING NL, might work with other banks, but not yet tested.
    """,
    'author': "White Willow BV",
    'website': "http://ww.net",
    'category': 'Accounting & Finance',
    'version': '0.1',
    'depends': ['account_bank_statement_import'],
}

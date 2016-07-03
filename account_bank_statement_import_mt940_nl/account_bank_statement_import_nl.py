# -*- coding: utf-8 -*-
#
# Some code borrowed from be-cloud (Jerome Sonnet)
#
# Alexis Yushin <alexis@ww.net>
#
#
# We should check the IBAN of the account identification and automatically recognize
# the bank and its format and handle them all in account_bank_statement_import_mt940
#
# This module assumes the statement is in the format as specified in
# doc/ING_ftp_unstructured_mt940_942_format_description_the_netherlands_february_2014_2_tcm162-45688.pdf
#

from openerp import api, fields, models, _
from openerp.exceptions import UserError

from mt940 import MT940, ing_description

import logging
import StringIO
import re

_logger = logging.getLogger(__name__)



class AccountBankStatementImport(models.TransientModel):

    _inherit = 'account.bank.statement.import'

    def _parse_file(self, data_file):

        currency = None
        account = None
        statements = []

        try:
            # invoke the MT940 parser
            f = StringIO.StringIO(data_file)
            mt940 = MT940(f)

            # if no statements found
            if not mt940.statements:
                _logger.info("Statement file was not recognized as an MT940 file, trying next parser", exc_info=True)
                return super(AccountBankStatementImport, self)._parse_file(data_file)

            # we iterate through each statement
            for st in mt940.statements:
                # check if the statement is in the same currency as the acccount and set the currency if its the first statement
                if st.start_balance.currency != st.end_balance.currency:
                    raise ValueError('Statement end balance is in a different currency than start balance')

                if not currency:
                    currency = st.start_balance.currency
                elif currency != st.start_balance.currency:
                    raise ValueError('Multiple currencies are not supported in one file')

                # ING account identification is IBAN+CUR
                m = re.match('(NL\d\dINGB\d+)'+currency, st.account, re.IGNORECASE)
                if not m:
                    raise ValueError('The account identification for ING bank must be IBAN+CUR, where CUR is the account currency 3 letter code')
                if not account:
                    account = m.group(1)
                elif account != m.group(1):
                    raise ValueError('Multiple accounts are not supported in one file')

                # initialize a new statement
                statement = {
                    'name'              : account + '-' + st.statement + '-' + st.information,
                    'date'              : st.end_balance.date,
                    'balance_start'     : st.start_balance.amount,
                    'balance_end_real'  : st.end_balance.amount,
                    'transactions'      : []
                }

                # iterate through the transactions
                for tr in st.transactions:

                    # XXX: will try to guess the bank, for now assume ING IBAN
                    details = ing_description(tr.description)

                    # generic part
                    transaction = {
                        'date'              : tr.date,
                        'amount'            : tr.amount,
                        'unique_import_id'  : tr.institution_reference,
                        'note'              : details.get('remi', {'remitance_info': None}).get('remittance_info'),
                        'eref'              : details.get('eref'),
                        'account_number'    : details.get('cntp', {'account_number': None}).get('account_number')
                    }

                    # At this stage if both name and remittance_info are empty we quit
                    transaction['name'] = details.get('cntp', {'name': None}).get('name') or transaction['note'] or transaction['account_number']

                    statement['transactions'].append(transaction)

                # add the statement to the statements
                statements.append(statement)

            return currency, account, statements

        except ValueError, e:
            _logger.info(e)
            raise UserError(_("The following problem occurred during import. The file might not be valid.\n\n %s" % e.message))

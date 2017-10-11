# -*- coding: utf-8 -*-

import logging
import ldap

_logger = logging.getLogger(__name__)

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessDenied


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def change_password(self, old_passwd, new_passwd):
        """Changes the LDAP password of the current user on the LDAP server.

        :return: True
        :raise: odoo.exceptions.AccessDenied when old password is wrong
        :raise: odoo.exceptions.UserError when new password is not set or empty
        """

        if not new_passwd:
            raise UserError("New password is missing.")

        _logger.info("Changing LDAP password for used id %s", self._uid)

        Ldap = self.env['res.company.ldap']

        for conf in Ldap.get_ldap_dicts():
            try:
                # _logger.info("Trying %s", self.env.user.login)
                ldap_user = Ldap.authenticate(
                    conf, self.env.user.login, old_passwd)
                if ldap_user:
                    _logger.info("Authenticated LDAP user %s", ldap_user[0])
                    conn = Ldap.connect(conf)
                    conn.simple_bind_s(ldap_user[0], old_passwd)

                    add_pass = [(ldap.MOD_REPLACE, 'userPassword',
                                 [new_passwd.encode('utf-8)')])]
                    _logger.info('Modifying LDAP password for %s' % ldap_user[0])
                    conn.modify_s(ldap_user[0], add_pass)
                    conn.unbind()

                    return True

            except ldap.INVALID_CREDENTIALS:
                _logger.error("LDAP bind failed.")
                raise AccessDenied

            except ldap.LDAPError, e:
                _logger.error('An LDAP exception occurred: %s', e)

        _logger.error('Unable authenticate user %s in LDAP', self.env.user.login)
        raise AccessDenied

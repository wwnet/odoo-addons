import ldap
import logging

import openerp.exceptions
from openerp import tools
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp.modules.registry import RegistryManager
_logger = logging.getLogger(__name__)


class res_users(osv.osv):
    _inherit = "res.users"

    def change_password(self, cr, uid, old_passwd, new_passwd, context=None):
        """Change LDAP password of the current user.

        :return: True
        :raise: openerp.exceptions.AccessDenied when old password is wrong
        :raise: except_osv when new password is not set or empty
        """

        # Find out the login name
        cr.execute('SELECT login FROM res_users WHERE id=%s AND active=TRUE', (int(uid),))
        res = cr.fetchone()

        if res:
            _logger.info("Changing LDAP password for user %s" % res[0])
            ldap_obj = self.pool['res.company.ldap']

            for conf in ldap_obj.get_ldap_dicts(cr):
                try:
                    ldap_user = ldap_obj.authenticate(conf, res[0], old_passwd)

                    if ldap_user:
                        conn = ldap_obj.connect(conf)
                        conn.simple_bind_s(ldap_user[0], old_passwd)

                        if not new_passwd:
                            raise openerp.exceptions.except_osv

                        add_pass = [(ldap.MOD_REPLACE, 'userPassword', [new_passwd.encode('utf-8)')])]
                        _logger.info('Changing LDAP password for %s' % ldap_user[0])

                        conn.modify_s(ldap_user[0], add_pass)

                        conn.unbind()

                        return True

                except ldap.INVALID_CREDENTIALS:
                    _logger.error("LDAP bind failed.")
                    raise openerp.exceptions.AccessDenied

                except ldap.LDAPError, e:
                    _logger.error('An LDAP exception occurred: %s', e)
        else:
            _logger.error('User id %d does not exist in the database' % int(uid))

        _logger.error('User %s not found in LDAP' % res[0])
        raise openerp.exceptions.except_osv
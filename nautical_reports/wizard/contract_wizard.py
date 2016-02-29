# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import models, api


class create_contract(models.TransientModel):
    _inherit = 'create_contract'

    @api.multi
    def create_contract(self):
        super(create_contract, self).create_contract()
        active_id = self._context.get('active_id', False)
        craft = self.env['nautical.craft'].browse(active_id)
        if self._context.get('print_report', False):
            return self.env['report'].get_action(craft, 'report_alta_odt')

# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import models, api


class contract_cancelled_wizard(models.TransientModel):
    _inherit = 'contract_cancelled_wizard'

    @api.multi
    def contract_cancelled_wizard(self):
        active_id = self._context.get('active_id', False)
        craft = self.env['nautical.craft'].browse(active_id)
        super(contract_cancelled_wizard, self).contract_cancelled_wizard()
        if self._context.get('print_report', False):
            return self.env['report'].get_action(craft, 'report_baja_odt')

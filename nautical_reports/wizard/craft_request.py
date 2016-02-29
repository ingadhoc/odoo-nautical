# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import models, api


class craft_request(models.TransientModel):
    _inherit = 'craft_request'

    @api.multi
    def craft_request(self):
        super(craft_request, self).craft_request()
        if self.request_type == 'transitional_retirement' and self._context.get('print_report', False):
            active_id = self._context.get('active_id', False)
            craft = self.env['nautical.craft'].browse(active_id)
            return self.env['report'].get_action(craft, 'retirement_report_odt')

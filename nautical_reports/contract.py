# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class contract(models.Model):
    """Contract"""

    _inherit = 'nautical.contract'

    number = fields.Integer('Contract Number')

    @api.multi
    def low_report_print(self):

        assert len(self) == 1
        return self.env['report'].get_action(self.craft_id, 'report_baja_odt')

    @api.multi
    def contract_alta_print(self):

        assert len(self) == 1
        return self.env['report'].get_action(self.craft_id, 'report_alta_odt')

# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class craft(models.Model):
    """Craft"""

    _inherit = 'nautical.craft'

    @api.multi
    def contract_alta_print(self):

        assert len(self) == 1
        return self.env['report'].get_action(self, 'report_alta_odt')

    @api.multi
    def retirement_report_print(self):

        assert len(self) == 1
        return self.env['report'].get_action(self, 'retirement_report_odt')

    @api.multi
    def low_report_print(self):

        assert len(self) == 1
        return self.env['report'].get_action(self, 'report_baja_odt')

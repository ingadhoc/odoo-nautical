# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from datetime import date


class res_partner(models.Model):
    """Craft"""

    _inherit = 'res.partner'

    count_debt_invoice = fields.Integer(compute='_get_count_debt_invoice')

    @api.one
    def _get_count_debt_invoice(self):
        invoices = self.env['account.invoice'].search(
            [('partner_id', '=', self.id),
             ('type', 'in', [
                 'out_invoice', 'out_refund']),
             ('state', 'not in', ['draft', 'cancel', 'paid']),
             ('date_due', '<', date.today())])
        self.count_debt_invoice = len(invoices)

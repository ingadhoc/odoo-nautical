from openerp import models, api


class partner_debt(models.TransientModel):
    """"""
    _name = 'nautical_partner_debt.wizard'

    @api.multi
    def members_print(self):
        assert len(self) == 1
        partners = self.env['res.partner'].search([('customer', '=', True)])
        return self.env['report'].get_action(partners, 'partner_debt_report')

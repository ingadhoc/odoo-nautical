from openerp import models, api


class member_wizard(models.TransientModel):
    """"""
    _name = 'nautical_member.wizard'
    _description = 'wizard'

    @api.multi
    def members_print(self):
        assert len(self) == 1
        partners = self.env['res.partner'].search([('customer','=',True)])
        return self.env['report'].get_action(partners, 'report_member_odt')

from openerp import netsvc
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import except_orm

class authorizations_cancellations(models.Model):
    """"""
    _name = 'nautical_ab.wizard'
    _description = 'Wizard to AB'

   
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    type = fields.Selection([('authorizations', 'Authorizations'),('cancellations', 'Cancellations')], string='Type', required=True)
    


    @api.multi
    def list_generated(self):
        assert len(self) == 1
        if self.type == 'authorizations':
            contracts = self.env['nautical.contract'].search([('start_date','<',self.date_to),('start_date','>',self.date_from)])
            if contracts:
                total= len(contracts)
                return self.env['report'].with_context(total_amount=total).get_action(contracts, 'authorizations_report_odt')
            else:
                raise except_orm(_("No records of contracts on these dates"),_(''))
        elif self.type == 'cancellations':
            contracts = self.env['nautical.contract'].search([('expiration_date','>',self.date_from),('expiration_date','<',self.date_to)])
            if contracts:
                total= len(contracts)
                return self.env['report'].with_context(total_amount=total).get_action(contracts, 'cancellations_report_odt')
            else:
                # raise except_orm(_("No records of contracts on these dates"))
                raise except_orm(_("No records of contracts on these dates"),_(''))

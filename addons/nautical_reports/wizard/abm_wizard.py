from openerp import netsvc
from openerp import models, fields, api
from openerp.tools.translate import _

class altas_bajas(models.Model):
    """"""
    _name = 'nautical_ab.wizard'
    _description = 'Wizard to AB'

   
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    


    @api.multi
    def list_generated(self):
        assert len(self) == 1
        contract = self.env['nautical.contract'].search([('state','=','contracted')])
        return self.env['report'].with_context(active_ids=contract.ids, active_model='nautical.contract').get_action(self, 'ab_report_odt')
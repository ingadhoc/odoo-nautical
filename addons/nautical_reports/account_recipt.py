from openerp import netsvc
from openerp import models, fields, api
from openerp.tools.translate import _



class recipt(models.Model):
    """"""
    
    _inherit = 'account.voucher'

   

    @api.multi
    def recipt_print(self):
        
        assert len(self) == 1
        return self.env['report'].get_action(self, 'report_receipt_odt')
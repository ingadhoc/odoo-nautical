# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import netsvc
from openerp import models, fields, api
from openerp.tools.translate import _



class contract(models.Model):
    """Contract"""
    
    _inherit = 'nautical.contract'

   

    _columns = {
        
        
    }

    @api.multi
    def contract_print(self):
        
        assert len(self) == 1
        return self.env['report'].get_action(self, 'report_contract_odt')

    

    
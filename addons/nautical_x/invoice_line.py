# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp import models, api, fields

class invoice_line(models.Model):
    """"""
    
    _name = 'account.invoice.line'
    _inherit = [ 'account.invoice.line' ]

    craft_id = fields.Many2one('nautical.craft', string='Craft')


    @api.onchange('craft_id')
    def onchange_craft_id(self):

        if self.craft_id:
            self.product_id = self.craft_id.product_id
           





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class product(osv.osv):
    """"""
    
    _name = 'product.product'
    _inherits = {  }
    _inherit = [ 'product.product' ]

    _columns = {
        'craft_type': fields.selection([(u'craft', u'Craft'), (u'kayak', u'Kayak')], string='Craft Type'),
    }

    _defaults = {
    }


    _constraints = [
    ]




product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

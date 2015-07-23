# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


import re
from openerp import netsvc
from openerp.osv import osv, fields

class template(osv.osv):
    """"""
    
    _inherit = 'product.template'

    _columns = {
        'type': fields.selection([('product','Stockable Product'),('consu', 'Consumable'),('service','Service'),('storage_service', 'Storage Service')], 'Product Type', required=True, help="Consumable: Will not imply stock management for this product. \nStockable product: Will imply stock management for this product."),
    }

    _defaults = {
    }


    _constraints = [
    ]




template()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

import re
from openerp import netsvc
from openerp.osv import osv, fields

class service_authorization(osv.osv):
    """Service Authorization"""
    
    _name = 'nautical.service_authorization'
    _description = 'Service Authorization'

    _columns = {
        'supplier_id': fields.many2one('res.partner', string='Supplier', required=True, context={'default_supplier':True}, domain=[('supplier','=',True)]),
        'expiration_date': fields.date(string='Expiration Date', required=True),
        'craft_id': fields.many2one('nautical.craft', string='Craft', required=True, ondelete='cascade'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




service_authorization()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

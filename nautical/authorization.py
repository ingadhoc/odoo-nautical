# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class authorization(osv.osv):
    """Authorizations"""
    
    _name = 'nautical.authorization'
    _description = 'Authorizations'

    _columns = {
        'authorization_type_id': fields.many2one('nautical.authorization_type', string='Authorization Type', required=True),
        'partner_id': fields.many2one('res.partner', string='Partner', required=True), 
        'craft_id': fields.many2one('nautical.craft', string='Craft', required=True, ondelete='cascade'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




authorization()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

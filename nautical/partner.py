# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class partner(osv.osv):
    """"""
    
    _name = 'res.partner'
    _inherits = {  }
    _inherit = [ 'res.partner' ]

    _columns = {
        'authorization_ids': fields.one2many('nautical.authorization', 'partner_id', string='Authorizations'), 
        'historical_record_ids': fields.one2many('nautical.partner_record', 'partner_id', string='historical_record_ids'), 
        'owned_craft_ids': fields.one2many('nautical.craft', 'owner_id', string='Owned Crafts'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

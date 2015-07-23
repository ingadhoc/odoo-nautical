# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class role_book(osv.osv):
    """"""
    
    _name = 'nautical.role_book'
    _description = 'role_book'

    _columns = {
        'estimated_dep_date': fields.datetime(string='Estimated Departure Date', required=True),
        'partner_id': fields.many2one('res.partner', string='Partner', readonly=True, required=True),
        'destiny': fields.char(string='Destiny'),
        'crew_qty': fields.integer(string='Crew'),
        'est_arrival_date': fields.datetime(string='Estimated Arrival Date'),
        'craft_id': fields.many2one('nautical.craft', string='Craft', readonly=True, required=True, ondelete='cascade'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




role_book()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

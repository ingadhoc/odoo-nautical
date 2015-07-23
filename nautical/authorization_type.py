# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class authorization_type(osv.osv):
    """Authorization Type"""
    
    _name = 'nautical.authorization_type'
    _description = 'Authorization Type'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'can_sail': fields.boolean(string='Can Sail'),
    }

    _defaults = {
    }

    _order = "name"

    _constraints = [
    ]




authorization_type()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

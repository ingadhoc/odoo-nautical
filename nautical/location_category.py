# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class location_category(osv.osv):
    """"""
    
    _name = 'nautical.location_category'
    _description = 'location_category'

    _columns = {
        'name': fields.char(string='Name', required=True),
    }

    _defaults = {
    }


    _constraints = [
    ]




location_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

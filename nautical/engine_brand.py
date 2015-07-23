# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class engine_brand(osv.osv):
    """Engine Brand"""
    
    _name = 'nautical.engine_brand'
    _description = 'Engine Brand'

    _columns = {
        'name': fields.char(string='Name', required=True),
    }

    _defaults = {
    }


    _constraints = [
    ]




engine_brand()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

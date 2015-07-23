# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class craft_material(osv.osv):
    """Craft Material"""
    
    _name = 'nautical.craft_material'
    _description = 'Craft Material'

    _columns = {
        'name': fields.char(string='Name', required=True),
    }

    _defaults = {
    }


    _constraints = [
    ]




craft_material()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

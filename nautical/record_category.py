# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class record_category(osv.osv):
    """Record Category"""
    
    _name = 'nautical.record_category'
    _description = 'Record Category'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'partner_record_id': fields.many2many('nautical.partner_record', 'nautical_categ_ids___rel', 'record_category_id', 'partner_record_id', string='&lt;no label&gt;'), 
    }

    _defaults = {
    }

    _order = "name"

    _constraints = [
    ]




record_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

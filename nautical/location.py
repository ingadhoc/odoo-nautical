# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class location(osv.osv):
    """Location"""
    
    _name = 'nautical.location'
    _description = 'Location'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'ref': fields.char(string='Ref', required=True),
        'sufix': fields.char(string='Sufix'),
        'type': fields.selection([(u'normal', u'Normal'), (u'view', u'View')], string='Type', required=True),
        'craft_id': fields.many2one('nautical.craft', string='Craft', domain=[('state','not in',['permanent_cancellation', 'draft'])]), 
        'parent_id': fields.many2one('nautical.location', string='Parent Location', context={'default_type':'view','from_child':True}, domain=[('type','=', 'view')]), 
        'child_ids': fields.one2many('nautical.location', 'parent_id', string='Child Locations'), 
    }

    _defaults = {
    }

    _order = "name"

    _constraints = [
    ]




location()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

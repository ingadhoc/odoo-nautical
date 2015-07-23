# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class partner_record(osv.osv):
    """Partner Record"""
    
    _name = 'nautical.partner_record'
    _description = 'Partner Record'

    _columns = {
        'date': fields.date(string='Date', required=True),
        'user_id': fields.many2one('res.users', string='User', required=True),
        'note': fields.text(string='Note', required=True),
        'partner_id': fields.many2one('res.partner', string='&lt;no label&gt;', ondelete='cascade'), 
        'categ_ids': fields.many2many('nautical.record_category', 'nautical_categ_ids___rel', 'partner_record_id', 'record_category_id', string='Tags', required=True), 
    }

    _defaults = {
    }

    _order = "date desc"

    _constraints = [
    ]




partner_record()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

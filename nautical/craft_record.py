# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.osv import osv, fields

class craft_record(osv.osv):
    """Craft Record"""
    
    _name = 'nautical.craft_record'
    _description = 'Craft Record'

    _columns = {
        'date': fields.datetime(string='Date', required=True),
        'user_id': fields.many2one('res.users', string='User', required=True),
        'requestor_id': fields.many2one('res.partner', string='Requestor'),
        'type': fields.selection([(u'draft', u'Draft'), (u'to_dispatch', u'To Dispatch'), (u'sailing', u'Sailing'), (u'in_reparation', u'In Reparation'), (u'in_custody', u'In Custody'), (u'transitional_retirement', u'Transitional Retirement'), (u'expired', u'Expired'), (u'contracted', u'Contracted'), (u'stored', u'Stored'), (u'do_not_dispatch', u'Do not Dispatch'), (u'permanent_cancellation', u'Permanent Cancellation'), (u'other', u'Other'), (u'picked', u'Picked')], string='Type', required=True),
        'note': fields.text(string='Note'),
        'craft_id': fields.many2one('nautical.craft', string='Craft', required=True, ondelete='cascade'), 
    }

    _defaults = {
    }

    _order = "date desc"

    _constraints = [
    ]


    def newOperation(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError



craft_record()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

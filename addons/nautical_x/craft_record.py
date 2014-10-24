# -*- coding: utf-8 -*-


import re
from openerp import netsvc
from openerp.osv import osv, fields

class craft_record(osv.osv):
    """Craft Record"""
    
    _inherit = 'nautical.craft_record'

    _columns = {
        'attachment_ids': fields.many2many('ir.attachment', 'craft_record_attachment_rel','contract_id', 'attachment_id', 'Attachments'),
    }

    _defaults = {
        'user_id': lambda s, cr, u, c: u,
        'date': lambda *a: fields.datetime.now(),
        # 'date': lambda self, cr, uid, ctx: ctx.get('date', fields.date.context_today(self,cr,uid,context=ctx))
    }

    _constraints = [
    ]


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

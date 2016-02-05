# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp.osv import osv, fields

class partner_record(osv.osv):
    """Partner Record"""
    
    _inherit = 'nautical.partner_record'

    _columns = {
    }

    _defaults = {
        'user_id': lambda s, cr, u, c: u,
        'date': lambda self, cr, uid, ctx: ctx.get('date', fields.date.context_today(self,cr,uid,context=ctx))
    }

    _constraints = [
    ]


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

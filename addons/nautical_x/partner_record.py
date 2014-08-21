# -*- coding: utf-8 -*-
##############################################################################
#
#    Nautical
#    Copyright (C) 2013 Sistemas ADHOC
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import re
from openerp import netsvc
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

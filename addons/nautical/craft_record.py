# -*- coding: utf-8 -*-
##############################################################################
#
#    Nautical
#    Copyright (C) 2014 Sistemas ADHOC
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

class craft_record(osv.osv):
    """Craft Record"""
    
    _name = 'nautical.craft_record'
    _description = 'Craft Record'

    _columns = {
        'date': fields.datetime(string='Date', required=True),
        'user_id': fields.many2one('res.users', string='User', required=True),
        'requestor_id': fields.many2one('res.partner', string='Requestor'),
        'type': fields.selection([(u'draft', u'Draft'), (u'to_dispatch', u'To Dispatch'), (u'sailing', u'Sailing'), (u'in_reparation', u'In Reparation'), (u'in_custody', u'In Custody'), (u'transitional_retirement', u'Transitional Retirement'), (u'expired', u'Expired'), (u'contracted', u'Contracted'), (u'stored', u'Stored'), (u'do_not_dispatch', u'Do not Dispatch'), (u'permanent_cancellation', u'Permanent Cancellation'), (u'other', u'Other')], string='Type', required=True),
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

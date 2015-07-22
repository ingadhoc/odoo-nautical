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

class contract(osv.osv):
    """Contract"""
    
    _name = 'nautical.contract'
    _description = 'Contract'

    _states_ = [
        # State machine: basic
        ('draft','Draft'),
        ('contracted','Contracted'),
        ('expired','Expired'),
        ('permanent_cancellation','Permanent Cancellation'),
    ]
    _columns = {
        'start_date': fields.date(string='Contract Date', required=True),
        'start_code': fields.char(string='Contract Number', required=True),
        'expiration_date': fields.date(string='Expiration Date'),
        'owner_id': fields.many2one('res.partner', string='Owner', readonly=True, required=True),
        'end_date': fields.date(string='Cancellation Date'),
        'end_code': fields.char(string='Cancellation Number'),
        'cancellation_note': fields.text(string='Cancellation Notes'),
        'state': fields.selection(_states_, "State"),
        'craft_id': fields.many2one('nautical.craft', string='craft_id', ondelete='cascade', required=True), 
    }

    _defaults = {
        'state': 'draft',
    }

    _order = "id desc"

    _constraints = [
    ]


    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'nautical.contract', obj_id, cr)
            wf_service.trg_create(uid, 'nautical.contract', obj_id, cr)
        return True



contract()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

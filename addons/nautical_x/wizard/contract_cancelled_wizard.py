# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from osv import fields, osv
from tools.translate import _
from openerp import netsvc

class contract_cancelled_wizard(osv.osv_memory):
    _name = 'contract_cancelled_wizard'
    _description = 'Wizard to cancel contract'

    _columns = {
        'end_date': fields.date(string='Cancellation Date', required=True),
        'end_code': fields.char(string='Cancellation Number', required=True),
        'cancellation_note': fields.text(string='Cancellation Notes'),
    }
    

    _defaults = {
    }
            
    def contract_cancelled_wizard(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        active_id = context.get('active_id', False)
        contract_obj = self.pool.get('nautical.contract')
        craft_obj = self.pool.get('nautical.craft')
        craft = craft_obj.browse(cr, uid, [active_id])[0]
        contract_id = contract_obj.search(cr, uid, [], order='id desc', context=context)[0]
        wf_service = netsvc.LocalService("workflow")
        if active_id:
            end_date = wizard.end_date
            end_code = wizard.end_code            
            cancellation_note = wizard.cancellation_note            
            contract_vals = {'end_date': end_date, 'end_code': end_code, 'cancellation_note': cancellation_note,}
            print contract_vals
            print contract_id
            contract_obj.write(cr, uid, contract_id, contract_vals, context=context)
            wf_service.trg_validate(uid, 'nautical.contract', contract_id, 'sgn_contract_cancelled', cr)
            
            # # Empty locations 
            craft_obj.write(cr, uid, active_id, {'location_ids': [(5, 0)]}, context=context)
            
            # # Move craft WF
            wf_service.trg_validate(uid, 'nautical.craft', active_id, 'sgn_contract_cancelled', cr)
        
        return True
# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


from openerp.osv import fields, osv
from openerp import _


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
        contract_id = contract_obj.search(
            cr, uid, [('craft_id', '=', active_id), ('state', '=', 'contracted')],
            order='id desc',
            context=context)[0]
        if active_id:
            end_date = wizard.end_date
            end_code = wizard.end_code
            cancellation_note = wizard.cancellation_note
            contract_vals = {'end_date': end_date, 'end_code': end_code,
                             'cancellation_note': cancellation_note, 'state': 'permanent_cancellation'}
            contract_obj.write(
                cr, uid, contract_id, contract_vals, context=context)
            # Empty locations
            craft_obj.write(cr, uid, active_id, {
                            'location_ids': [(5, 0)], 'state': 'permanent_cancellation'}, context=context)


        return True

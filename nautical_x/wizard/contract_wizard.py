# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


from openerp.osv import fields, osv
from openerp import _


class create_contract(osv.osv_memory):
    _name = 'create_contract'
    _description = 'Wizard to create contract'
    _rec_name = 'start_date'

    _columns = {
        'start_date': fields.date(string='Contract Date', required=True),
        'start_code': fields.char(string='Contract Number', required=True),
        'expiration_date': fields.date(string='Expiration Date'),
    }

    _defaults = {
    }

    def create_contract(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        active_id = context.get('active_id', False)
        contract_obj = self.pool.get('nautical.contract')
        craft_obj = self.pool.get('nautical.craft')
        craft = craft_obj.browse(cr, uid, [active_id])[0]
        if active_id:
            start_date = wizard.start_date
            start_code = wizard.start_code
            expiration_date = wizard.expiration_date
            new_contract_vals = {'start_date': start_date, 'start_code': start_code, 'expiration_date':
                                 expiration_date, 'owner_id': craft.owner_id.id, 'craft_id': craft.id, 'state': 'contracted'}
            contract_obj.create(
                cr, uid, new_contract_vals, context=context)
            craft_obj.write(
                cr, uid, craft.id, {'state': 'contracted'}, context=context)

        return True

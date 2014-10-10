# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from openerp import _
from openerp import netsvc

class create_contract(osv.osv):
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
        wf_service = netsvc.LocalService("workflow")
        print craft.owner_id.id
        if active_id:
            start_date = wizard.start_date
            start_code = wizard.start_code
            expiration_date = wizard.expiration_date
            new_contract_vals = {'start_date': start_date, 'start_code': start_code, 'expiration_date': expiration_date, 'owner_id':craft.owner_id.id,'craft_id': craft.id, 'state':'contracted'}
            new_contract_id = contract_obj.create(cr, uid, new_contract_vals, context=context)
            wf_service.trg_validate(uid, 'nautical.contract', new_contract_id, 'sgn_contract_signed', cr)            
            wf_service.trg_validate(uid, 'nautical.craft', active_id, 'sgn_contract_signed', cr)
        
        return True
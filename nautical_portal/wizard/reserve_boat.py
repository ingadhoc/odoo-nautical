# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from openerp import netsvc
from openerp import _
from datetime import datetime, date

class craft_reserve(osv.osv_memory):
    _name = 'nautical_portal.reserve_boat'
    _description = 'Wizard to reserve craft'
    _rec_name = 'destiny'

    _columns = {
        'estimated_dep_date': fields.datetime(string='Estimated Departure Date', required=True),
        'destiny': fields.char(string='Destiny'),
        'crew_qty': fields.integer(string='Crew'),
        'est_arrival_date': fields.datetime(string='Estimated Arrival Date'),
        
    }
    

    _defaults = {
    'estimated_dep_date': lambda *a: fields.datetime.now(),
        
    }
            
    def reserve(self, cr, uid, ids, context=None):
        context = context or {}
        active_id = context.get('active_id', False)
        craft_obj = self.pool.get('nautical.craft')
        wizard = self.browse(cr, uid, ids, context=context)[0]
        user = self.pool['res.users'].browse(cr,uid,uid)
        craft_id = craft_obj.browse(cr, uid, [active_id])[0]
        role_obj=self.pool['nautical.role_book']
        
        vals = {
                'estimated_dep_date': wizard.estimated_dep_date,
                'partner_id': user.partner_id.id,
                'craft_id':craft_id.id,
                'destiny': wizard.destiny,
                'crew_qty':wizard.crew_qty,
                'est_arrival_date':wizard.est_arrival_date,
            }

        craft_obj.craft_request(cr, 1, [craft_id.id], 'sail', user.partner_id.id, context=None)
        print vals
        role_obj.create(cr, uid, vals, context=context)


       
            


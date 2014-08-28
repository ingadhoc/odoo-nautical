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
from datetime import datetime, date

class craft_reserve(osv.osv_memory):
    _name = 'nautical_portal.reserve_boat'
    _description = 'Wizard to reserve craft'

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
        partner_id = self.pool['res.users'].browse(cr,uid,uid,context)
        craft_id = craft_obj.browse(cr, uid, [active_id])[0]
        role_obj=self.pool['nautical.role_book']
        print wizard
        
        vals = {
                'estimated_dep_date': wizard.estimated_dep_date,
                'partner_id': partner_id.id,
                'craft_id':craft_id.id,
                'destiny': wizard.destiny,
                'crew_qty':wizard.crew_qty,
                'est_arrival_date':wizard.est_arrival_date,
            }
        print vals

        craft_obj.craft_request(cr, 1, [craft_id.id], 'sail', partner_id.id, context=None)
        role_obj.create(cr, uid, vals, context=context)


       
            


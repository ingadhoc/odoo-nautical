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

class craft(osv.osv):
    """Craft"""
    
    _name = 'nautical.craft'
    _description = 'Craft'
    _inherits = {  }
    _inherit = [ 'mail.thread' ]

    _states_ = [
        # State machine: basic
        ('draft','Draft'),
        ('to_dispatch','To Dispatch'),
        ('sailing','Sailing'),
        ('in_reparation','In Reparation'),
        ('in_custody','In Custody'),
        ('transitional_retirement','Transitional Retirement'),
        ('expired','Expired'),
        ('contracted','Contracted'),
        ('stored','Stored'),
        ('check_due','Check Due'),
        ('do_not_dispatch','Do not Dispatch'),
        ('permanent_cancellation','Permanent Cancellation'),
    ]
    _track = {
        'state': {
            'nautical.craft_draft': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'draft',
            'nautical.craft_to_dispatch': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'to_dispatch',
            'nautical.craft_sailing': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'sailing',
            'nautical.craft_in_reparation': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'in_reparation',
            'nautical.craft_in_custody': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'in_custody',
            'nautical.craft_transitional_retirement': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'transitional_retirement',
            'nautical.craft_expired': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'expired',
            'nautical.craft_contracted': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'contracted',
            'nautical.craft_stored': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'stored',
            'nautical.craft_check_due': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'check_due',
            'nautical.craft_do_not_dispatch': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'do_not_dispatch',
            'nautical.craft_permanent_cancellation': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'permanent_cancellation',
        },
    }
    _columns = {
        'ref': fields.char(string='Internal Reference', readonly=True),
        'product_id': fields.many2one('product.product', string='Product', required=True, context={'default_type':'storage_service'}, domain=[('type','=','storage_service')]),
        'plate': fields.char(string='Plate'),
        'name': fields.char(string='Name'),
        'measures_uom_id': fields.many2one('product.uom', string='Measures UOM'),
        'lenght': fields.char(string='Lenght'),
        'breadth': fields.char(string='Breadth'),
        'draught': fields.char(string='Draught'),
        'prop': fields.char(string='Prop'),
        'displacement': fields.char(string='Displacement'),
        'displacement_uom_id': fields.many2one('product.uom', string='Displacement UOM'),
        'material_id': fields.many2one('nautical.craft_material', string='Material'),
        'engine_brand_id': fields.many2one('nautical.engine_brand', string='Engine Brand'),
        'engine_power': fields.char(string='Engine Power'),
        'engine_power_uom_id': fields.many2one('product.uom', string='Engine Power UOM'),
        'engine_serial_number': fields.char(string='Engine Serial Number'),
        'aux_engine_brand_id': fields.many2one('nautical.engine_brand', string='Aux. Engine Brand'),
        'aux_engine_power': fields.char(string='Aux. Engine Power'),
        'aux_engine_power_uom_id': fields.many2one('product.uom', string='Aux. Engine Power UOM'),
        'aux_engine_serial_number': fields.char(string='Aux. Engine Serial Number'),
        'note': fields.text(string='Note'),
        'craft_type': fields.char(string='Craft Type'),
        'last_action_date': fields.datetime(string='Last Action Date', readonly=True),
        'brand_id': fields.many2one('nautical.craft_brand', string='Brand'),
        'shipyard_id': fields.many2one('nautical.shipyard', string='Shipyard'),
        'aux_requestor_id': fields.many2one('res.partner', string='Aux. Requestor'),
        'state': fields.selection(_states_, "State"),
        'location_ids': fields.one2many('nautical.location', 'craft_id', string='Location', states={'draft':[('readonly', True)],'permanent_cancellation':[('readonly', True)]}, context={'default_type':'normal'}, domain=[('type','=','normal')]), 
        'authorization_ids': fields.one2many('nautical.authorization', 'craft_id', string='Authorizations'), 
        'owner_id': fields.many2one('res.partner', string='Owner', readonly=True, states={'draft':[('readonly', False)]}, domain=[('customer','=',True)], ondelete='cascade', required=True), 
        'service_authorization_ids': fields.one2many('nautical.service_authorization', 'craft_id', string='Service Authorizations'), 
        'contract_ids': fields.one2many('nautical.contract', 'craft_id', string='Contracts'), 
        'craft_record_ids': fields.one2many('nautical.craft_record', 'craft_id', string='Record', context={'from_craft':True}), 
    }

    _defaults = {
        'state': 'draft',
    }

    _order = "ref"

    _constraints = [
    ]


    def onchange_product(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'nautical.craft', obj_id, cr)
            wf_service.trg_create(uid, 'nautical.craft', obj_id, cr)
        return True



craft()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

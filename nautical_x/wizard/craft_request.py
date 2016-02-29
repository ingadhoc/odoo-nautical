# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp.osv import fields, osv
from openerp import _
from datetime import datetime, date


class craft_request(osv.osv_memory):
    _name = 'craft_request'
    _description = 'Wizard to cancel contract'

    def onchange_request_type(self, cr, uid, ids, request_type, context=None):
        context = context or {}
        craft_id = context.get('craft_id', False)
        domain = [('craft_id', '=', craft_id)]
        if request_type == 'sail':
            domain.append(('authorization_type_id.can_sail', '=', True))
        elif request_type == 'in_reparation':
            domain.append(
                ('expiration_date', '>=', date.today().strftime('%Y-%m-%d')))

        result = {}
        result['domain'] = {}
        result['domain'].update({
            'requestor_id': domain,
            'service_requestor_id': domain,
        })
        return result

    _columns = {
        'requestor_type': fields.selection([('owner', 'Owner'), ('authorized', 'Authorized')], string='Type', required=True),
        'requestor_id': fields.many2one('nautical.authorization', string='Requestor',),
        'service_requestor_id': fields.many2one('nautical.service_authorization', string='Requestor',),
        'custody_requestor_id': fields.many2one('res.partner', string='Requestor',),
        'request_type': fields.char(string='Request Type', required=True),
    }

    _defaults = {
        'requestor_type': 'owner',
    }

    # def craft_request(self, cr, uid, ids, context=None):
    #     context = context or {}
    #     wizard = self.browse(cr, uid, ids)[0]
    #     active_id = context.get('active_id', False)
    #     craft_obj = self.pool.get('nautical.craft')
    #     authorization_obj = self.pool.get('nautical.authorization')
    #     craft_id = craft_obj.browse(cr, uid, [active_id])[0]
    #     wf_service = netsvc.LocalService("workflow")
    #     if active_id:
    #         requestor_type = wizard.requestor_type
    #         if requestor_type == 'owner':
    #             partner_id = craft_id.owner_id.id
    #         else:
    #             partner_id = wizard.requestor_id.partner_id.id

    #         if wizard.request_type== 'in_reparation':
    #             partner_id = wizard.service_requestor_id.supplier_id.id

    #         if wizard.request_type== 'in_custody':
    #             partner_id = wizard.custody_requestor_id.id

    #         craft_obj.write(cr, uid, [craft_id.id], {'aux_requestor_id':partner_id}, context)

    #         if wizard.request_type == 'sail':
    #             wf_service.trg_validate(uid, 'nautical.craft', active_id, 'sgn_requested', cr)
    #         elif wizard.request_type== 'transitional_retirement':
    #             wf_service.trg_validate(uid, 'nautical.craft', active_id, 'sgn_to_transitional_retirement', cr)
    #         elif wizard.request_type== 'in_reparation':
    #             wf_service.trg_validate(uid, 'nautical.craft', active_id, 'sgn_to_reparation', cr)
    #         elif wizard.request_type== 'in_custody':
    #             wf_service.trg_validate(uid, 'nautical.craft', active_id, 'sgn_to_custody', cr)
    #     return True

    def craft_request(self, cr, uid, ids, context=None):
        context = context or {}
        wizard = self.browse(cr, uid, ids)[0]
        active_id = context.get('active_id', False)
        craft_obj = self.pool.get('nautical.craft')
        craft_id = craft_obj.browse(cr, uid, [active_id])[0]
        if active_id:
            requestor_type = wizard.requestor_type
            if requestor_type == 'owner':
                partner_id = craft_id.owner_id.id
            else:
                partner_id = wizard.requestor_id.partner_id.id

            if wizard.request_type == 'in_reparation':
                partner_id = wizard.service_requestor_id.supplier_id.id

            if wizard.request_type == 'in_custody':
                partner_id = wizard.custody_requestor_id.id

            craft_obj.craft_request(
                cr, uid, [craft_id.id], wizard.request_type, partner_id, context)
        return True

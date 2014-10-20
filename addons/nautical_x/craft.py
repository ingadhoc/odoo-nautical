# -*- coding: utf-8 -*-
##############################################################################
#
#    Nautical
#    Copyright (C) 2013 Sistemas ADHOC
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

import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import fields as fields_new
from openerp import models, api
from openerp import tools, netsvc
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class craft(models.Model):
# class craft(osv.osv):
    """Craft"""

    _inherit = 'nautical.craft'

    @api.one
    @api.depends('role_book_ids.estimated_dep_date','role_book_ids.est_arrival_date','role_book_ids')
    def _cal_role(self):
        role_books = self.env['nautical.role_book'].search([('craft_id','=',self.id)], order='estimated_dep_date desc')
        if role_books:
            self.role_book_id = role_books[0]
            self.estimated_dep_date = role_books[0].estimated_dep_date
            self.est_arrival_date = role_books[0].est_arrival_date
        else:
            self.role_book_id = False    

    role_book_id = fields_new.Many2one(
        'nautical.role_book',
        string='Role book',
        compute='_cal_role',
        store=True
    )

    estimated_dep_date = fields_new.Datetime(
        # related='role_book_id.estimated_dep_date',
        compute='_cal_role',
        string='Estimated Departure Date',
        store=True
    )

    est_arrival_date = fields_new.Datetime(
        compute='_cal_role',
        # related='role_book_id.est_arrival_date',
        string='Estimated Arrival Date',
        store=True
    )


    def name_get(self, cr, uid, ids, context=None):
        # always return the full hierarchical name
        res = {}
        for line in self.browse(cr, uid, ids):
            if line.name and line.owner_id.name:
                sep = ' - '
            else:
                sep = ''
            res[line.id] = (line.name or '')+ sep + line.owner_id.name
        return res.items()

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        ids = set()
        if name:
            ids.update(self.search(cr, user, args + [('name',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
            if not limit or len(ids) < limit:
                ids.update(self.search(cr, user, args + [('owner_id.name',operator,name)], limit=limit, context=context))
            ids = list(ids)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'price_unit': 0.0,
            }

            # Get price
            price_unit = self.pool.get('product.pricelist').price_get(cr, uid, [record.pricelist_id.id],
                    record.product_id.id, 1.0, record.owner_id.id, {
                        'uom': record.product_id.uom_id.id,
                        # 'uom': result.get('product_uom'),
                        'date': date_order,
                        })[record.pricelist_id.id]
            # [record.pricelist_id.id]


            val = 0.0
            cur = record.owner_id.property_product_pricelist.currency_id
            # res[record.id]['price_unit'] = 0.0
            res[record.id]['price_unit'] = cur_obj.round(cr, uid, cur, price_unit)
            price = price_unit * (1 - (record.discount or 0.0) / 100.0)
            # price = record.price_unit * (1 - (record.discount or 0.0) / 100.0)
            # price = 0.0
            taxes = tax_obj.compute_all(cr, uid, record.tax_id, price, 1, record.product_id, record.owner_id)
            res[record.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, price)
            for c in taxes['taxes']:
                val += c.get('amount', 0.0)
            res[record.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[record.id]['amount_total'] = cur_obj.round(cr, uid, cur, taxes['total_included'])
        return res

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _get_location_string(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            loc_name = ''
            for location in obj.location_ids:
                loc_name += location.complete_ref + ', '
            result[obj.id] = loc_name
        return result

    # def _cal_role(self, cr, uid, ids, name, args, context=None):
    #     result = {}
    #     role_obj=self.pool['nautical.role_book']
    #     for craft in self.browse(cr, uid, ids, context=context):
    #         role_book_id = False
    #         role_book_ids = role_obj.search(cr, uid, [('craft_id','=',craft.id)], order='estimated_dep_date desc', context=context)
    #         if role_book_ids:
    #             role_book_id = role_book_ids[0]
    #         result[craft.id] = role_book_id
    #     return result


    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    _columns = {
# Images
        'image': fields.binary("Image",
            help="This field holds the image used as image for the craft, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'nautical.craft': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of the craft. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved, "\
                 "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'nautical.craft': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of the craft. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
# Others
        'craft_type': fields.related('product_id', 'craft_type', type='char', string='Craft Type Code',),
        'partner_payment_earliest_due_date': fields.related('owner_id', 'payment_earliest_due_date', type='char', string='Worst Due Date',),
        'locations_string': fields.function(_get_location_string, string='Locations', type='char'),
# TODO. Could be good to add states restricion "readonly=True, states={'draft': [('readonly', False)]}"" to all this fields
        'account_invoice_line_ids': fields.one2many('account.invoice.line', 'craft_id', string='Account Invoice Lines', readonly=True),
        'price_unit': fields.function(_amount_all, string='Price', digits_compute= dp.get_precision('Product Price'), multi='sums'),
        'amount_untaxed': fields.function(_amount_all, string='Untaxed Amount', digits_compute= dp.get_precision('Account'), multi='sums'),
        'amount_tax': fields.function(_amount_all, string='Taxes', digits_compute= dp.get_precision('Account'), multi='sums'),
        'amount_total': fields.function(_amount_all, string='Total', digits_compute= dp.get_precision('Account'), multi='sums'),
        'discount': fields.float('Discount (%)', digits_compute= dp.get_precision('Discount'),),
        'tax_id': fields.many2many('account.tax', 'craft_tax_rel', 'craft_id', 'tax_id', 'Taxes',),
        'pricelist_id': fields.related('owner_id', 'property_product_pricelist', type='many2one', relation='product.pricelist', string='Pricelist'),
        'fiscal_position': fields.related('owner_id', 'property_account_position', type='many2one', relation='account.fiscal.position', string='Fiscal Position'),
        'currency_id': fields.related('pricelist_id', 'currency_id', type="many2one", relation="res.currency", string="Currency", readonly=True, required=False),
# ADDED TRACKING
        # El tracking en locations, por ser m2m, registra los ids y eso no esta bueno
        # 'location_ids': fields.one2many('nautical.location', 'craft_id', string='Location', states={'draft':[('readonly', True)],'permanent_cancellation':[('readonly', True)]}, context={'default_type':'normal'}, domain=[('type','=','normal')], track_visibility='onchange'),
        'owner_id': fields.many2one('res.partner', string='Owner', readonly=True, states={'draft':[('readonly', False)]}, ondelete='cascade', required=True, track_visibility='onchange'),
    }

    _defaults = {
    }

    # _order = 'estimated_dep_date, est_arrival_date, id'

    def create(self, cr, uid, vals, context=None):
        if vals.get('ref','/')=='/':
            vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'craft_reference') or '/'
        return super(craft, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        # print ('context', context)
        if 'state' in vals:
            # self.wkf_preconditions(cr, uid, ids, vals, context=context)
            if vals['state'] not in 'check_due':
                self.create_craft_record(cr, uid, ids, vals, context=context)

            vals['last_action_date'] = datetime.now()

        ret = super(craft, self).write(cr, uid, ids, vals, context=context)
        return ret

    #TODO mover este metodo a el modulo nautical_portal
    def action_reserver(self, cr, uid, ids, context=None):
        reserve_obj = self.pool['nautical_portal.reserve_boat']
        if self.test_partner_dispatch(cr, 1, ids):
            reserve_obj.reserve(cr, uid, ids, context=None)
        else:
            raise osv.except_osv(_('Error!'),
                        _('Member  does not have the fee per day.') )

            return True

    def craft_request(self, cr, uid, ids, request_type, partner_id, context=None):
        wf_service = netsvc.LocalService("workflow")
        if request_type == 'sail':
            signal = 'sgn_requested'
        elif request_type== 'transitional_retirement':
            signal = 'sgn_to_transitional_retirement'
        elif request_type== 'in_reparation':
            signal = 'sgn_to_reparation'
        elif request_type== 'in_custody':
            signal = 'sgn_to_custody'
        self.write(cr, uid, ids, {'aux_requestor_id':partner_id}, context)
        for craft_id in ids:
            wf_service.trg_validate(uid, 'nautical.craft', craft_id, signal, cr)

    def create_craft_record(self, cr, uid, ids, vals, context=None):
        craft_record_obj = self.pool.get('nautical.craft_record')
        context = context or {}
        # requestor_id = context.get('requestor_id', False)

        for craft in self.browse(cr, uid, ids, context):
            record_vals = {
                'craft_id': craft.id,
                # 'date': ,
                # 'user_id': ,
                'requestor_id': craft.aux_requestor_id.id,
                'type': vals['state'] or '',
            }
            craft_record_obj.create(cr, uid, record_vals, context=context)
        self.write(cr, uid, ids, {'aux_requestor_id':False}, context)


    def wkf_preconditions(self, cr, uid, ids, vals, context=None):
        if 'state' not in vals:
            return
        # if vals['state'] == 'contracted':
        #     self.check_contract_permanent_cancellation(cr, uid, ids, context=context)


    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        if not part:
            return {'value': {'pricelist_id': False, 'fiscal_position': False,}}

        part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
        # payment_term = part.property_payment_term and part.property_payment_term.id or False
        fiscal_position = part.property_account_position and part.property_account_position.id or False
        val = {
            # 'payment_term': payment_term,
            'fiscal_position': fiscal_position,
        }
        if pricelist:
            val['pricelist_id'] = pricelist
        return {'value': val}


    def product_id_change(self, cr, uid, ids, pricelist, product_id, partner_id=False, update_tax=True, fiscal_position=False, context=None):
        # Partner would be the owner
        if not  partner_id:
            raise osv.except_osv(_('No Owner Defined!'), _('Before choosing a product,\n select an owner.'))
        context = context or {}
        warning = {}
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'partner_id': partner_id}
        warning_msgs = ''
        result = {}
        domain = {}

        if product_id:
            product_obj = product_obj.browse(cr, uid, product_id, context=context)

            fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
            if update_tax: #The quantity only have changed
                result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)
            result['product_uom'] = product_obj.uom_id.id
            result['craft_type'] = product_obj.craft_type
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
            if not pricelist:
                warn_msg = _('You have to select an owner!\n'
                        'Please set one before choosing a product.')
                warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
            else:
                price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                        product_id, 1.0, partner_id, {
                            'uom': result.get('product_uom'),
                            'date': date_order,
                            })[pricelist]
                if price is False:
                    warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
                            "You have to change either the product, the quantity or the pricelist.")

                    warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
                else:
                    result.update({'price_unit': price})

            if warning_msgs:
                warning = {
                           'title': _('Configuration Error!'),
                           'message' : warning_msgs
                        }
        else:
            result['product_uom'] = False
            result['craft_type'] = False
            result['price_unit'] = False
            result['tax_id'] = False

        return {'value': result, 'domain': domain, 'warning': warning}


    def button_dummy(self, cr, uid, ids, context=None):
        return True

    def test_partner_dispatch(self, cr, uid, ids, *args):
        user_obj=self.pool['res.users']
        company_obj = self.pool['res.company']
        craft = self.browse(cr, uid, ids, context=None)[0]

        company_ids = user_obj.search(cr, uid, [('company_id','=',craft.owner_id.company_id.id)], context=None)
        company_id=company_obj.browse(cr, uid, company_ids, context=None)[0]
        months_debt=company_id.debt_limit_months

        # Test if partner due date is highter than 2 months. If not, return true so he can dispatch. Else, return False
        if months_debt == 0 or not months_debt:
            return True
        else:
            tolerance_date = (datetime.today() + relativedelta(months=-months_debt)).strftime('%Y-%m-%d')
            for record in self.browse(cr, uid, ids, context={}):
                if not record.owner_id.payment_earliest_due_date or record.owner_id.payment_earliest_due_date >= tolerance_date:
                    return True
                else:
                    return False


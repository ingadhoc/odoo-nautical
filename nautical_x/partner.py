# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

import re
from openerp import netsvc
from openerp.osv import osv, fields
from openerp import fields as new_fields
from openerp import api
from datetime import datetime, date, timedelta
from openerp import _
from dateutil.relativedelta import relativedelta
import time
from openerp.addons.decimal_precision import decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import logging
_logger = logging.getLogger(__name__)


class res_partner_invoice_line(osv.osv):
    _name = "res.partner.invoice.line"

    def _amount_line(self, cr, uid, ids, prop, unknow_none, unknow_dict, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.quantity * line.price_unit
            # if line.analytic_account_id.pricelist_id:
                # cur = line.analytic_account_id.pricelist_id.currency_id
                # res[line.id] = self.pool.get('res.currency').round(cr, uid, cur, res[line.id])
        return res

    _columns = {
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'partner_id': fields.many2one('res.partner', 'Partner'),
        'name': fields.text('Description', required=True),
        'quantity': fields.float('Quantity', required=True),
        'uom_id': fields.many2one('product.uom', 'Unit of Measure', required=True),
        'price_unit': fields.float('Unit Price', required=True),
        'price_subtotal': fields.function(_amount_line, string='Sub Total', type="float", digits_compute=dp.get_precision('Account')),
    }
    _defaults = {
        'quantity': 1,
    }

    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, partner_id=False, price_unit=False, pricelist_id=False, context=None):
        context = context or {}
        uom_obj = self.pool.get('product.uom')
        # company_id = company_id or False
        local_context = dict(context, pricelist=1)
        if not product:
            return {'value': {'price_unit': 0.0}, 'domain': {'product_uom': []}}
        # if partner_id:
            # part = self.pool.get('res.partner').browse(cr, uid, partner_id, context=local_context)
            # if part.lang:
                # local_context.update({'lang': part.lang})

        result = {}
        res = self.pool.get('product.product').browse(
            cr, uid, product, context=local_context)
        price = False
        name = False
        if price_unit is not False:
            price = res.price
        if price is False:
            price = res.list_price
        if not name:
            name = self.pool.get('product.product').name_get(
                cr, uid, [res.id], context=context)[0][1]
            if res.description_sale:
                name += '\n' + res.description_sale
        result.update({'name': name or False, 'uom_id':
                       uom_id or res.uom_id.id or False, 'price_unit': price})

        res_final = {'value': result}
        if result['uom_id'] != res.uom_id.id:
            selected_uom = uom_obj.browse(
                cr, uid, result['uom_id'], context=context)
            new_price = uom_obj._compute_price(
                cr, uid, res.uom_id.id, res_final['value']['price_unit'], result['uom_id'])
            res_final['value']['price_unit'] = new_price
        return res_final

    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            defaults = self.product_id_change(
                vals.get('product_id'),
                vals.get('oum_id', False),
                context=None
            )['value']
        vals = dict(defaults, **vals)
        return super(res_partner_invoice_line, self).create(vals)


class social_category(osv.osv):

    """"""

    _name = 'nautical.social_category'

    name = new_fields.Char(string='Name')


class partner(osv.osv):

    """"""

    _inherit = 'res.partner'

    @api.one
    @api.depends(
        'document_number',
        # 'document_type_id',
        # 'document_type_id.name',
    )
    def _cal_number(self):
        self.social_number = self.document_number
        self.national_identity = self.document_number
        # lo dejamos por las dudas que al cliente no le guste que guardemos el cuit como si fuese un documento
        # if self.document_type_id.name == 'DNI':
        #     self.social_number = self.document_number
        #     self.national_identity = self.document_number
        # else:
        #     self.social_number = self.document_number
        #     self.national_identity = False

    national_identity = new_fields.Char(compute="_cal_number", store=True)
    social_number = new_fields.Char(compute="_cal_number",
                                    string='Social Number')
    document_number = new_fields.Char(required=True)
    social_category_id = new_fields.Many2one('nautical.social_category',
                                             string='Social Category')

    _columns = {
        # 'social_category': fields.selection([
        #     ('fees', 'Fees'),
        #     ('assets fees', 'Assets Fees'),
        #     ('lifetime', 'Lifetime'),
        #     ('active', 'Active'),
        #     ('cadet', 'Cadet'),
        #     ('minor', 'Minor'),
        #     ('retired and pensioners', 'Retired and pensioners'),
        #     ('transient', 'Transient'),
        #     ('adherents', 'Adherents'),
        #     ('sports', 'Sports'),
        #     ('absent', 'Absent'),
        #     ('students', 'Students')
        # ], string='Social Category'),
        'recurring_invoice_line_ids': fields.one2many('res.partner.invoice.line', 'partner_id', 'Partner', copy=True),
        # 'recurring_invoices' : fields.boolean('Generate recurring invoices automatically'),
        'recurring_rule_type': fields.selection([
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)'),
        ], 'Recurrency', help="Invoice automatically repeat at specified interval"),
        'recurring_interval': fields.integer('Repeat Every', help="Repeat every (Days/Week/Month/Year)"),
        'recurring_next_date': fields.date('Date of Next Invoice'),
    }

    _sql_constraints = [
        ('national_identity_uniq', 'unique(national_identity, company_id)',
         'National Identity must be unique per Company!'),
    ]

    _defaults = {
        'recurring_interval': 1,
        'recurring_next_date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def process_partner_invoices(self, cr, uid, ids=None, open_invoices=False, context=None):
        if context is None:
            context = {}
        if ids is None:
            ids = self.search(cr, uid, [], context=context)
        res = None
        context['date_invoice'] = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return self.create_invoices(cr, uid, ids, open_invoices, context)

    def _cron_recurring_create_invoice(self, cr, uid, ids=None, context=None):
        context = context or {}
        current_date = time.strftime('%Y-%m-%d')
        if ids:
            partner_ids = ids
        else:
            partner_ids = self.search(
                cr, uid, [('recurring_next_date', '<=', current_date), ('customer', '=', True)])
        return self.create_invoices(
            cr, uid, partner_ids, open_invoices=True,
            automatic=True, context=context)

    def create_invoices(
            self, cr, uid, ids, open_invoices=False,
            automatic=False, context=None):
        wf_service = netsvc.LocalService("workflow")
        current_date = time.strftime('%Y-%m-%d')
        inv_obj = self.pool.get('account.invoice')
        inv_ids = []
        for partner in self.browse(cr, uid, ids, context=context):
            active_craft_ids = self.pool['nautical.craft'].search(
                cr, uid,
                [('owner_id', '=', partner.id),
                 ('state', 'not in',  ['draft', 'permanent_cancellation'])],
                context=context)
            if not active_craft_ids and not partner.recurring_invoice_line_ids:
                _logger.info(
                    'Fail to create recurring invoice for partner %s, he does not have any activ craft or recurreing invoice line' % (partner.name))
                continue
            # We use the partner prepare invoice fucntion defined in account
            # intereset
            inv_values = self._prepare_invoice(
                cr, uid, partner, context=context)
            if inv_values:
                invoce_date = datetime.strptime(
                    partner.recurring_next_date, DEFAULT_SERVER_DATE_FORMAT)

                inv_values['comment'] = _(
                    'Cuota del Periodo ') + invoce_date.strftime('%m-%y')
                inv_values['date_invoice'] = partner.recurring_next_date
                inv_values['origin'] = inv_values['reference'] = _(
                    'Cuota. ') + invoce_date.strftime('%m-%y')
                try:
                    inv_id = inv_obj.create(
                        cr, uid, inv_values, context=context)
                    _logger.info('Invoice id: %i created' % (inv_id))
                except Exception, e:
                    _logger.warning(
                        "Unable to create invoice. This is what we get: %s" % e)
                    continue
                inv_ids.append(inv_id)

                # We create invoice lines for active crafts
                for craft in partner.owned_craft_ids:
                    if craft.state not in ['draft', 'permanent_cancellation']:
                        inv_lines_vals = self._prepare_invoice_line_craft(
                            cr, uid, partner, craft, inv_id, context=context)
                        if inv_lines_vals:
                            self.pool.get('account.invoice.line').create(
                                cr, uid, inv_lines_vals, context=context)

                # We create invoice lines for other products
                inv_lines_vals = self._prepare_invoice_line(
                    cr, uid, partner, inv_values['fiscal_position'], inv_id, context=None)
                for inv_line in inv_lines_vals:
                    if inv_line:
                        self.pool.get('account.invoice.line').create(
                            cr, uid, inv_line, context=context)

                inv_obj.button_reset_taxes(cr, uid, [inv_id], context=context)
                # wf_service.trg_write(uid, 'sale.order', sale_id, cr)
                if open_invoices:
                    wf_service.trg_validate(
                        uid, 'account.invoice', inv_id, 'invoice_open', cr)
                interval = partner.recurring_interval
                next_date = datetime.strptime(
                    partner.recurring_next_date or current_date, "%Y-%m-%d")
                if partner.recurring_rule_type == 'daily':
                    new_date = next_date + relativedelta(days=+interval)
                elif partner.recurring_rule_type == 'weekly':
                    new_date = next_date + relativedelta(weeks=+interval)
                elif partner.recurring_rule_type == 'monthly':
                    new_date = next_date + relativedelta(months=+interval)
                else:
                    new_date = next_date + relativedelta(years=+interval)
                self.write(cr, uid, [partner.id], {
                           'recurring_next_date': new_date.strftime('%Y-%m-%d')}, context=context)

                if automatic:
                    # auto-commit for batch processing
                    cr.commit()
        return inv_ids

    def _prepare_invoice_line(self, cr, uid, partner, fiscal_position_id, inv_id, context=None):
        fpos_obj = self.pool.get('account.fiscal.position')
        fiscal_position = None
        invoce_date = datetime.strptime(
            partner.recurring_next_date, DEFAULT_SERVER_DATE_FORMAT)
        if fiscal_position_id:
            fiscal_position = fpos_obj.browse(
                cr, uid,  fiscal_position_id, context=context)
        invoice_lines = []
        for line in partner.recurring_invoice_line_ids:

            res = line.product_id
            account_id = res.property_account_income.id
            if not account_id:
                account_id = res.categ_id.property_account_income_categ.id
            account_id = fpos_obj.map_account(
                cr, uid, fiscal_position, account_id)
            default_analytics = self.pool.get('account.analytic.default').account_get(
                cr, uid, line.product_id.id, partner.id, context=None)
            analytics_id = False
            if default_analytics:
                analytics_id = default_analytics.analytics_id.id

            taxes = res.taxes_id or False
            tax_id = fpos_obj.map_tax(cr, uid, fiscal_position, taxes)

            lines = {
                'name': line.name + ' - ' + _('. Period ') + invoce_date.strftime('%m-%y'),
                'account_id': account_id,
                'analytics_id': analytics_id,
                'price_unit': line.price_unit or 0.0,
                'quantity': line.quantity,
                'uos_id': line.uom_id.id or False,
                'product_id': line.product_id.id or False,
                'invoice_id': inv_id,
                'invoice_line_tax_id': [(6, 0, tax_id)],
            }
            invoice_lines.append(lines)
        return invoice_lines

    def _prepare_invoice_line_craft(self, cr, uid, partner, craft, inv_id, context=None):
        if context is None:
            context = {}

        invoce_date = datetime.strptime(
            partner.recurring_next_date, DEFAULT_SERVER_DATE_FORMAT)
        default_analytics = self.pool.get('account.analytic.default').account_get(
                cr, uid, craft.product_id.id, partner.id, context=None)
        analytics_id = False
        if default_analytics:
            analytics_id = default_analytics.analytics_id.id

        inv_line_values = {
            # TODO add tax, name origin and analitic account
            'name': craft.product_id.name + ' - ' + (craft.name or '') + _('. Period ') + invoce_date.strftime('%m-%y'),
            # 'origin': sale.name,
            # 'account_id': res['account_id'],
            'price_unit': craft.price_unit,
            'craft_id': craft.id,
            'quantity': 1.0,
            'discount': craft.discount or False,
            # 'uos_id': craft.product_uom.id or False,
            'product_id': craft.product_id.id or False,
            'invoice_id': inv_id,
            'invoice_line_tax_id': [(6, 0, [x.id for x in craft.tax_id])],
            # 'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
            'analytics_id': analytics_id,
            # 'invoice_line_tax_id': res.get('invoice_line_tax_id'),
            # 'account_analytic_id': sale.project_id.id or False,
        }
        return inv_line_values

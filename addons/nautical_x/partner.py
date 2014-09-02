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


import re
from openerp import netsvc
from openerp.osv import osv, fields
from datetime import datetime, date, timedelta
from openerp import _
from dateutil.relativedelta import relativedelta
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class partner(osv.osv):
    """"""
    
    _inherit = 'res.partner'

    _columns = {
    }

    _sql_constraints = [
        ('national_identity_uniq', 'unique(national_identity, company_id)', 'National Identity must be unique per Company!'),
    ]    


    def process_active_partner_invoices(self, cr, uid, ids=None, open_invoices=False, context=None):
        if context is None:
            context = {}
        if ids is None:
            ids = self.search(cr, uid, [], context=context)
        res = None
        context['date_invoice'] = time.strftime(DEFAULT_SERVER_DATE_FORMAT) 
        active_partner_ids = self.get_active_partner_ids(cr, uid, ids, context)
        # self.create_invoices(cr, uid, active_partner_ids, open_invoices, context)
        return self.create_invoices(cr, uid, active_partner_ids, open_invoices, context)
        # return res

    def get_active_partner_ids(self, cr, uid, ids, context=None):        
        active_partner_ids = []
        for record in self.browse(cr, uid, ids, context):
            for craft in record.owned_craft_ids:
                if craft.state not in ['draft', 'permanent_cancellation']:
                    print craft.state
                    active_partner_ids.append(record.id)
                    break
        return active_partner_ids

    def create_invoices(self, cr, uid, ids, open_invoices=False, context=None):
        """ create invoices for the active sales orders """

        wf_service = netsvc.LocalService("workflow")
        inv_obj = self.pool.get('account.invoice')
        inv_ids = []
        for partner in self.browse(cr, uid, ids, context=context):
            inv_values = self._prepare_invoice(cr, uid, partner, context=context)
            if inv_values:
                inv_values['comment'] =  _('Storage Service Period ') + time.strftime('%m-%y')
                inv_values['origin'] = inv_values['reference'] = _('Storage Serv. ') + time.strftime('%m-%y')
                inv_id = inv_obj.create(cr, uid, inv_values, context=context)
                inv_ids.append(inv_id)
                for craft in partner.owned_craft_ids:
                    if craft.state not in ['draft', 'permanent_cancellation']:
                        inv_lines_vals = self._prepare_invoice_line_craft(cr, uid, craft, inv_id, context=context)
                        if inv_lines_vals:
                            self.pool.get('account.invoice.line').create(cr, uid, inv_lines_vals, context=context)
                inv_obj.button_reset_taxes(cr, uid, [inv_id], context=context)
                # wf_service.trg_write(uid, 'sale.order', sale_id, cr)
                if open_invoices:
                    wf_service.trg_validate(uid, 'account.invoice', inv_id, 'invoice_open', cr)                            
        return inv_ids


# Usamos el de account_interest
#     def _prepare_invoice(self, cr, uid, partner, journal_id=None, context=None):
#         """Prepare the dict of values to create the new invoice for a
#            sales order. This method may be overridden to implement custom
#            invoice generation (making sure to call super() to establish
#            a clean extension chain).

#            :param browse_record order: sale.order record to invoice
#            :param list(int) line: list of invoice line IDs that must be
#                                   attached to the invoice
#            :return: dict of value to create() the invoice
#         """
#         if context is None:
#             context = {}
#         if journal_id is None:
#             journal_ids = self.pool.get('account.journal').search(cr, uid,
#                 [('type', '=', 'sale'), ('company_id', '=', partner.company_id.id)],
#                 limit=1)
#             if not journal_ids:
#                 raise osv.except_osv(_('Error!'),
#                     _('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
#             journal_id = journal_ids[0]
#         invoice_vals = {
#             # 'name': order.client_order_ref or '',
# # TODO agregar nombre
#             'name': '',
#             # 'origin': order.name,
# # TODO agregar origin
#             'origin': '',
#             'type': 'out_invoice',
# # TODO agregar reference
#             # 'reference': order.client_order_ref or order.name,
#             'reference': '',
#             'account_id': partner.property_account_receivable.id,
#             'partner_id': partner.id,
#             'journal_id': journal_id,
#             # 'invoice_line': [(6, 0, lines)],
#             'currency_id': partner.property_product_pricelist.currency_id.id,
# # TODO agregar comment
#             # 'comment': order.note,
#             # 'payment_term': partner.payment_term and order.payment_term.id or False,
#             'payment_term': partner.property_payment_term.id or False,
#             'fiscal_position': partner.property_account_position.id,
#             'date_invoice': context.get('date_invoice', False),
#             'company_id': partner.company_id.id,
#             'user_id': partner.user_id.id or False
#         }
#         return invoice_vals

    def _prepare_invoice_line_craft(self, cr, uid, craft, inv_id, context=None):
        if context is None:
            context = {}

        result = []

        inv_line_values = {
# TODO add tax, name origin and analitic account
            'name': craft.product_id.name + ' - ' + (craft.name or '') + _('. Period ') + time.strftime('%m-%y'),
            # 'origin': sale.name,
            # 'account_id': res['account_id'],
            'price_unit': craft.price_unit,
            'craft_id': craft.id,
            'quantity': 1.0,
            'discount': craft.discount or False,
            'uos_id': craft.product_uom.id or False,
            'product_id': craft.product_id.id or False,
            'invoice_id': inv_id,
            'invoice_line_tax_id': [(6, 0, [x.id for x in craft.tax_id])],
            # 'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
            # 'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
            # 'invoice_line_tax_id': res.get('invoice_line_tax_id'),
            # 'account_analytic_id': sale.project_id.id or False,
        }
        return inv_line_values

# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

import re
from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import SUPERUSER_ID, tools
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp import api


class contract(osv.osv):
    """Contract"""

    _inherit = 'nautical.contract'
    _rec_name = 'start_code'

    # def _data_get_start_file(self, cr, uid, ids, name, arg, context=None):
    #     if context is None:
    #         context = {}
    #     result = {}
    #     location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
    #     bin_size = context.get('bin_size')
    #     for attach in self.browse(cr, uid, ids, context=context):
    #         if location and attach.store_fname_start_file:
    #             result[attach.id] = self._file_read(cr, uid, location, attach.store_fname_start_file, bin_size)
    #         else:
    #             result[attach.id] = attach.start_file
    #     return result

    # def _data_set_start_file(self, cr, uid, id, name, value, arg, context=None):
    # We dont handle setting data to null
    #     if not value:
    #         return True
    #     if context is None:
    #         context = {}
    #     location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
    #     file_size = len(value.decode('base64'))
    #     if location:
    #         attach = self.browse(cr, uid, id, context=context)
    #         if attach.store_fname_start_file:
    #             self._file_delete(cr, uid, location, attach.store_fname_start_file)
    #         fname = self._file_write(cr, uid, location, value)
    # SUPERUSER_ID as probably don't have write access, trigger during create
    #         super(contract, self).write(cr, SUPERUSER_ID, [id], {'store_fname_start_file': fname, 'file_size_start_file': file_size}, context=context)
    #     else:
    #         super(contract, self).write(cr, SUPERUSER_ID, [id], {'start_file': value, 'file_size_start_file': file_size}, context=context)
    #     return True

    # def _data_get_end_file(self, cr, uid, ids, name, arg, context=None):
    #     if context is None:
    #         context = {}
    #     result = {}
    #     location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
    #     bin_size = context.get('bin_size')
    #     for attach in self.browse(cr, uid, ids, context=context):
    #         if location and attach.store_fname_end_file:
    #             result[attach.id] = self._file_read(cr, uid, location, attach.store_fname_end_file, bin_size)
    #         else:
    #             result[attach.id] = attach.end_file
    #     return result

    # def _data_set_end_file(self, cr, uid, id, name, value, arg, context=None):
    # We dont handle setting data to null
    #     if not value:
    #         return True
    #     if context is None:
    #         context = {}
    #     location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
    #     file_size = len(value.decode('base64'))
    #     if location:
    #         attach = self.browse(cr, uid, id, context=context)
    #         if attach.store_fname_end_file:
    #             self._file_delete(cr, uid, location, attach.store_fname_end_file)
    #         fname = self._file_write(cr, uid, location, value)
    # SUPERUSER_ID as probably don't have write access, trigger during create
    #         super(contract, self).write(cr, SUPERUSER_ID, [id], {'store_fname_end_file': fname, 'file_size_end_file': file_size}, context=context)
    #     else:
    #         super(contract, self).write(cr, SUPERUSER_ID, [id], {'end_file': value, 'file_size_end_file': file_size}, context=context)
    #     return True

    _columns = {
        # Fields for attachment
        # 'datas_start_file': fields.function(_data_get_start_file, fnct_inv=_data_set_start_file, string='Contract File', type="binary", nodrop=True),
        # 'file_size_start_file': fields.integer('File Size'),
        # 'store_fname_start_file': fields.char('Stored Filename', size=256),
        # 'datas_fname_start_file': fields.char('File Name',size=256),
        # 'datas_end_file': fields.function(_data_get_end_file, fnct_inv=_data_set_end_file, string='Cancellation File', type="binary", nodrop=True),
        # 'file_size_end_file': fields.integer('File Size'),
        # 'store_fname_end_file': fields.char('Stored Filename', size=256),
        # 'datas_fname_end_file': fields.char('File Name', size=256),
        'start_file': fields.many2many('ir.attachment', 'contract_start_file_rel', 'contract_id', 'attachment_id', 'Contract Files'),
        'end_file': fields.many2many('ir.attachment', 'contract_end_file_rel', 'contract_id', 'attachment_id', 'Cancellation Files'),
    }

    _constraints = [
    ]

    @api.one
    @api.constrains('state')
    def validate_contract_permanent_cancellation(self):
        if self.state == 'permanent_cancellation':
            if not self.end_date:
                raise osv.except_osv(_('End Date is Required.'),
                                     _('Cannot move to next stage, an End Date should be provided first.'))
            if not self.end_code:
                raise osv.except_osv(_('End Code is Required.'),
                                     _('Cannot move to next stage, an End Code should be provided first.'))


    def verify_contracts_validity(self, cr, uid, ids=None, context=None):
        if context is None:
            context = {}
        date = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        # wf_service = netsvc.LocalService("workflow")
        # ids = self.search(cr, uid, [('expiration_date','<=',date)])
        ids = self.search(
            cr, uid, [('state', 'in', ['contracted']), ('expiration_date', '<=', date)])
        for record in self.browse(cr, uid, ids, context):
            self.write(cr, uid, record.id, {'state': 'expired'})
            self.pool['nautical.craft'].write(
                cr, uid, record.craft_id.id, {'state': 'expired'})
        return True
        # return res

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order(osv.osv):
    _inherit = "sale.order"

    def proccess_manual_invoice(self, cr, uid, ids=None, context=None):
        if context is None:
            context = {}

        date_invoice = context.get('date_invoice', time.strftime(DEFAULT_SERVER_DATE_FORMAT) )

        ids = self.search(cr, uid, [('state','=', 'manual') ], context=context)
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        newinv = []
        if context is None:
            context = {}

        self.action_invoice_create(cr, uid, ids, grouped=True, date_invoice=date_invoice)

        for o in self.browse(cr, uid, ids, context=context):
            for i in o.invoice_ids:
                newinv.append(i.id)

        result = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        result['domain'] = "[('id','in', [" + ','.join(map(str, newinv)) + "])]"

        return result    
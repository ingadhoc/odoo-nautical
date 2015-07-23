# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
#######################################################T#######################

import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp import _
from openerp import tools, netsvc
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare


class craft(osv.osv):

    """Craft"""
    
    _inherit = 'nautical.craft'

    _columns = {}

  
    # TODO mover este metodo a el modulo nautical_portal
    def action_reserve(self, cr, uid, ids, context=None):
        reserve_obj = self.pool['nautical_portal.reserve_boat']
        if self.test_partner_dispatch(cr, 1, ids):
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'nautical_portal.reserve_boat',
            'view_mode': 'form',
            # 'res_id': craft_id.id,
            'target': 'new'
        }
        else:
            raise osv.except_osv(_('Error!'),
                        _('Member does not have the fee per day.') )

            return True

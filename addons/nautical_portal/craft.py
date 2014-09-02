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

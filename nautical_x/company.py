# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import re
from openerp import netsvc
from openerp.tools.translate import _
from openerp.osv import osv, fields



class company(osv.osv):
    """"""

    _name = 'res.company'
    _inherit = 'res.company'


    _columns = {

        'debt_limit_months': fields.integer(string='Debt limit Months')

    }

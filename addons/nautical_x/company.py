# -*- coding: utf-8 -*-
import re
from openerp import netsvc
from openerp.osv import osv, fields



class company(osv.osv):
    """"""

    _name = 'res.company'
    _inherit = 'res.company'


    _columns = {

        'debt_limit_months': fields.integer(string='Debt limit Months')

    }

# -*- coding: utf-8 -*-
##############################################################################
#
#    Nautical
#    Copyright (C) 2014 Sistemas ADHOC
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

class record_category(osv.osv):
    """Record Category"""
    
    _name = 'nautical.record_category'
    _description = 'Record Category'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'partner_record_id': fields.many2many('nautical.partner_record', 'nautical_categ_ids___rel', 'record_category_id', 'partner_record_id', string='&lt;no label&gt;'), 
    }

    _defaults = {
    }

    _order = "name"

    _constraints = [
    ]




record_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

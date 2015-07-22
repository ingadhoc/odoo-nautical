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

class partner_record(osv.osv):
    """Partner Record"""
    
    _name = 'nautical.partner_record'
    _description = 'Partner Record'

    _columns = {
        'date': fields.date(string='Date', required=True),
        'user_id': fields.many2one('res.users', string='User', required=True),
        'note': fields.text(string='Note', required=True),
        'partner_id': fields.many2one('res.partner', string='&lt;no label&gt;', ondelete='cascade'), 
        'categ_ids': fields.many2many('nautical.record_category', 'nautical_categ_ids___rel', 'partner_record_id', 'record_category_id', string='Tags', required=True), 
    }

    _defaults = {
    }

    _order = "date desc"

    _constraints = [
    ]




partner_record()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

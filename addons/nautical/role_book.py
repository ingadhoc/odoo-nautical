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

class role_book(osv.osv):
    """"""
    
    _name = 'nautical.role_book'
    _description = 'role_book'

    _columns = {
        'estimated_dep_date': fields.datetime(string='Estimated Departure Date', required=True),
        'partner_id': fields.many2one('res.partner', string='Partner', readonly=True, required=True),
        'destiny': fields.char(string='Destiny'),
        'crew_qty': fields.integer(string='Crew'),
        'est_arrival_date': fields.datetime(string='Estimated Arrival Date'),
        'craft_id': fields.many2one('nautical.craft', string='Craft', readonly=True, required=True, ondelete='cascade'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




role_book()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

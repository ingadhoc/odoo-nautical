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

class authorization(osv.osv):
    """Authorizations"""
    
    _name = 'nautical.authorization'
    _description = 'Authorizations'

    _columns = {
        'authorization_type_id': fields.many2one('nautical.authorization_type', string='Authorization Type', required=True),
        'partner_id': fields.many2one('res.partner', string='Partner', required=True), 
        'craft_id': fields.many2one('nautical.craft', string='Craft', required=True, ondelete='cascade'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




authorization()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

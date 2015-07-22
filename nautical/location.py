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

class location(osv.osv):
    """Location"""
    
    _name = 'nautical.location'
    _description = 'Location'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'ref': fields.char(string='Ref', required=True),
        'sufix': fields.char(string='Sufix'),
        'type': fields.selection([(u'normal', u'Normal'), (u'view', u'View')], string='Type', required=True),
        'craft_id': fields.many2one('nautical.craft', string='Craft', domain=[('state','not in',['permanent_cancellation', 'draft'])]), 
        'parent_id': fields.many2one('nautical.location', string='Parent Location', context={'default_type':'view','from_child':True}, domain=[('type','=', 'view')]), 
        'child_ids': fields.one2many('nautical.location', 'parent_id', string='Child Locations'), 
    }

    _defaults = {
    }

    _order = "name"

    _constraints = [
    ]




location()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

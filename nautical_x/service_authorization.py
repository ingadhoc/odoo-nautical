# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

import re
from openerp.osv import osv, fields

class service_authorization(osv.osv):
    """Service Authorization"""
    
    _inherit = 'nautical.service_authorization'

    def name_get(self, cr, uid, ids, context=None):
        # always return the full hierarchical name
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] = line.supplier_id.name + ' - ' + line.expiration_date         
        return res.items()     

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []    
        ids = set()     
        if name:
            ids.update(self.search(cr, user, args + [('supplier_id.name',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
            # if not limit or len(ids) < limit:
            #     ids.update(self.search(cr, user, args + [('craft_id.name',operator,name)], limit=limit, context=context))
            ids = list(ids)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result




service_authorization()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- coding: utf-8 -


import re
from openerp import netsvc
from openerp import SUPERUSER_ID, tools
from openerp.osv import osv, fields

class location(osv.osv):
    """Location"""
    

    _inherit = 'nautical.location'

# Puede ser interesante agregar un name_search tambien
    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','ref'], context=context)
        res = []
        for record in reads:
            name = '[' + record['ref'] + ']' + record['name'] 
            res.append((record['id'], name))
        return res    

# Esto es para borrar
    # def name_get_2(self, cr, uid, ids, context=None):
    #     if isinstance(ids, (list, tuple)) and not len(ids):
    #         return []
    #     if isinstance(ids, (long, int)):
    #         ids = [ids]
    #     reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
    #     res = []
    #     for record in reads:
    #         name = record['name']
    #         if record['parent_id']:
    #             name = record['parent_id'][1] +' / '+ name
    #         res.append((record['id'], name))
    #     return res

    # def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
    #     res = self.name_get_2(cr, uid, ids, context=context)
    #     return dict(res)

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from nautical_location where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

# Esto es para borrar
    # def ref_get(self, cr, uid, ids, context=None):
    #     if isinstance(ids, (list, tuple)) and not len(ids):
    #         return []
    #     if isinstance(ids, (long, int)):
    #         ids = [ids]
    #     # reads = self.read(cr, uid, ids, ['ref','parent_id'], context=context)
    #     # reads = self.browse(cr, uid, ids, context=context)
    #     res = []
    #     # for record in reads:
    #     for record in self.browse(cr, uid, ids, context=context):
    #         name = record.ref
    #         print ('name', name)
    #         # name = record['ref']
    #         # if record['parent_id']:
    #         sufix = ''
    #         if record.parent_id.complete_ref:
    #             print ('parent_id', record.parent_id)
    #             if record.parent_id.sufix:
    #                 sufix = record.parent_id.sufix
    #         	name = record.parent_id.complete_ref + sufix + name
    #             	# name = record['parent_id'][1]+' / '+name
    #         res.append((record['id'], name))
    #     return res


    # def _ref_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
    #     res = self.ref_get(cr, uid, ids, context=context)
    #     return dict(res)


    def get_childs(self, cr, uid, ids, context=None):
        ids2 = self.search(cr, uid, [('parent_id', 'child_of', ids)], context=context)            
        return ids2

    def _ref_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            record_name = record.ref
            
            record_it = record
            while record_it.parent_id:
                record_it = record_it.parent_id
                sufix = ''
                if record_it.parent_id.sufix:
                    sufix = record_it.parent_id.sufix
                record_name = record_it.ref + sufix + record_name
            res[record.id] = record_name
        return res 

    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            record_name = record.name
            
            record_it = record
            while record_it.parent_id:
                record_it = record_it.parent_id
                sufix = ''
                # if record_it.parent_id.sufix:
                #     sufix = record_it.parent_id.sufix
                record_name = record_it.name + ' / ' + record_name
            res[record.id] = record_name
        return res                  
     
    _columns = {
    	'complete_name': fields.function(_name_get_fnc, type="char", string='Complete Name',
                store={
                 'nautical.location': (get_childs, ['name'], 10),
                 }),
        'complete_ref': fields.function(_ref_get_fnc, type="char", string='Complete Ref', 
                store={
                 'nautical.location': (get_childs, ['ref'], 10),
                 }),
    }

    _constraints = [
        (_check_recursion, 'Error ! You cannot create recursive location.', ['parent_id'])
    ]
from openerp import netsvc
from openerp import models, fields, api
from openerp.tools.translate import _


class member_wizard(models.Model):
    """"""
    _name = 'nautical_member.wizard'
    _description = 'wizard'
    

    # @api.multi
    # def members_print(self):
        
    #     assert len(self) == 1
    #     partners = self.env['res.partner'].search([('active','=',True)])
    #     print 'partners', partners.ids
    #     a = self.env['report'].with_context(active_ids=partners.ids, active_id=partners.ids[0], active_model='res.partner')
    #     print 'a context', a._context
    #     return a.get_action(self, 'report_member_odt')

    def members_print(self, cr, uid, ids, context=None):
        # wizard = self.browse(cr, uid, ids, context=context)[0]
        partner_ids = self.pool['res.partner'].search(cr, uid, [('active','=',True)])
        context['active_ids'] = partner_ids
        # context['active_id'] = partner_ids{}
        context['active_model'] = 'res.partner'        
        return {'type' : 'ir.actions.report.xml',
                         'context' : context,
                         'report_name': 'report_member_odt'}        
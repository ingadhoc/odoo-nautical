# -*- coding: utf-8 -*-
##############################################################################
#
#    Saas Manager
#    Copyright (C) 2013 Sistemas ADHOC
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


{   'active': False,
    'author': u'Ingenieria ADHOC',
    'category': u'base.module_category_knowledge_management',
    'depends': [
      'nautical',
      'l10n_ar_states',
      # 'web_m2x_options',
      # 'account_interests',
      # OpenERP officla addons
      'procurement',
      'sale',
      'account_followup',  
        ],
    'description': """
Nautical Module Modifications
=============================

Projects required:
* lp:web-addons/8.0 --> web_nocreatedb, web_m2x_options
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Nautical Module Modifications',
    'test': [],
    'demo': [
      'data/demo/nautical.authorization_type.csv',
      'data/demo/nautical.location.csv',
      'data/demo/pricelist_data.xml',
      'data/demo/res.partner.csv',
      'data/demo/product.product.csv',
      'data/demo/nautical.craft.csv',
      'data/demo/nautical.authorization.csv',
    ],
    'data': [   
      'wizard/contract_wizard_view.xml',
      'wizard/contract_cancelled_wizard_view.xml',
      'wizard/craft_request_view.xml',
      'view/res_partner_view.xml',
      'view/partner_record_view.xml',
      'view/product_view.xml',
      'view/craft_view.xml',
      'view/craft_record_view.xml',
      'view/contract_view.xml',
      'view/location_view.xml',
      'view/account_invoice_view.xml',
      'view/company_view.xml',
      'view/res_partner_account_view.xml',
      'workflow/craft_workflow.xml',
      'data/sequences.xml',
      'data/cron.xml',
      'data/product_data.xml',
    ],
    'init_xml': [   

    ],    
    'version': u'1.1',
    'website': 'www.ingadhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

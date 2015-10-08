# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
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
{'active': False,
    'author': u'ADHOC SA',
    'category': u'base.module_category_knowledge_management',
    'depends': [
        'nautical_x',
        'report_aeroo',
        'l10n_ar_aeroo_base',
        'l10n_ar_aeroo_voucher',
    ],
    'description': """
Nautical Reports
================
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Nautical Reports',
    'test': [],
    'demo': [
    ],
    'data': [
        'report/transitional_retirement.xml',
        'report/contract_report.xml',
        'view/contract_view.xml',
        'report/cuota_report.xml',
        'report/recibo.xml',
        'report/member_report.xml',
        'report/auth_wizard.xml',
        'report/cancel_wizard.xml',
        'report/receipt_report.xml',
        'wizard/members_views.xml',
        'wizard/ab_wizard_view.xml',
    ],
    'init_xml': [

    ],
    'version': '8.0.1.1.0',
    'website': 'www.adhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

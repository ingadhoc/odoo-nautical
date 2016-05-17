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
{
    'name': 'Nautical Reports',
    'version': '8.0.1.4.0',
    'author': 'ADHOC SA',
    'license': 'AGPL-3',
    'category': 'base.module_category_knowledge_management',
    'website': 'www.adhoc.com.ar',
    'description': """
Nautical Reports
================
""",
    'test': [],
    'depends': [
        'nautical_x',
        'report_aeroo',
        'l10n_ar_aeroo_base',
        'l10n_ar_aeroo_voucher',
        'login_serial',
    ],
    'demo': [
    ],
    'data': [
        'report/contract_report.xml',
        'report/report_alta.xml',
        'report/report_baja.xml',
        'report/report_retirement.xml',
        'report/export_craft_report.xml',
        'view/craft_view.xml',
        'view/contract_view.xml',
        'report/cuota_report.xml',
        'report/recibo.xml',
        'report/member_report.xml',
        'report/auth_wizard.xml',
        'report/cancel_wizard.xml',
        'report/receipt_report.xml',
        'report/carnet_report.xml',
        'wizard/members_views.xml',
        'wizard/ab_wizard_view.xml',
        'wizard/contract_wizard_view.xml',
        'wizard/contract_cancelled_wizard_view.xml',
        'wizard/craft_request_view.xml',
    ],
    'active': False,
    'installable': True,
}

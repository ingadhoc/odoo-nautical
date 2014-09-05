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
    'author': u'Sistemas ADHOC',
    'category': u'base.module_category_knowledge_management',
    'depends': [
      'nautical_x',
      'nautical_search_by_ni',
      'web_group_expand',
      # 'web_adhoc_cust',
      # Others addons
      # 'web_nocreatedb', Disabled for now to make it easier to test
      # 'cron_run_manually',
      'disable_openerp_online',
      # OpenERP officla addons
      'base_import',
      'purchase',
      'account_cancel',
      'portal_account_summary',
        ],
    'description': """
Nautical Project
================
Installs all modules of Nautical Project

Post installation instrucions
-----------------------------
* Instal es_AR language
* Set default language to es_AR
* Habilitar "Habilitar restablecimiento de la contraseña desde la página de inicio de sesión"
* Habilitar listas de precios en sales
* Configurar next call de los crons: Create invoice (01/mm/yy) y interests (11/mm/yy) y también de facturacion de manual invoice sale order
* Configurar plazo de pago predeterminado el día 10 del mes
* Configuracion de intereses:
/ Intereses en deudores por venta
/ Crear diario tipo nota de debito
* Establecer uoms por defecto:
    eslora, manga y puntal: irían en metros
    Desplazamiento en toneladas
    Potencia en HP


Projects required:
* lp:~sistemas-adhoc/openerp-l10n-ar-localization/7.0
* lp:~sistemas-adhoc/adhoc-oerp/7.0
* lp:server-env-tools/7.0 --> disable_openerp_online
* lp:web-addons/7.0 --> web_nocreatedb, web_m2x_options
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Nautical Project',
    'test': [],
    'demo': [
    ],
    'data': [     
    ],
    'init_xml': [   

    ],    
    'version': u'1.1',
    'website': 'www.ingadhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

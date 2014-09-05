# -*- coding: utf-8 -*-
{'active': False,
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
        # nautical_reports, TODO hasta que ande bien aeroo lo instalamos a mano para poder traducir
        # 'portal_account_summary', TODO hasta que ande bien aeroo lo instalamos a mano para poder traducir
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
    'data': [
    ],
    'version': u'1.1',
    'website': 'www.ingadhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

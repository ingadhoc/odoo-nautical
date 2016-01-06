# -*- coding: utf-8 -*-

{
    'name': 'Nautical Portal',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'complexity': 'easy',
    'description': """

    """,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'depends': ['nautical_x','portal'],
    'data': [
        'wizard/wizard_view.xml',
        'view/portal_craft_view.xml',
        'portal_nautical_view.xml',
        'security/ir.model.access.csv',
        'security/portal_security.xml',
    ],
    'installable': True,
    'auto_install': True,
    'category': 'Hidden',
}

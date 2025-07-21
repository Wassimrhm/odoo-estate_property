{
    'name': 'Estate',
    'version': '1.0',
    'summary': 'Un module Odoo minimal',
    'description': 'Ce module est vide et sert de base.',
    'author': 'Rahmani Wassim Takieddine',
    'category': 'Uncategorized',
    'depends': ['base','sale_management','account','mail','contacts'],
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequences.xml",
        "views/properties_views.xml",
        "views/property_hist_view.xml",
        "views/sale_order_view.xml",
        "views/configuration_view.xml",
        "views/res_partner_view.xml",
        "views/building_view.xml",
        "views/account_move_view.xml",
        "wizards/property_wizard_view.xml",
        "reports/property_report.xml",
        "views/menus.xml",
    ],
    'assets':{
        'web.assets_backend':['estate_module/static/src/css/property.css',
                              'estate_module/static/src/components/list_view.css',
                              'estate_module/static/src/components/list_view.xml',
                              'estate_module/static/src/components/list_view.js'
                            ],

        'web.report_assets_backend':['estate_module/static/src/fronts/kaushan-script.ttf']
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

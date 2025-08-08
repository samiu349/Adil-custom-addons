{
    'name': 'Bon de Livraison 2 pages par feuille',
    'version': '1.0',
    'summary': 'Imprimer les bons de livraison avec 2 pages sur une feuille A4',
    'category': 'Inventory',
    'author': 'Alternative IT',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',


        'views/report_delivery_2pages.xml',
        'views/report_action_delivery_2pages.xml',  # D'abord le rapport !
        'views/picking_button_print_2pages.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {
        'python': ['PyPDF2'],
    },
}

{
    "name": "ALT Reports Excel",
    "version": "1.0",
    "depends": ["account", "report_xlsx"],
    "category": "Reporting",
    "author": "Alternative IT",
    "summary": "Export des factures en Excel",
    "description": "Permet d'exporter les factures en Excel avec filtres personnalisés.",
    "installable": True,
    "application": False,
    "data": [
        "security/ir.model.access.csv",
        "views/invoice_report_wizard_view.xml",
        'views/export_excel_menus.xml',
    ]
}

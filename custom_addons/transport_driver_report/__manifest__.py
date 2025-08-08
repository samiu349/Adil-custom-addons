{
    "name": "Transport Driver Report",
    "version": "17.0.1.0.0",
    "depends": ["sale", "account", "report_xlsx"],
    "category": "Custom",
    "summary": "Génère un rapport Excel mensuel par chauffeur",

    "author": "Alternative IT",
    "installable": True,
    "auto_install": False,
    "data": [
"views/driver_report_menu.xml",
        "views/driver_report_wizard_view.xml",

    ]
}
{
    "name": "Advanced Check Management",
    "version": "1.0",
    "summary": "Gestion avancée des chèques client/fournisseur",
    "category": "Accounting",
    "author": "Alternative IT",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "views/account_check_views.xml",
        "views/account_my_payment_views.xml",

        "views/menu.xml",
    ],
    "installable": True,
    "application": True,
}
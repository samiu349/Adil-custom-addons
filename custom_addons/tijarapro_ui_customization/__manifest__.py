{
    "name": "TIJARAPRO UI Customization",
    "version": "1.0",
    "category": "Customization",
    "depends": ["web"],
    "assets": {
        "web.assets_backend": [
            "tijarapro_ui_customization/static/src/js/custom_ui.js",
            "tijarapro_ui_customization/views/assets.xml"
        ]
    },
    'data': [
        'views/menu_sequence.xml',
    ],
    "installable": True,
    "application": False
}

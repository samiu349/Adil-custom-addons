from odoo import models, fields, api, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char(
        string='Order Reference',
        required=True,
        index='trigram',
        copy=False,
        default=lambda self: _('Nouveau')
    )

from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    invoice_on_order = fields.Boolean(
        string="Facturer la quantité commandée",
        help="Si coché, les lignes de vente de cette catégorie seront facturées selon la quantité commandée, même si la quantité livrée est différente."
    )

from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    chauffeur_id = fields.Many2one(
        'res.partner',
        string="Chauffeur",
        domain="[('is_driver', '=', True)]"
    )
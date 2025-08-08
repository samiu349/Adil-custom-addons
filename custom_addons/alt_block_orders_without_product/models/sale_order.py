from odoo import models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            if not order.order_line:
                raise UserError(_("Vous ne pouvez pas confirmer un devis sans au moins un produit."))
        return super().action_confirm()

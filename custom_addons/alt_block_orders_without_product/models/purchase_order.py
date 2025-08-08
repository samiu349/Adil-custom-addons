from odoo import models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        for order in self:
            if not order.order_line:
                raise UserError(_("Vous ne pouvez pas confirmer une demande d'achat sans au moins un produit."))
        return super().button_confirm()

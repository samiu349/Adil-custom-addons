from odoo import models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        invoice_line_vals = super()._prepare_invoice_line(**optional_values)

        if self.product_id.categ_id.invoice_on_order:
            invoice_line_vals['quantity'] = self.product_uom_qty

        return invoice_line_vals

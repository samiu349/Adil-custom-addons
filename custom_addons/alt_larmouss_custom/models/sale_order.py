from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        client_divers = self.env['res.partner'].search([
            ('name', '=', 'Client Divers'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        if not client_divers:
            client_divers = self.env['res.partner'].search([
                ('name', '=', 'Client Divers'),
            ], limit=1)
        if client_divers:
            res['partner_id'] = client_divers.id
        return res

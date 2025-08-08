from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Float(string="Plafond Crédit")
    payment_days = fields.Integer(string="Délai de paiement (jours)")

    @api.constrains('phone', 'street')
    def _check_required_fields(self):
        for rec in self:
            if not rec.phone or not rec.street:
                raise ValidationError("Les champs Téléphone et Adresse sont obligatoires.")

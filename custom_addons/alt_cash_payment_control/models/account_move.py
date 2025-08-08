from odoo import models, _
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        for move in self:
            if move.journal_id.code == 'CSH1':
                for line in move.line_ids:
                    if  (line.debit > 4999 or line.credit > 4999):
                        raise ValidationError(
                            _("Interdit : Le montant du paiement espèces  ne doit pas dépacer 4999.")
                        )
        return super()._post(soft=soft)

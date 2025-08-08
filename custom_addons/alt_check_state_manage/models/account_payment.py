from odoo import models, api, _
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_reconcile_check(self):
        for payment in self:
            if payment.state != 'posted':
                raise UserError(_("Le paiement doit être comptabilisé."))
            if not payment.is_matched:
                payment.is_matched = True
                payment.message_post(body=_("Chèque réglé à la banque."))

    def action_send_to_bank(self):
        for payment in self:
            if payment.state != 'posted':
                raise UserError(_("Le paiement doit être comptabilisé."))
            if not payment.is_move_sent:
                payment.is_move_sent = True
                payment.message_post(body=_("Chèque envoyé à la banque."))

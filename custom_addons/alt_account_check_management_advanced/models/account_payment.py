
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    check_id = fields.Many2one('account.check', string='Chèque existant')
    use_existing_check = fields.Boolean(string='Utiliser un chèque client')

    @api.model_create_multi
    def create(self, vals_list):
        payments = super().create(vals_list)
        for payment in payments:
            payment._create_check_if_needed()
        return payments

    def write(self, vals):
        result = super().write(vals)
        for payment in self:
            if payment.check_id:
                if 'bank_reference' in vals:
                    payment.check_id.bank = vals['bank_reference']
                if 'cheque_reference' in vals:
                    payment.check_id.check_number = vals['cheque_reference']
                if 'date' in vals:
                    payment.check_id.issue_date = vals['date']
                if 'ref' in vals:
                    payment.check_id.memo = vals['ref']
        return result

    def _create_check_if_needed(self):
        if self.payment_method_line_id.code != 'check_printing':
            return
        if self.payment_type == 'outbound':
            if self.use_existing_check:
                if not self.check_id:
                    raise UserError("Veuillez sélectionner un chèque existant.")
                if self.check_id.state != 'received':
                    raise UserError("Le chèque sélectionné n'est pas valide pour un paiement.")
                self.check_id.state = 'used'
            else:
                self._create_check('outgoing')
        elif self.payment_type == 'inbound':
            self._create_check('incoming')

    def _create_check(self, check_type):
        new_check = self.env['account.check'].create({
            'name': self.env['ir.sequence'].next_by_code('account.check') or _('Nouveau'),
            'type': check_type,
            'partner_id': self.partner_id.id,
            'bank': self.bank_reference,
            'check_number': self.cheque_reference,
            'issue_date': self.date,
            'amount': self.amount,
            'memo': self.ref,
            'state': 'received',
            'payment_id': self.id,
        })
        self.check_id = new_check.id

    def action_open_related_check(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Chèque lié'),
            'res_model': 'account.check',
            'view_mode': 'form',
            'res_id': self.check_id.id,
            'target': 'current',
        }


from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountCheck(models.Model):
    _name = 'account.check'
    _description = 'Chèque'
    _inherit = ['mail.thread']

    name = fields.Char('Référence', required=True, default=lambda self: _('Nouveau'))
    type = fields.Selection([
        ('incoming', 'Chèque reçu (client)'),
        ('outgoing', 'Chèque émis (fournisseur)'),
    ], required=True)
    amount = fields.Monetary('Montant', required=True)
    partner_id = fields.Many2one('res.partner', string='Client/Fournisseur', required=True)
    payment_id = fields.Many2one('account.payment', string='Paiement lié')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('received', 'Reçu'),
        ('used', 'Utilisé'),
        ('cleared', 'Encaissé'),
        ('returned', 'Rejeté'),
    ], default='draft', tracking=True)
    check_number = fields.Char('N° de chèque')
    bank = fields.Char('Banque')
    memo = fields.Char('Memo')
    issue_date = fields.Date("Date d’émission")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    def action_mark_received(self):
        for check in self:
            if check.state == 'draft':
                check.state = 'received'

    def action_mark_cleared(self):
        for check in self:
            if not check.amount or not check.partner_id:
                raise UserError(_("Le montant et le partenaire doivent être définis."))
            if check.state == 'received':
                check.state = 'cleared'


    def action_mark_returned(self):
        for check in self:
            if check.state == 'received':
                check.state = 'returned'

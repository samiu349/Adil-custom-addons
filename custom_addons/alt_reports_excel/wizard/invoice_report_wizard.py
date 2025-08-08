from odoo import models, fields

class InvoiceReportWizard(models.TransientModel):
    _name = 'invoice.report.wizard'
    _description = 'Assistant Rapport Factures'

    date_month = fields.Date(string="Mois", required=True)

    #date_from = fields.Date(string="Date de début")
    #date_to = fields.Date(string="Date de fin")
    #journal_id = fields.Many2one('account.journal', string="Journal")
    report_type = fields.Selection([
        ('invoice_client', 'Factures Clients'),
        ('invoice_fournisseur', 'Factures Fournisseurs'),
        ('sale', 'Commandes de vente'),
        ('purchase', 'Commandes d\'achat'),
        ('payment', 'Paiements'),
        ('transport', 'Transport'),
    ], string="Type de rapport", required=True, default='invoice_client')

    def export_excel_report(self):
        return self.env.ref('alt_reports_excel.action_export_invoice_excel').report_action(self)

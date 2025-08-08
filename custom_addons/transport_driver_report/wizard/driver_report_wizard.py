from odoo import models, fields

class TransportDriverReportWizard(models.TransientModel):
    _name = 'report.transport.driver.wizard'
    _description = 'Assistant Rapport Chauffeur'

    date_month = fields.Date(string="Mois", required=True)

    def export_report(self):
        return self.env.ref('transport_driver_report.action_export_driver_report_xlsx').report_action(self)
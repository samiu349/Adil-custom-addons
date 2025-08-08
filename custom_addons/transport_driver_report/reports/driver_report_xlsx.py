from odoo import models
import io
import base64
from datetime import datetime
from dateutil.relativedelta import relativedelta

class DriverReportXlsx(models.AbstractModel):
    _name = 'report.transport_driver_report.report_driver_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Rapport Excel Chauffeurs'

    def generate_xlsx_report(self, workbook, data, wizard):
        month_start = wizard.date_month.replace(day=1)
        month_end = (month_start + relativedelta(months=1)) - relativedelta(days=1)

        sale_line_model = self.env['sale.order.line']
        payment_model = self.env['account.payment']
        partner_model = self.env['res.partner'].search([('is_driver', '=', True)])

        for driver in partner_model:
            lines = sale_line_model.search([
                ('chauffeur_id', '=', driver.id),
                ('order_id.date_order', '>=', month_start),
                ('order_id.date_order', '<=', month_end),
            ])
            payments = payment_model.search([
                ('partner_id', '=', driver.id),
                ('payment_type', '=', 'outbound'),
                ('date', '>=', month_start),
                ('date', '<=', month_end),
                ('journal_id.code', 'in', ['SAL', 'GAS', 'DEP', 'AUT'])
            ])

            sheet = workbook.add_worksheet(driver.name[:31])
            bold = workbook.add_format({'bold': True})
            money = workbook.add_format({'num_format': '#,##0.00'})

            row = 0
            sheet.write(row, 0, "Voyages", bold)
            row += 1
            sheet.write_row(row, 0, ["Client", "Date", "Prix", "État"], bold)
            row += 1
            for line in lines:
                sheet.write(row, 0, line.order_id.partner_id.name)
                sheet.write(row, 1, str(line.order_id.date_order.date()))
                sheet.write(row, 2, line.price_total, money)
                sheet.write(row, 3, line.order_id.state)
                row += 1

            row += 2
            sheet.write(row, 0, "Dépenses", bold)
            row += 1
            sheet.write_row(row, 0, ["Journal", "Montant"], bold)
            row += 1
            for journal in payments.mapped('journal_id'):
                total = sum(payments.filtered(lambda p: p.journal_id.id == journal.id).mapped('amount'))
                sheet.write(row, 0, journal.name)
                sheet.write(row, 1, total, money)
                row += 1
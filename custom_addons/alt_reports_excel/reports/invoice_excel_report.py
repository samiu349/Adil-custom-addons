from dateutil.relativedelta import relativedelta

from odoo import models
import base64
import io


class InvoiceExcelReport(models.AbstractModel):
    _name = 'report.alt_reports_excel.report_invoice_excel'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Rapport Excel Factures'

    def generate_xlsx_report(self, workbook, data, wizard):
        method_map = {
            'invoice_client': self.generate_xlsx_report_factures_client,
            'invoice_fournisseur': self.generate_xlsx_report_factures_client,
            'sale': self.generate_xlsx_report_sales,
            'purchase': self.generate_xlsx_report_purchases,
            'payment': self.generate_xlsx_report_payments,
            'transport': self.generate_xlsx_report_transport,
        }

        method = method_map.get(wizard.report_type)
        if method:
            method(workbook, data, wizard)
        else:
            raise ValueError("Type de rapport non pris en charge.")

    def _setup_sheet(self, workbook, wizard, title):
        sheet = workbook.add_worksheet(title)

        # Styles
        header_style = workbook.add_format({'bold': True, 'font_size': 14})
        title_style = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
        logo_options = {'x_scale': 0.5, 'y_scale': 0.5}

        # Logo
        company = wizard.env.company
        if company.logo:
            logo_data = base64.b64decode(company.logo)
            logo_image = io.BytesIO(logo_data)
            sheet.insert_image('A1', 'logo.png', {
                'image_data': logo_image,
                'x_scale': 0.15,
                'y_scale': 0.15,
                'x_offset': 5,
                'y_offset': 5,
                'object_position': 1
            })

        # Titre
        sheet.merge_range('C1:F1', f'{title} - {company.name}', title_style)

        # Formats
        styles = {
            'header': workbook.add_format({
                'bold': True, 'bg_color': '#DDEBF7', 'border': 1, 'align': 'center'
            }),
            'money': workbook.add_format({'num_format': '#,##0.00', 'border': 1}),
            'date': workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1}),
            'text': workbook.add_format({'border': 1}),
        }

        return sheet, styles

    def generate_xlsx_report_factures_client(self, workbook, data, wizard):
        domain = [('move_type', '=', 'out_invoice'), ('state', '=', 'posted')]
        date_from = wizard.date_month.replace(day=1)
        date_to = (date_from + relativedelta(months=1)) - relativedelta(days=1)

        if date_from:
            domain.append(('invoice_date', '>=', date_from))
        if date_to:
            domain.append(('invoice_date', '<=', date_to))

        domain.append(('journal_id.code', 'in', ['FAC']))

        invoices = wizard.env['account.move'].search(domain)

        sheet, styles = self._setup_sheet(workbook, wizard, "Factures Clients")

        headers = ['Facture', 'Client', 'Date', 'Montant']
        for col, h in enumerate(headers):
            sheet.write(3, col, h, styles['header'])

        for row, inv in enumerate(invoices, start=4):
            sheet.write(row, 0, inv.name, styles['text'])
            sheet.write(row, 1, inv.partner_id.name or '', styles['text'])
            sheet.write(row, 2, inv.invoice_date, styles['date'])
            sheet.write(row, 3, inv.amount_total, styles['money'])

    def generate_xlsx_report_factures_fournisseur(self, workbook, data, wizard):
        # À implémenter selon la logique souhaitée
        pass

    def generate_xlsx_report_sales(self, workbook, data, wizard):
        # À implémenter selon la logique souhaitée
        pass

    def generate_xlsx_report_purchases(self, workbook, data, wizard):
        # À implémenter selon la logique souhaitée
        pass

    def generate_xlsx_report_payments(self, workbook, data, wizard):
        # À implémenter selon la logique souhaitée
        pass

    def generate_xlsx_report_transport(self, workbook, data, wizard):
        month_start = wizard.date_month.replace(day=1)
        month_end = (month_start + relativedelta(months=1)) - relativedelta(days=1)
        year_start = month_start.replace(month=1, day=1)
        year_end = month_start.replace(month=12, day=31)

        sale_line_model = self.env['sale.order.line']
        payment_model = self.env['account.payment']
        partner_model = self.env['res.partner'].search([('is_driver', '=', True)])

        for driver in partner_model:
            lines = sale_line_model.search([
                ('chauffeur_id', '=', driver.id),
                ('order_id.date_order', '>=', month_start),
                ('order_id.date_order', '<=', month_end),
            ])
            payments_monthly = payment_model.search([
                ('partner_id', '=', driver.id),
                ('payment_type', '=', 'outbound'),
                ('date', '>=', month_start),
                ('date', '<=', month_end),
                ('journal_id.code', 'in', ['SAL', 'GAS', 'DEPM'])
            ])

            payments_annual = payment_model.search([
                ('partner_id', '=', driver.id),
                ('payment_type', '=', 'outbound'),
                ('date', '>=', year_start),
                ('date', '<=', year_end),
                ('journal_id.code', 'in', ['ASS', 'PNE', 'DEPA'])
            ])


            sheet = workbook.add_worksheet(driver.name[:31])
            bold = workbook.add_format({'bold': True})
            money = workbook.add_format({'num_format': '#,##0.00'})

            row = 0
            sheet.write(row, 0, driver.name[:31], bold)
            row = 2
            sheet.write(row, 0, "Voyages", bold)
            row += 1
            sheet.write_row(row, 0, ["Client", "Date", "Prix"], bold)
            row += 1
            total_in = 0
            for line in lines:
                sheet.write(row, 0, line.order_id.partner_id.name)
                sheet.write(row, 1, str(line.order_id.date_order.date()))
                sheet.write(row, 2, line.price_total, money)
                total_in += line.price_total
                row += 1

            row = 2
            sheet.write(row, 5, "Dépenses", bold)
            row += 1
            sheet.write_row(row, 5, ["Journal", "Montant"], bold)
            row += 1
            total_out_month = 0
            for journal in payments_monthly.mapped('journal_id'):
                total = sum(payments_monthly.filtered(lambda p: p.journal_id.id == journal.id).mapped('amount'))
                sheet.write(row, 5, journal.name)
                sheet.write(row, 6, total, money)
                total_out_month += total
                row += 1

            total_out_annual = 0
            for journal in payments_annual.mapped('journal_id'):
                total = sum(payments_annual.filtered(lambda p: p.journal_id.id == journal.id).mapped('amount')) / 12
                sheet.write(row, 5, journal.name)
                sheet.write(row, 6, total, money)
                total_out_annual += total
                row += 1
            row += 1

            sheet.write(row, 5, 'Entrées')
            sheet.write(row+1, 5, 'Sortie')
            sheet.write(row+2, 5, 'Marge')
            sheet.write(row, 6, total_in, money)
            sheet.write(row+1, 6, total_out_month + total_out_annual, money)
            sheet.write(row+2, 6, total_in - total_out_month - total_out_annual, money)



from odoo import models
from odoo.http import request
from io import BytesIO
from .. import report_utils
import logging




_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_print_2pages_pdf(self):
        self.ensure_one()
        _logger.info(f"Alternative == befor")

        report_action = self.env.ref('stock.action_report_delivery')
        report_name = report_action.name or "report"
        filename = f"{report_name}_{self.name}.pdf"
        _logger.info(f"Alternative == {filename}")

        # pdf_content, _ = report._render_qweb_pdf([self.id])
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf('stock.action_report_delivery', [self.id])
        _logger.info(f"Alternative == betw")

        transformed_pdf = report_utils.duplicate_each_page_on_landscape_a4(BytesIO(pdf_content))
        _logger.info(f"Alternative == alter")

        # Sauvegarde temporaire sur le fil de la requête pour téléchargement
        request.session['delivery_2pages_pdf'] = transformed_pdf
        request.session['delivery_2pages_pdf_filename'] = filename

        return {
            'type': 'ir.actions.act_url',
            'url': '/delivery_2pages_pdf/download',
            'target': 'new',
        }

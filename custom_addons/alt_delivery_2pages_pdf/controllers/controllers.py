from io import BytesIO

from odoo import http
from odoo.http import request

class Delivery2PagesController(http.Controller):

    @http.route('/delivery_2pages_pdf/download', type='http', auth='user')
    def download_pdf(self):
        pdf_data = request.session.get('delivery_2pages_pdf')
        filename = request.session.get('delivery_2pages_pdf_filename', 'document.pdf')
        if not pdf_data:
            return request.not_found()

        return request.make_response(
            pdf_data,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', f'attachment; filename="{filename}"')
            ]
        )

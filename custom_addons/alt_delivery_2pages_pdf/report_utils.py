from PyPDF2 import PdfReader, PdfWriter, Transformation
from PyPDF2._page import PageObject
from io import BytesIO

import logging

_logger = logging.getLogger(__name__)

# Fonction utilitaire pour créer une copie transformée d'une page
def make_strong_transformed_copy(page, transformations):
    temp_writer = PdfWriter()
    temp_writer.add_page(page)
    temp_stream = BytesIO()
    temp_writer.write(temp_stream)
    temp_stream.seek(0)
    copy_page = PdfReader(temp_stream).pages[0]
    for t in transformations:
        copy_page.add_transformation(t)
    return copy_page

# Fonction principale à utiliser dans ton module Odoo
def duplicate_each_page_on_landscape_a4(pdf_stream):
    A4_LANDSCAPE_WIDTH = 842  # points
    A4_LANDSCAPE_HEIGHT = 595  # points
    A5_WIDTH = A4_LANDSCAPE_WIDTH / 2

    reader = PdfReader(pdf_stream)
    writer = PdfWriter()

    for original_page in reader.pages:
        new_page = PageObject.create_blank_page(width=A4_LANDSCAPE_WIDTH, height=A4_LANDSCAPE_HEIGHT)

        original_width = float(original_page.mediabox.width)
        scale_factor =A5_WIDTH / original_width



        _logger.info(f"Alternative A5_WIDTH == {A5_WIDTH}")
        _logger.info(f"Alternative original_width == {original_width}")
        _logger.info(f"Alternative scale_factor == {scale_factor}")


        # ✅ Première copie à gauche
        copy1 = make_strong_transformed_copy(original_page, [
            Transformation().scale(sx=scale_factor, sy=scale_factor)
        ])
        new_page.merge_page(copy1)



        # ✅ Deuxième copie à droite
        corrected_translation = A5_WIDTH / scale_factor  # Translation compensée du scale
        copy2 = make_strong_transformed_copy(original_page, [

            Transformation().translate(tx=corrected_translation-100, ty=0),
            Transformation().scale(sx=scale_factor, sy=scale_factor)
        ])
        new_page.merge_page(copy2)



        writer.add_page(new_page)

    output_stream = BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream.read()

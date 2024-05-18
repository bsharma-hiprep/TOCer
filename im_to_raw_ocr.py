"""_summary_
Works well. Extracts images from a PDF, performs OCR on them, and adds page breaks.
Verdict: Usable. Make sure to test it on a variety of PDFs to ensure it works as expected.
"""

import fitz  # PyMuPDF
import re
import pytesseract
from PIL import Image
import io
import PyPDF2

# Extract images from the PDF
def extract_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page_images = page.get_images(full=True)

        for img in page_images:
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append((image, page_num + 1))

    return images

# Perform OCR on the extracted images and add page breaks
def perform_ocr_on_images(images):
    extracted_text = ""
    page_breaks = []

    for page_num, (image, actual_page_num) in enumerate(images, start=1):
        text = pytesseract.image_to_string(image)
        extracted_text += f"__page {actual_page_num}__\n{text}\n"
        page_breaks.append(f"__page {actual_page_num}__")

    return extracted_text, page_breaks
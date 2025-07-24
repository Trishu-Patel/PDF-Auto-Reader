from pdf2image import convert_from_path
from utils.constants import POPPLER_PATH, TEMP_DIR
import os
from PIL.Image import Image
import PyPDF2


def pdf_to_image(pdf_path: str, page_number: int) -> Image | None:
    """
    Convert a PDF file to a PIL Image object for a specific page.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        Image | None: The PIL Image object for the specified page, or None if conversion fails.
    """

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    try:
        images = convert_from_path(
            pdf_path,
            fmt="png",
            poppler_path=POPPLER_PATH,
            thread_count=4,
            first_page=page_number,
            last_page=page_number,
        )

        return images[0]

    except:
        return None


def get_number_of_pages(pdf_path: str) -> int:
    """
    Get the number of pages in a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        int: The number of pages in the PDF.
    """
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            return len(reader.pages)
    except Exception as e:
        return 0

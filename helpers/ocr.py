from PIL.Image import Image
import pytesseract

def optical_character_recognition(image: Image) -> str:
    """
    Perform Optical Character Recognition (OCR) on the given image

    Args:
        image (Image): PIL Image object containing the image to process.
        
    Returns:
        str: The text extracted from the image.
    """
    try:
        # Use pytesseract to perform OCR on the image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""
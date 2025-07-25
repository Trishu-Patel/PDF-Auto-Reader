from PIL.Image import Image

def process_image(image: Image, x1: int, y1: int, x2: int, y2: int):
    """
    Process the image by cropping it to the specified coordinates.
    
    Args:
        image (Image): The image to process.
        x1 (int): The x-coordinate of the top-left corner of the crop rectangle.
        y1 (int): The y-coordinate of the top-left corner of the crop rectangle.
        x2 (int): The x-coordinate of the bottom-right corner of the crop rectangle.
        y2 (int): The y-coordinate of the bottom-right corner of the crop rectangle.

    Returns:
        Image: The cropped image.
    """
    
    cropped_image = image.crop((x1, y1, x2, y2))
    
    return cropped_image
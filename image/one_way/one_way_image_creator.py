from PIL import Image, ImageOps
import io

def create_one_way_image(image_data, invert=False, rotate=0):
    """
    Create and process an image from One Way Space.
    
    Args:
        image_data: The binary image data.
        invert: Whether to invert the image colors.
        rotate: Rotation angle (0, 90, 180, or 270).
    
    Returns:
        A PIL Image object.
    """
    try:
        # Load the image using PIL
        img = Image.open(io.BytesIO(image_data))
        
        # Process invert if requested
        if invert:
            img = ImageOps.invert(img.convert('RGB'))
        
        # Process rotation if requested
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)
        
        return img
    except Exception as e:
        print(f"Error processing One Way image: {e}")
        raise
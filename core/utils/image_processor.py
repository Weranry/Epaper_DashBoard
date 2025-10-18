"""Image processing utilities for common operations"""
from PIL import ImageOps
from io import BytesIO


class ImageProcessor:
    """Utility class for common image processing operations"""
    
    @staticmethod
    def apply_invert(img, invert=False):
        """
        Apply color inversion to image
        
        Args:
            img: PIL Image object
            invert: Boolean flag for inversion
            
        Returns:
            Processed PIL Image object
        """
        if invert:
            return ImageOps.invert(img.convert('RGB'))
        return img
    
    @staticmethod
    def apply_rotation(img, rotate=0):
        """
        Apply rotation to image
        
        Args:
            img: PIL Image object
            rotate: Rotation angle (0, 90, 180, 270)
            
        Returns:
            Rotated PIL Image object
        """
        if rotate in [90, 180, 270]:
            return img.rotate(rotate, expand=True)
        return img
    
    @staticmethod
    def process_image(img, invert=False, rotate=0):
        """
        Apply both inversion and rotation to image
        
        Args:
            img: PIL Image object
            invert: Boolean flag for inversion
            rotate: Rotation angle (0, 90, 180, 270)
            
        Returns:
            Processed PIL Image object
        """
        img = ImageProcessor.apply_invert(img, invert)
        img = ImageProcessor.apply_rotation(img, rotate)
        return img
    
    @staticmethod
    def get_image_bytes(img, format='JPEG', quality=95, subsampling=0):
        """
        Convert PIL Image to BytesIO object
        
        Args:
            img: PIL Image object
            format: Image format (JPEG, PNG, etc.)
            quality: Image quality (1-100 for JPEG)
            subsampling: Subsampling mode (0=4:4:4, 1=4:2:2, 2=4:2:0)
            
        Returns:
            BytesIO object containing image data
        """
        img_io = BytesIO()
        if format.upper() == 'JPEG':
            img.save(img_io, format, quality=quality, subsampling=subsampling)
        else:
            img.save(img_io, format)
        img_io.seek(0)
        return img_io

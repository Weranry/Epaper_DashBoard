"""Base class for image creators"""
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from core.utils.image_processor import ImageProcessor
import os


class BaseImageCreator:
    """Base class for all image creator classes"""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self._load_default_fonts()
    
    def _load_default_fonts(self):
        """Load default fonts used across image creators"""
        font_path = os.path.join('assets', 'simhei.ttf')
        try:
            self.font_small = ImageFont.truetype(font_path, 12)
            self.font_normal = ImageFont.truetype(font_path, 14)
            self.font_medium = ImageFont.truetype(font_path, 18)
            self.font_large = ImageFont.truetype(font_path, 24)
            self.font_xlarge = ImageFont.truetype(font_path, 120)
        except Exception as e:
            # Fallback to default font if custom font not found
            self.font_small = ImageFont.load_default()
            self.font_normal = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_large = ImageFont.load_default()
            self.font_xlarge = ImageFont.load_default()
    
    def create_base_image(self, width=400, height=300, mode='P'):
        """
        Create a base image with standard palette
        
        Args:
            width: Image width
            height: Image height
            mode: Image mode ('P' for indexed, 'RGB' for RGB)
            
        Returns:
            PIL Image object
        """
        img = Image.new(mode, (width, height))
        if mode == 'P':
            # Standard palette: white, black, red
            img.putpalette([
                255, 255, 255,  # White (0)
                0, 0, 0,        # Black (1)
                255, 0, 0       # Red (2)
            ])
        return img
    
    def get_image_bytes(self, img, format='JPEG', quality=95, subsampling=0):
        """
        Convert PIL Image to BytesIO object
        
        Args:
            img: PIL Image object
            format: Image format (JPEG, PNG, etc.)
            quality: Image quality (1-100 for JPEG)
            subsampling: Subsampling mode (0=4:4:4)
            
        Returns:
            BytesIO object containing image data
        """
        return self.image_processor.get_image_bytes(img, format, quality, subsampling)
    
    def create_image(self, data):
        """
        Abstract method to create image - should be implemented by subclasses
        
        Args:
            data: Data needed to create the image
            
        Returns:
            PIL Image object
        """
        raise NotImplementedError("Subclasses must implement create_image method")

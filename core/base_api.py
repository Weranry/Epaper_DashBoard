"""Base API class for common route functionality"""
from flask import request, send_file
from core.utils.image_processor import ImageProcessor


class BaseImageAPI:
    """Base class for image-generating API endpoints"""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
    
    def get_common_params(self):
        """
        Extract common parameters from request
        
        Returns:
            dict: Dictionary containing common parameters (invert, rotate)
        """
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))
        return {
            'invert': invert,
            'rotate': rotate
        }
    
    def process_and_send_image(self, img, mimetype='image/jpeg'):
        """
        Process image with common operations and send as response
        
        Args:
            img: PIL Image object
            mimetype: MIME type for response
            
        Returns:
            Flask response with image file
        """
        params = self.get_common_params()
        img = self.image_processor.process_image(
            img, 
            invert=params['invert'], 
            rotate=params['rotate']
        )
        img_io = self.image_processor.get_image_bytes(img)
        return send_file(img_io, mimetype=mimetype)


class BaseJsonAPI:
    """Base class for JSON-generating API endpoints"""
    
    def __init__(self):
        pass
    
    def get_common_params(self):
        """
        Extract common parameters from request
        
        Returns:
            dict: Dictionary containing common parameters
        """
        return {}

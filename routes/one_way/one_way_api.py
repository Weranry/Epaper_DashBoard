from flask import Response, request, jsonify
from web.one_way.one_way_fetcher import fetch_one_way_image
from image.one_way.one_way_image_creator import create_one_way_image
import io

class OneWayImageAPI:
    def get_one_way_image(self):
        # Get request parameters
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))
        
        # Fetch the image content
        image_data = fetch_one_way_image()
        
        if image_data is None:
            return jsonify({"error": "Failed to fetch One Way image"}), 404
        
        try:
            # Process the image using the image creator
            img = create_one_way_image(image_data, invert, rotate)
            
            # Save the processed image to a bytes buffer
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            
            # Return the image as a response
            return Response(img_byte_arr.getvalue(), mimetype='image/jpeg')
        except Exception as e:
            return jsonify({"error": f"Error processing image: {e}"}), 500
import requests
from datetime import datetime

def fetch_one_way_image():
    """
    Fetch the daily image from One Way Space.
    Returns the image content or None if request failed.
    """
    # Format the date the same way as PHP's date("Y/md")
    current_date = datetime.now().strftime("%Y/%m%d")
    
    # Construct the image URL
    image_url = f"http://img.owspace.com/Public/uploads/Download/{current_date}.jpg"
    
    try:
        # Get the image content
        response = requests.get(image_url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        print(f"Error fetching One Way image: {e}")
        return None
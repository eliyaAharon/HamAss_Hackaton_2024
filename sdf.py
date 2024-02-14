import os

from deepface import DeepFace
from PIL import Image


def face_match(image1, image2):
    try:
        # Convert PIL images to file paths
        temp_image1_path = "temp_image1.jpg"

        result = DeepFace.verify(temp_image1_path, "elya.jpg", model_name="Facenet", distance_metric='euclidean_l2')
        return result["verified"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    finally:
        # Remove temporary files
        try:
            os.remove(temp_image1_path)
        except:
            pass

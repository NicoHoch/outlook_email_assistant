from google.cloud import vision
from google.cloud.vision_v1 import types


def detect_text_from_image(content):
    """
    Detects text in the given image content using Google Vision API.

    Args:
        content (bytes): The image content in bytes.

    Returns:
        str: The detected text concatenated into a single string.

    Raises:
        Exception: If the API response contains an error.
    """
    client = vision.ImageAnnotatorClient()

    if not isinstance(content, bytes):
        raise ValueError("Content should be of type 'bytes'")

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    texts = response.text_annotations
    final_string = " ".join(text.description for text in texts).strip()

    return final_string

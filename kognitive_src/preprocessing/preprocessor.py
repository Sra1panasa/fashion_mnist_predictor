import numpy as np
import io
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from kognitive_src.utils import logger

class Preprocessor:
    """
    Preprocessor class for handling image preprocessing steps before feeding to a neural network model.
    """

    def __init__(self, target_size=(224, 224)):
        """
        Initialize the preprocessor with a target image size.
        Args:
            target_size: tuple of int
                The target size for the image after resizing (width, height).
        """
        self.target_size = target_size

    def preprocess_image(self, image_content):
        """
        Load an image from bytes and preprocess it for model prediction.
        Args:
            image_content: bytes
                The image in bytes format to be processed.
        Returns:
            A numpy array representing the preprocessed image.
        """
        try:
            # Load the image from bytes
            img = image.load_img(io.BytesIO(image_content), target_size=self.target_size)
            # Convert the image to a numpy array
            img_array = image.img_to_array(img)
            # Expand dimensions to match the model's input format
            img_array_expanded_dims = np.expand_dims(img_array, axis=0)
            # Preprocess the image using the appropriate preprocessing input for the model
            img_preprocessed = preprocess_input(img_array_expanded_dims)
            logger.info("Image preprocessing successful")
            return img_preprocessed
        except Exception as e:
            logger.error("An error occurred during image preprocessing: %s", e)
            raise e

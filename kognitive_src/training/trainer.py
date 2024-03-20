import mlflow
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.models import Sequential
from kognitive_src.utils import logger  # Assuming you have a custom logger set up here

class FashionMNISTClassifier:
    """
    Classifier for the Fashion MNIST dataset.
    """
    def __init__(self):
        self.fashion_mnist = tf.keras.datasets.fashion_mnist
        self.model = None
        self.history = None

    def load_data(self):
        """
        Loads the Fashion MNIST dataset and preprocesses it.
        
        Returns:
            Tuple of numpy arrays: (training_images, training_labels, test_images, test_labels)
        """
        (training_images, training_labels), (test_images, test_labels) = self.fashion_mnist.load_data()
        # Normalize the images to [0, 1] range
        training_images = training_images / 255.0
        test_images = test_images / 255.0
        return training_images, training_labels, test_images, test_labels

    def build_model(self):
        """
        Builds a simple neural network model for classification.
        """
        self.model = Sequential([
            Flatten(input_shape=(28, 28)),
            Dense(128, activation='relu'),
            Dense(10, activation='softmax')
        ])
        self.model.compile(optimizer=Adam(),
                           loss="sparse_categorical_crossentropy",
                           metrics=["accuracy"])
        logger.info("Model built successfully.")

    def train(self, epochs):
        """
        Trains the model on the Fashion MNIST dataset.
        
        Args:
            epochs (int): Number of epochs to train the model.
        """
        if self.model is None:
            self.build_model()

        training_images, training_labels, _, _ = self.load_data()

        # Start MLflow run
        with mlflow.start_run():
            mlflow.log_param("epochs", epochs)
            self.history = self.model.fit(training_images, training_labels, epochs=epochs)
            # Log metrics after each epoch
            for i in range(epochs):
                mlflow.log_metric("loss", self.history.history["loss"][i], step=i)
                mlflow.log_metric("accuracy", self.history.history["accuracy"][i], step=i)

            # Save the model as an MLflow artifact
            mlflow.keras.log_model(self.model, "model")
            
            logger.info("Training completed. Model logged with MLflow.")

    def evaluate(self):
        """
        Evaluates the trained model on the test set.
        """
        if self.model is None or self.history is None:
            logger.error("Model not trained yet. Please call train() first.")
            return

        _, _, test_images, test_labels = self.load_data()
        loss, accuracy = self.model.evaluate(test_images, test_labels)
        logger.info(f"Validation Loss: {loss:.4f}, Validation Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    classifier = FashionMNISTClassifier()
    classifier.train(epochs=2)  
    classifier.evaluate()  

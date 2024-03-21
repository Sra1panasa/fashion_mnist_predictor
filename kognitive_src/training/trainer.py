import mlflow
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.models import Sequential
from kognitive_src.utils import logger 

class FashionMNISTClassifier:
    def __init__(self):
        try:
            self.fashion_mnist = tf.keras.datasets.fashion_mnist
            self.model = None
            self.history = None
            logger.info("FashionMNISTClassifier initialized successfully.")
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            raise

    def load_data(self, validation_split=0.1, test_split=0.2):
        """
        Loads the Fashion MNIST dataset, preprocesses it, and splits into train, validation, test sets.

        Args:
            validation_split (float): Proportion of data for validation (default: 0.1)
            test_split (float): Proportion of data for testing (default: 0.2)

        Returns:
            Tuple of numpy arrays: 
                (training_images, training_labels, val_images, val_labels, test_images, test_labels)
        """
        try:
            (training_images, training_labels), (test_images, test_labels) = self.fashion_mnist.load_data()
            training_images = training_images / 255.0
            test_images = test_images / 255.0

            split_idx = int((1 - validation_split - test_split) * len(training_images)) 
            training_images, val_images = training_images[:split_idx], training_images[split_idx:]
            training_labels, val_labels = training_labels[:split_idx], training_labels[split_idx:]

            return training_images, training_labels, val_images, val_labels, test_images, test_labels

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def build_model(self):
        """
        Builds a simple neural network model for classification.
        """
        try:
            self.model = Sequential([
                Flatten(input_shape=(28, 28)),
                Dense(128, activation='relu'),
                Dense(10, activation='softmax')
            ])
            self.model.compile(optimizer=Adam(),
                               loss="sparse_categorical_crossentropy",
                               metrics=["accuracy"])
            logger.info("Model built successfully.")
        except Exception as e:
            logger.error(f"Error building the model: {e}")
            raise


    def train(self, epochs):
        """
        Trains the model on the Fashion MNIST dataset, using a validation set.

        Args:
            epochs (int): Number of epochs to train the model.
        """
        try:
            if self.model is None:
                self.build_model()

            training_images, training_labels, val_images, val_labels, _, _ = self.load_data()

            with mlflow.start_run():
                mlflow.log_param("epochs", epochs) 

                # Fit the model with validation data
                self.history = self.model.fit(
                    training_images, training_labels, 
                    epochs=epochs, 
                    validation_data=(val_images, val_labels)
                )

                # Log metrics with MLflow
                for i in range(epochs):
                    mlflow.log_metric("loss", self.history.history["loss"][i], step=i)
                    mlflow.log_metric("accuracy", self.history.history["accuracy"][i], step=i)
                    mlflow.log_metric("val_loss", self.history.history["val_loss"][i], step=i)
                    mlflow.log_metric("val_accuracy", self.history.history["val_accuracy"][i], step=i)

                # Log the model with MLflow
                mlflow.keras.log_model(self.model, "model") 
                logger.info("Training completed. Model logged with MLflow.")

        except Exception as e:
            logger.error(f"Error during training: {e}")
            raise


    def evaluate(self):
        """
        Evaluates the trained model on the test set.
        """
        try:
            if self.model is None or self.history is None:
                logger.error("Model not trained yet. Please call train() first.")
                return

            _, _,_, _, test_images, test_labels = self.load_data()
            loss, accuracy = self.model.evaluate(test_images, test_labels)
            logger.info(f"Validation Loss: {loss:.4f}, Validation Accuracy: {accuracy:.4f}")

        except Exception as e:  
            logger.error(f"Error during evaluation: {e}")
            raise 

if __name__ == "__main__":
    classifier = FashionMNISTClassifier()
    try:   
        classifier.train(epochs=2)  
        classifier.evaluate() 
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")

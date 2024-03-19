from fastapi import FastAPI, File, UploadFile, HTTPException
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
import numpy as np
import uvicorn
from kognitive_src.preprocessing.preprocessor import Preprocessor
from kognitive_src.utils import logger 

app = FastAPI()

# Load Base model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

x = base_model.output
x = GlobalAveragePooling2D()(x) # average pooling layer
x = Dense(1024, activation='relu')(x) # Adding a fully-connected layer
predictions = Dense(10, activation='softmax')(x) #output layer

model = Model(inputs=base_model.input, outputs=predictions)

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


preprocessor = Preprocessor(target_size=(224, 224))

@app.get("/")
async def root():
    """
    Health check endpoint.
    Returns:
        JSON response with message "API Endpoit up and running".
    """
    return {"message": "API Endpoit up and running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint for predicting the class of a fashion item in an image.
    Args:
        file: UploadFile
            The image file uploaded by the client.
    Returns:
        JSON response with the original filename and predicted class label.
    """
    try:
        # Read image contents
        contents = await file.read()
        img_preprocessed = preprocessor.preprocess_image(contents)
        
        # Make prediction using the preprocessed image
        prediction = model.predict(img_preprocessed)
        logger.info(f"Prediction made with probabilities: {prediction}")

        # Decode the predictions to get the class label
        predicted_class_index = np.argmax(prediction, axis=1)[0]
        predicted_label = class_names[predicted_class_index]
        logger.info(f"Predicted class: {predicted_label}")
        return {"filename": file.filename, "predicted_class": predicted_label}
    
    except Exception as e:
        logger.error(f"An error occurred during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

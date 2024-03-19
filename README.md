# Fashion MNIST Predictor

## Overview
This project is a machine learning application developed to classify images from the Fashion MNIST dataset. It utilizes a pre-trained neural network for inference. The application is containerized using Docker for easy Deployment and Scalability.

## Prerequisites
- Docker
- Python 3.9 or higher

## Project Structure

Below is the directory structure of the Fashion MNIST Predictor project, detailing the organization and purpose of each component:

```plaintext
Project Root
├── data                     # Data directory for storing Fashion MNIST dataset or related data files.
├── kognitive_src            # Main source code directory.
│   ├── config               # Contains configuration files for model paths, logging paths, etc.
│   │   └── config.ini       
│   ├── preprocessing        # Preprocessing scripts for preparing the dataset.
│   │   └── preprocessor.py  
│   ├── training             # Contains scripts for model training and inference.
│   │   ├── inference.py    
│   │   └── trainer.py        
│   └── utils                # Utility functions and classes.
│       └── util.py          
├── logs                     # Directory to store application logs.
├── main.py                  # Main FastAPI application entry point for API interface.
├── requirements.txt         # Lists dependencies required for the project.
├── setup.py                 # Script for installing the project as a package.
└── README.md                # README file with project documentation.

```

## Project Setup

1. **Clone the git Repository:**

   ```bash
   git clone https://yourrepositorylink.git
   
   ```

2. **Build the Docker image:**

* Go to the directory of Docker file.Run the below Docker build command.This command builds a Docker image named mnist-predictor from the Dockerfile in the current directory.

    ```
    cd Kognitive/MNIST
    docker build -t mnist-predictor 
    ```
3. **Run the Container :**

* Run the container using the docker run command.This maps port 8000 of the container to port 8000 on your host, making the application accessible at http://localhost:8000.(If we are running on any server make sure to replace localhost with server ip)

* The -v parameter mounts a volume for logs from /path/on/your/host on your local machine to /app/logs inside the container.

    ```
    docker run -p 8000:8000 -v /path/on/your/host:/app/logs mnist-predictor
    ```

## Testing the Endpoint

* Once the Docker container is up and running, the FastAPI application's `/predict` endpoint will be available for classifying images from the Fashion MNIST dataset. You can test this endpoint by sending a POST request with an image file as input. This can be done using various tools and libraries such as Postman or the Python `requests` library.

* End point url: `http://localhost:8000/predict`  (replace localhost with server IP)

**Using Postman**

1. Open Postman and create a new request.
2. Set the request type to `POST` and the request URL to `http://localhost:8000/predict`.
3. Under the `Body` tab, select `form-data`.
4. In the `Key` field, type `file`, set the type to File, and then upload the image you want to classify by clicking on the `Select Files` button.
5. Send the request to see the classification results.

**Using Python requests library**

If you prefer to use the `requests` library in Python, follow these steps:

```python
    import requests

    # URL for the FastAPI endpoint
    url = 'http://localhost:8000/predict'(replace localhost with IP)
    # Replace 'path_to_your_image' with the actual path to the image file
    files = {'file': open('path_to_your_image', 'rb')}
    response = requests.post(url, files=files)
    print(response.json())
```

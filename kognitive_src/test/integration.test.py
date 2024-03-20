import pytest
import requests
from starlette import status  

BASE_URL = "http://localhost:8000"  # API endpoint within the container

def test_root_endpoint():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "API Endpoit up and running"}

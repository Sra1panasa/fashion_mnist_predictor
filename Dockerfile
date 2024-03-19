# official lightweight Python image.
FROM python:3.9-slim

# Set the working directory in the container to /app.
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The application listens on port 8000. Make this port available outside the container.
EXPOSE 8000

CMD ["uvicorn", "kognitive_src.main:app", "--host", "0.0.0.0", "--port", "8000"]

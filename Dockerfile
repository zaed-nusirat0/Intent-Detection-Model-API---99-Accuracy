# Use the slim image of Python to minimize size
FROM python:3.9-slim

# Ensure pip is upgraded and install necessary build tools
RUN pip install --upgrade pip \
    && apt-get update \
    && apt-get install -y build-essential libssl-dev libffi-dev python3-dev \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt .

# Install the dependencies from requirements.txt without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose the application on port 8000
EXPOSE 8000

# Run the Flask application using Gunicorn for production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]

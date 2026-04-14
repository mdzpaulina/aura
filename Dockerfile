# Lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and allow logs to print directly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install the libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code from the src folder to the container
COPY src/ ./src/

# Define the entrypoint. 
# Use 'exec' mode so AURA receives system signals correctly.
ENTRYPOINT ["python", "src/main.py"]

# Default command
CMD ["--help"]
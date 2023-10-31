# Use the official Python 3.10 image as the base image
FROM python:3.10-slim

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory within the container
WORKDIR /app

# Copy the requirements.txt file to the container's working directory
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory to the container's working directory
# Copy the application code into the container
COPY src/ /app/src/

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod a+x /app/entrypoint.sh

# Specify the entry point for the container
ENTRYPOINT ["/app/entrypoint.sh"]
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y curl && apt-get clean

# Copy the script to the container
COPY check_internet.py /app/check_internet.py

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install requests

# Run the script
CMD ["python", "check_internet.py"]

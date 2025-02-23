# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script to the container
COPY net_check.py .

# Install required Python packages
RUN pip install --no-cache-dir requests pytz

# Set environment variables (optional defaults)
ENV NOTIFY_URL=""
ENV CHECK_INTERVAL=30
ENV TIMEZONE="Asia/Kolkata"

# Run the script when the container launches
CMD ["python", "net_check.py"]

FROM python:3.10-slim

# Set timezone and install dependencies
ENV TZ=Asia/Kolkata
RUN apt-get update && apt-get install -y curl tzdata && apt-get clean && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set the working directory
WORKDIR /app

# Copy the script to the container
COPY check_internet.py /app/check_internet.py

# Install Python dependencies
RUN pip install --no-cache-dir requests pytz

# Run the script
CMD ["python", "check_internet.py"]

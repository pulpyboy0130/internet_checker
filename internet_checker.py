import time
import requests
import socket
import os
import datetime
import pytz

# Set timezone to Asia/Kolkata
IST = pytz.timezone("Asia/Kolkata")

def log(message):
    """
    Log messages with an Asia/Kolkata timestamp for Portainer logs.
    """
    timestamp = datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"[{timestamp}] {message}", flush=True)  # Flush ensures logs appear in real-time

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Check if there is an internet connection by trying to connect to a public DNS server.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def notify_server(url):
    """
    Send a notification request to the specified URL.
    """
    if not url:
        log("No NOTIFY_URL set. Skipping notification.")
        return
    
    try:
        response = requests.get(url, timeout=5)
        log(f"Notification sent: {response.status_code}")
    except requests.RequestException as e:
        log(f"Failed to send notification: {e}")

def main():
    url = os.getenv("NOTIFY_URL")

    log(f"Using notification URL: {url}")

    while True:
        if not check_internet():
            log("No internet connection detected.")
            notify_server(url)
        else:
            log("Internet connection is active.")

        time.sleep(30)  # Wait for 30 seconds before the next check

if __name__ == "__main__":
    main()

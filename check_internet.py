import time
import requests
import socket
import os

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
    try:
        response = requests.get(url, timeout=5)
        print(f"Notification sent: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to send notification: {e}")

def main():
    # Get the notification URL from the environment variable or use a default value
    url = os.getenv("NOTIFY_URL")
    
    print(f"Using notification URL: {url}")

    while True:
        if not check_internet():
            print("No internet connection detected.")
            notify_server(url)
        else:
            print("Internet connection is active.")
        
        # Wait for 120 seconds before the next check
        time.sleep(120)

if __name__ == "__main__":
    main()

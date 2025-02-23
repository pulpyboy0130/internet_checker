import time
import requests
import socket
import os
import datetime
import pytz

def log(message, timezone):
    """
    Log messages with a configurable timezone timestamp for Docker/Portainer logs.
    """
    timestamp = datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"[{timestamp}] {message}", flush=True)  # Flush ensures logs appear in real-time in Docker

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
        log("No NOTIFY_URL set. Skipping notification.", TZ)
        return
    
    try:
        response = requests.get(url, timeout=5)
        log(f"Notification sent: {response.status_code}", TZ)
    except requests.RequestException as e:
        log(f"Failed to send notification: {e}", TZ)

def main():
    # Get environment variables
    url = os.getenv("NOTIFY_URL")
    
    # Get CHECK_INTERVAL from env, default to 30 seconds if not set or invalid
    try:
        check_interval = int(os.getenv("CHECK_INTERVAL", 30))
        if check_interval <= 0:
            check_interval = 30  # Enforce a minimum reasonable value
    except (ValueError, TypeError):
        check_interval = 30  # Fallback to 30 seconds if conversion fails

    # Get TIMEZONE from env, default to UTC if not set or invalid
    timezone_str = os.getenv("TIMEZONE", "UTC")
    try:
        global TZ
        TZ = pytz.timezone(timezone_str)
    except pytz.exceptions.UnknownTimeZoneError:
        log(f"Invalid timezone '{timezone_str}' provided. Falling back to UTC.", pytz.UTC)
        TZ = pytz.UTC

    log(f"Starting service with notification URL: {url}", TZ)
    log(f"Check interval set to: {check_interval} seconds", TZ)
    log(f"Using timezone: {TZ.zone}", TZ)

    while True:
        if not check_internet():
            log("No internet connection detected.", TZ)
            notify_server(url)
        else:
            log("Internet connection is active.", TZ)

        time.sleep(check_interval)  # Use the configurable interval

if __name__ == "__main__":
    main()

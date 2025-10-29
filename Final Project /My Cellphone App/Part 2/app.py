from flask import Flask
from prometheus_client import start_http_server, Gauge # pyright: ignore[reportMissingImports]
import random
import time
import threading

app = Flask(__name__)

# Simulated apps
apps = {
    "WhatsApp": True,
    "Instagram": True,
    "Gmail": True
}

# Prometheus metrics
app_status_gauge = Gauge('app_status', 'Status of each app (1=active, 0=inactive)', ['app'])
app_error_gauge = Gauge('app_errors', 'Number of errors per app', ['app'])

# Error counters
error_counts = {
    "WhatsApp": 0,
    "Instagram": 0,
    "Gmail": 0
}

# Function to simulate app status changes
def simulate_app_status():
    while True:
        for app_name in apps:
            # Randomly set app status
            status = random.choice([True, True, True, False])  # More likely to be active
            apps[app_name] = status
            app_status_gauge.labels(app=app_name).set(1 if status else 0)
            if not status:
                error_counts[app_name] += 1
                app_error_gauge.labels(app=app_name).set(error_counts[app_name])
        time.sleep(5)

# Start Prometheus metrics server
start_http_server(8000)

# Start simulation in background thread
threading.Thread(target=simulate_app_status, daemon=True).start()

@app.route('/')
def home():
    return "My Cellphone App."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
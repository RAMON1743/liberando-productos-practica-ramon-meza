"""
FastAPI application with Prometheus metrics and Hypercorn server configuration.
"""

import asyncio
import threading
import time
from fastapi import FastAPI
from fastapi.responses import Response
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCornConfig
from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

# ─────────────────────────────
# FastAPI app initialization
# ─────────────────────────────
app = FastAPI()

# ─────────────────────────────
# Prometheus Metrics
# ─────────────────────────────

# General
REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')
APP_STARTS = Counter('fastapi_app_starts_total', 'App boot counter')
APP_STARTS.inc()  # Count app startup

# Endpoint-specific
HEALTHCHECK_REQUESTS = Counter('healthcheck_requests_total', 'Total number of requests to /health')
MAIN_ENDPOINT_REQUESTS = Counter('main_requests_total', 'Total number of requests to /')
BYE_ENDPOINT_REQUESTS = Counter('bye_requests_total', 'Total number of requests to /bye')

# Simulated CPU metrics for alerts
CPU_REQUEST = Gauge('fastapi_cpu_request', 'Simulated CPU request for FastAPI')
CPU_USAGE = Gauge('fastapi_cpu_usage', 'Simulated CPU usage for FastAPI')
CPU_REQUEST.set(0.1)  # Simulated 100m CPU request

def simulate_cpu_load():
    """
    Simulates CPU usage for 3 minutes, then drops usage.
    Used to trigger and resolve Prometheus alerts.
    """
    end_time = time.time() + 180  # 3 minutes
    while time.time() < end_time:
        _ = 1 + 1  # Simulated computation
        CPU_USAGE.set(0.3)  # 300m usage
        time.sleep(1)
    CPU_USAGE.set(0.05)  # Back to normal after 3 minutes

# Start background thread for CPU simulation
threading.Thread(target=simulate_cpu_load, daemon=True).start()

# ─────────────────────────────
# FastAPI Endpoints
# ─────────────────────────────

@app.get("/health")
async def health_check():
    REQUESTS.inc()
    HEALTHCHECK_REQUESTS.inc()
    return {"health": "ok"}

@app.get("/")
async def read_main():
    REQUESTS.inc()
    MAIN_ENDPOINT_REQUESTS.inc()
    return {"msg": "Hello World"}

@app.get("/bye")
async def read_bye():
    REQUESTS.inc()
    BYE_ENDPOINT_REQUESTS.inc()
    return {"msg": "Bye Bye"}

@app.get("/metrics")
def metrics():
    """
    Exposes Prometheus metrics at /metrics
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ─────────────────────────────
# Server Configuration
# ─────────────────────────────

class SimpleServer:
    """
    Configures and starts the Hypercorn server with FastAPI app.
    """

    def __init__(self):
        self._hypercorn_config = HyperCornConfig()
        self._hypercorn_config.bind = ['0.0.0.0:8081']
        self._hypercorn_config.keep_alive_timeout = 90

    async def run_server(self):
        """Starts the FastAPI app using Hypercorn."""
        await serve(app, self._hypercorn_config)

# ─────────────────────────────
# Entry Point
# ─────────────────────────────

if __name__ == '__main__':
    server = SimpleServer()
    asyncio.run(server.run_server())

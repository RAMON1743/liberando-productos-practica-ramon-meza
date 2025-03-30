"""
Module to launch the FastAPI application with Prometheus metrics server.
"""

import asyncio
from prometheus_client import start_http_server
from application.app import SimpleServer


class AppContainer:
    """
    AppContainer manages application initialization and startup.
    """

    def __init__(self):
        self._server = SimpleServer()

    async def start(self):
        """
        Asynchronously starts the FastAPI server.
        """
        await self._server.run_server()


if __name__ == "__main__":
    # Start Prometheus metrics HTTP server on port 8000
    start_http_server(8000)

    # Initialize and run the FastAPI application
    container = AppContainer()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(container.start(), loop=loop)
    loop.run_forever()

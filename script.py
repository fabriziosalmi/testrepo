import logging
from typing import Any

import mitmproxy
from mitmproxy import http
import ipaddress

# Configure logging
logging.basicConfig(
    filename="proxy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

blocked_ip = "1.2.3.4"

class TransparentProxy:
    """
    A transparent proxy class to block requests from a specific IP address and log other requests.
    """

    def request(self, flow: http.HTTPFlow) -> None:
        """
        Handle the HTTP request.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]  # Get client IP

        # Validate the client IP address
        try:
            ipaddress.ip_address(client_ip)
        except ValueError:
            logging.error(f"Invalid IP address received: {client_ip}")
            return

        if client_ip == blocked_ip:
            logging.info(f"Blocked request from {client_ip}")
            flow.response = http.HTTPResponse.make(
                403, b"Forbidden", {"Content-Type": "text/plain"}
            )  # Or just drop: flow.kill()
            return  # Stop processing the request

        # Log the request (optional)
        logging.info(f"Forwarding request from {client_ip}")

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Handle the HTTP response.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]
        logging.info(
            f"Received response from {flow.request.url} for {client_ip} "
            f"(status code: {flow.response.status_code})"
        )

addons = [TransparentProxy()]
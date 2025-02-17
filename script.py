import logging
import os
from typing import Any

import mitmproxy
from mitmproxy import http

# Configure logging
logging.basicConfig(
    filename="proxy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Use environment variable for blocked IP
blocked_ip = os.getenv("BLOCKED_IP", "1.2.3.4")

class TransparentProxy:
    """A transparent proxy class to block requests from a specific IP address and log other requests."""

    def request(self, flow: http.HTTPFlow) -> None:
        """Handle the HTTP request.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]  # Get client IP

        if not self.is_valid_ip(client_ip):
            logging.warning(f"Invalid IP address detected: {client_ip}")
            return

        if client_ip == blocked_ip:
            logging.info(f"Blocked request from {client_ip} to {self.sanitize_url(flow.request.url)}")
            flow.response = http.HTTPResponse.make(
                403, b"Forbidden", {"Content-Type": "text/plain"}
            )
            return  # Stop processing the request

        # Log the request (optional)
        logging.info(f"Forwarding request from {client_ip} to {self.sanitize_url(flow.request.url)}")

    def response(self, flow: http.HTTPFlow) -> None:
        """Handle the HTTP response.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]
        logging.info(
            f"Received response from {self.sanitize_url(flow.request.url)} for {client_ip} "
            f"(status code: {flow.response.status_code})"
        )

    def is_valid_ip(self, ip: str) -> bool:
        """Validate the IP address format."""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True

    def sanitize_url(self, url: str) -> str:
        """Sanitize the URL before logging."""
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

addons = [TransparentProxy()]